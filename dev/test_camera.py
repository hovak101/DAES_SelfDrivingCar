import cv2
import subprocess
from dotenv import load_dotenv
import os

load_dotenv()

count = 0
vid = cv2.VideoCapture(0)

while True: 
    if count == 1: 
        subprocess.check_call(os.path.join(
            os.getenv('ROOT_DIR_PI'), 'scripts', 
            'set_camera_preset.sh'), shell=True)
    ret, frame = vid.read()
    if frame is None:
        print("Error: Image not loaded")
    else:
        # Display the image dimensions
        print("Image dimensions:", frame.shape)
    
    if ret: 
        cv2.imshow('frame', frame) 

    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
    count += 1
  
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows()