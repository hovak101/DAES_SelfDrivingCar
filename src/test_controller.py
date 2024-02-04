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
            
    def my_sequences(self):
        return [
            {"inputs": ['up', 'up'],
            "callback": delete_data_callback}
        ]
    
    def delete_data_callback(self):
        print("Sequence detected, now deleting.")

if __name__ == "__main__":
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen()
