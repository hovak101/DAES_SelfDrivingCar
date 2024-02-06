# RUN ON RPI
# The goal of this file is to:
#   1. Connect rpi to bluetooth controller
#       a. Mappings for DS4
#           i.   R2 = forward
#           ii.  L2 = backward
#           iii. L3 = steering
#           iv.  Triangle = Start/Stop Recording
#   2. Record video frames and corresponding actuator values
#       a. Frames go in frames folder, names "frame_x"
#       b. Actuator values go in csv
#           i. Columns: frame_id, act_1, act_2, act_3, act_4
#           iii. actuators are measured by duty load percentage, 
#           so the values should be from 0 to 1.

from pyPS4Controller.controller import Controller
import cv2
import threading
import time

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

if __name__ == "__main__":
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen()