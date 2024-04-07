# RUN ON RPI
# The goal of this file is to: 
#   1. Define and then load the model weights
#   2. Run car
#       a. Loop: 
#           i.   Get video frame as np array
#           ii.  Then something like (act_1, act_2 ...) = model.fit(frame as np array)
#           iii. Set actuator values to rc car

import numpy as np
import tensorflow as tf
from dotenv import load_dotenv
import os
import cv2
from rcDriverController import RcDriver
import subprocess
import time
import threading

load_dotenv()

os.path.join(os.getenv('ROOT_DIR_PI'), 'model.tflite')
# Load the TFLite model and allocate tensors
interpreter = tf.lite.Interpreter(model_path=os.path.join(os.getenv('ROOT_DIR_PI'), 
                                                          'model.tflite'))
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# check shapes 
input_shape = input_details[0]['shape']
print("input shape:", input_shape)
output_shape = output_details[0]['shape']
print("output shape:", output_shape)

vid = cv2.VideoCapture(0)
rc_driver = RcDriver()

prev = time.time()
count = 0
lock = threading.Lock()

while True:
    try:
        time_elapsed = time.time() - prev
        ret, frame = vid.read()

        if time_elapsed > 1./int(os.getenv('FPS')):

            if count == 1:
                # subprocess.check_call(os.path.join(
                #         os.getenv('ROOT_DIR_PI'), 'scripts', 
                #         'set_camera_preset.sh'), shell=True)
                pass
            
            if ret: 
                if count > 0:
                    threading.Thread(target=frame_to_output, daemon=True).start()
                count += 1

            prev = time.time()
            # cv2.imshow('frame', frame)
            # cv2.waitKey(1)
        
    except KeyboardInterrupt:
        vid.release()
        break

    def frame_to_output():
        with lock:
            # print("in thread")
            input_data = np.expand_dims(np.asarray(frame, dtype=np.float32), axis=0)
                        
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()

            # The function `get_tensor()` returns a copy of the tensor data
            output_data = interpreter.get_tensor(output_details[0]['index'])
            # print(output_data)
            front_left = output_data[0][0]
            back_left = output_data[0][1]
            front_right = output_data[0][2]
            back_right = output_data[0][3]
            print("FL:", front_left)
            print("BL", back_left)
            print("FR:", front_right)
            print("BR", back_right)
            reverse_left = False
            reverse_right = False
            
            if front_left < 0:
                reverse_left = True
            
            if front_right < 0: 
                reverse_right = True
                
            rc_driver.set_pins(abs(front_left), abs(front_right), reverse_left, reverse_right)
