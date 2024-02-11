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

# front left
f_ena = PWMLED(13)
f_in1 = LED(27)
f_in2 = LED(22)

# front right
f_enb = PWMLED(19)
f_in3 = LED(17)
f_in4 = LED(4)

# back left
b_ena = PWMLED(12)
b_in1 = LED(14)
# b_in2 = LED()

# back right
b_enb = PWMLED(18)
b_in3 = LED(15)
# b_in4 = LED()

class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.recording = False
        self.vid = None
        self.count = 0
        # Create a lock for thread-safe operations
        self.lock = threading.Lock()

    def on_triangle_press(self):
        with self.lock:
            self.recording = not self.recording
            if self.recording:
                self.vid = cv2.VideoCapture(0)
                # Start the background thread for capturing frames
                threading.Thread(target=self.capture_frames, daemon=True).start()
            else:
                # Release the video capture object
                self.vid.release()

    def on_R2_press(self, value):
        pwm = self.R2_to_PWM(value)
        
    
    def capture_frames(self):
        while self.recording:
            with self.lock:
                ret, frame = self.vid.read()
                if ret:
                    file_path = f"../data/frames/frame_{self.count}.jpg"
                    cv2.imwrite(file_path, frame)
                    self.count += 1
            # Add a small delay to give time back to the main thread
            time.sleep(0.1)

    def R2_to_PWM(self, value):
        return (value + 32767) / 65534
        
        
if __name__ == "__main__":
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen()