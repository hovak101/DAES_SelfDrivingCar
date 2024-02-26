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
from gpiozero import LED, PWMLED
import cv2
import threading
import time
import os 
from dotenv import load_dotenv
import csv

class MyController(Controller):
    # front left gpio
    F_ENA = PWMLED(13)
    F_IN1 = LED(27)
    F_IN2 = LED(22)

    # front right gpio
    F_ENB = PWMLED(19)
    F_IN3 = LED(17)
    F_IN4 = LED(4)

    # back left gpio
    B_ENB = PWMLED(18)
    B_IN3 = LED(15)
    # B_IN4 = LED() waiting on jumper cable

    # back right gpio
    B_ENA = PWMLED(12)
    B_IN1 = LED(14)
    # B_IN2 = LED() waiting on jumper cable
    
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        load_dotenv()
        
        # delete contents of csv file and define column names
        self.csv_file =  open(os.path.join(os.getenv('ROOT_DIR'), 'data', 'act_values.csv'), 'w')
        self.writer = csv.writer(self.csv_file)
        field = ['frame_id', 'front_left', 'back_left', 'front_right', 'back_right']
        self.writer.writerow(field)
            
        # delete contents of frames folder
        frames_directory = os.path.join(os.getenv('ROOT_DIR'), 'data', 'frames')
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

        # reversing boolean
        self.reverse = False
        
        self.update_pins()

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
        self.speed = self.R2_to_PWM(value)
        print(self.speed)
        self.update_pins()
        
    def on_R2_release(self):
        self.speed = 0
        self.update_pins()
    
    def on_L3_left(self, value):
        self.relative_left_speed = self.L3_to_relative(value)
        print(self.relative_left_speed)
        self.update_pins()
        
    def on_L3_right(self, value):
        self.relative_right_speed = self.L3_to_relative(value)
        print(self.relative_right_speed)
        self.update_pins()
        
    def on_L3_x_at_rest(self):
        self.relative_left_speed = 1
        self.relative_right_speed = 1
        print(self.relative_left_speed, self.relative_right_speed)
        self.update_pins()
    
    def capture_frames(self):
        while self.recording:
            start = time.time()
            
            with self.lock:
                ret, frame = self.vid.read()
                if ret:
                    file_path = os.path.join(os.getenv('ROOT_DIR'), 'data', 
                                            'frames', f'frame_{self.count}.jpg')
                    cv2.imwrite(file_path, frame)
                    
                    # act values
                    frame_id = self.count
                    front_left = self.speed * self.relative_left_speed
                    back_left = self.speed * self.relative_left_speed
                    front_right = self.speed * self.relative_right_speed
                    back_right = self.speed * self.relative_right_speed
                    
                    self.writer.writerow([frame_id, front_left, back_left, front_right, back_right])
                    self.count += 1
            
            end = time.time()
            elapsed = end - start
            
            if elapsed < self.time_between_frames:
                time.sleep(self.time_between_frames - elapsed)
            else:
                print("ERROR: GONE OVERTIME")

    def R2_to_PWM(self, value):
        return (value + 32767) / 65534
        
    def L3_to_relative(self, value):
        return 1 - abs(value) / 32767
    
    def update_pins(self):
        if self.reverse:
            self.F_IN1.off()
            self.F_IN2.on()
            
            self.F_IN3.off()
            self.F_IN4.on()
            
            self.B_IN1.off()
            # self.B_IN2.on() waiting on jumper wire
            
            self.B_IN3.off()
            # self.B_IN4.on() waiting on jumper wire
        else:
            self.F_IN1.on()
            self.F_IN2.off()
            
            self.F_IN3.on()
            self.F_IN4.off()
            
            self.B_IN1.on()
            # self.B_IN2.off() waiting on jumper wire
            
            self.B_IN3.on()
            # self.B_IN4.off() waiting on jumper wire
        
        # left speed
        self.F_ENA.value = self.speed * self.relative_left_speed
        self.B_ENB.value = self.speed * self.relative_left_speed
        
        # right speed
        self.F_ENB.value = self.speed * self.relative_right_speed
        self.B_ENA.value = self.speed * self.relative_right_speed
        
if __name__ == "__main__":
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen()