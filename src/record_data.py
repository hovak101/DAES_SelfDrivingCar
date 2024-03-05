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
    B_IN4 = LED(24) 
    
    # back right gpio
    B_ENA = PWMLED(12)
    B_IN1 = LED(14)
    B_IN2 = LED(23)
    
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

        # determines when to switch opposite sided motors to reverse for turns;
        # decimal values from 0 to 1
        self.reverse_turn_percent = 0.8
        
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
        self.speed = self.trigger_to_PWM(value)
        self.update_pins()
        
    def on_R2_release(self):
        self.speed = 0
        self.update_pins()
    
    def on_L2_press(self, value):
        self.reverse = True
        self.speed = self.trigger_to_PWM(value)
        self.update_pins()
    
    def on_L2_release(self):
        self.reverse = False
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
    
    def switch_motor_direction(self, motor_id):
        if motor_id == 'FL':
            if self.F_IN1.value == 0 and self.F_IN2.value == 1:
                self.F_IN1.on()
                self.F_IN2.off()
            elif self.F_IN1.value == 1 and self.F_IN2.value == 0:
                self.F_IN1.off()
                self.F_IN2.on()
            else:
                raise Exception("Error switching motor direction: Motor is neither moving forward nor backward") 
                    
        elif motor_id == 'FR':
            if self.F_IN3.value == 0 and self.F_IN4.value == 1:
                self.F_IN3.on()
                self.F_IN4.off()
            elif self.F_IN3.value == 1 and self.F_IN4.value == 0:
                self.F_IN3.off()
                self.F_IN4.on()
            else:
                raise Exception("Error switching motor direction: Motor is neither moving forward nor backward")
        
        elif motor_id == 'BL':
            if self.B_IN3.value == 0 and self.B_IN4.value == 1:
                self.B_IN3.on()
                self.B_IN4.off()
            elif self.B_IN3.value == 1 and self.B_IN4.value == 0:
                self.B_IN3.off()
                self.B_IN4.on()
            else:
                raise Exception("Error switching motor direction: Motor is neither moving forward nor backward")
            
        elif motor_id == 'BR':
            if self.B_IN1.value == 0 and self.B_IN2.value == 1:
                self.B_IN1.on()
                self.B_IN2.off()
            elif self.B_IN1.value == 1 and self.B_IN2.value == 0:
                self.B_IN1.off()
                self.B_IN2.on()
            else:
                raise Exception("Error switching motor direction: Motor is neither moving forward nor backward")
                
    def update_pins(self):
        # TODO: Simplify this so that its simply that the speed and relative speed can both either be positive or negative, and that the sign of the product
        # determines the direction of the spin with some if statements. No need for this switch direction thing. Also, for the reversal percent, that means
        # that instead of the reversal percent should somehow determine the threshold rather than the sign of the product as mentioned above. 
        if self.reverse:
            self.F_IN1.off()
            self.F_IN2.on()
            
            self.F_IN3.off()
            self.F_IN4.on()
            
            self.B_IN1.off()
            self.B_IN2.on()
            
            self.B_IN3.off()
            self.B_IN4.on()
        else:
            self.F_IN1.on()
            self.F_IN2.off()
            
            self.F_IN3.on()
            self.F_IN4.off()
            
            self.B_IN1.on()
            self.B_IN2.off()
            
            self.B_IN3.on()
            self.B_IN4.off()
        
        # left speed
        if self.relative_left_speed < 0:
            self.switch_motor_direction('FL')
            self.switch_motor_direction('BL')
            
        self.F_ENA.value = self.speed * abs(self.relative_left_speed)
        self.B_ENB.value = self.speed * abs(self.relative_left_speed)
        
        # right speed
        if self.relative_right_speed < 0: 
            self.switch_motor_direction('FR')
            self.switch_motor_direction('BR')
        
        self.F_ENB.value = self.speed * abs(self.relative_right_speed)
        self.B_ENA.value = self.speed * abs(self.relative_right_speed)
        
if __name__ == "__main__":
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen()