# RUN ON RPI
# The goal of this file is to:
#   1. Connect rpi to bluetooth controller
#       a. Mappings for DS4
#           i.   R2 = forward
#           ii.  L2 = backward
#           iii. L3 = steering
#           iv.  Triangle = Start/Stop Recording
#   2. Record video frames and corresponding actuator values
#       a. Frames go in frames folder, named "frame_x"
#       b. Actuator values go in csv
#           i. Columns: frame_id, act_1, act_2, act_3, act_4
#           iii. actuators are measured by duty load percentage, 
#           so the values should be from 0 to 1.

from pyPS4Controller.controller import Controller
from rcDriverController import RcDriver
import cv2
import threading
import time
import os 
from dotenv import load_dotenv
import csv

class MyController(Controller):
   
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        load_dotenv()
        
        # delete contents of csv file and define column names
        self.csv_file =  open(os.path.join(os.getenv('ROOT_DIR_PI'), 'data', 'act_values.csv'), 'w')
        self.writer = csv.writer(self.csv_file)
        field = ['frame_id', 'front_left', 'back_left', 'front_right', 'back_right']
        self.writer.writerow(field)
            
        # delete contents of frames folder
        frames_directory = os.path.join(os.getenv('ROOT_DIR_PI'), 'data', 'frames')
        frames_files = os.listdir(frames_directory)
        for file in frames_files:
            file_path = os.path.join(frames_directory, file)
            os.remove(file_path)
            
        self.recording = False
        self.vid = None
        self.count = 0
        self.time_between_frames = 1 / int(os.getenv('FPS'))
        
        # create a lock for thread-safe operations
        self.lock = threading.Lock()
        
        # PWM straight line speed for all motors; decimal value from 0 to 1
        self.speed = 0

        # the relative speeds for the left and right sides; decimal values from 0 to 1
        self.relative_left_speed = 1
        self.relative_right_speed = 1

        self.left_speed = None
        self.right_speed = None
        self.left_reverse = False
        self.right_reverse = False
        
        # determines when to switch opposite sided motors to reverse for turns;
        # decimal values from 0 to 1
        self.reverse_turn_percent = 0.8
        
        self.rc_driver = RcDriver()

    def on_triangle_press(self):
        with self.lock:
            self.recording = not self.recording
            if self.recording:
                self.vid = cv2.VideoCapture(0)
                # start the background thread for capturing frames
                threading.Thread(target=self.capture_frames, daemon=True).start()
            else:
                # release the video capture object
                self.vid.release()

    def on_R2_press(self, value):
        self.speed = self.trigger_to_PWM(value)
        self.update_pins()
        
    def on_R2_release(self):
        self.speed = 0
        self.update_pins()
    
    def on_L2_press(self, value):
        self.reverse = True
        self.speed = -1 * self.trigger_to_PWM(value)
        self.update_pins()
    
    def on_L2_release(self):
        self.speed = 0
        self.update_pins()
        
    def on_L3_left(self, value):
        self.relative_left_speed = self.L3_to_relative(value)
        self.update_pins()
        
    def on_L3_right(self, value):
        self.relative_right_speed = self.L3_to_relative(value)
        self.update_pins()
        
    def on_L3_x_at_rest(self):
        self.relative_left_speed = 1
        self.relative_right_speed = 1
        self.update_pins()
    
    def capture_frames(self):
        while self.recording:
            start = time.time()
            
            with self.lock:
                ret, frame = self.vid.read()
                if ret:
                    file_path = os.path.join(os.getenv('ROOT_DIR_PI'), 'data', 
                                            'frames', f'frame_{self.count}.jpg')
                    cv2.imwrite(file_path, frame)
                  
                    self.writer.writerow([self.count, self.F_ENA, self.B_ENB, self.F_ENB, self.B_ENA])
                    self.count += 1
            
            end = time.time()
            elapsed = end - start
            
            if elapsed < self.time_between_frames:
                time.sleep(self.time_between_frames - elapsed)

    def trigger_to_PWM(self, value):
        return (value + 32767) / 65534
        
    def L3_to_relative(self, value):
        # print("percent offset:", abs(value) / 16384)
        # print("relative speed:", self.reverse_turn_percent - abs(value) / 16384)
        return self.reverse_turn_percent - abs(value) / 32767
                
    def convert_to_pwm(self):
        left_reverse = False
        right_reverse = False
        
        if self.left_speed < 0:
            left_reverse = True
        
        if self.right_speed < 0:
            right_reverse = True
            
        left_pwm = abs(self.left_speed)
        right_pwm = abs(self.right_speed)
        
        return left_pwm, right_pwm, left_reverse, right_reverse
    
    def update_pins(self):
        left_pwm, right_pwm, left_reverse, right_reverse = self.convert_to_pwm()
        self.rc_driver.set_pins(left_pwm, right_pwm, left_reverse, right_reverse)
        
if __name__ == "__main__":
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen()