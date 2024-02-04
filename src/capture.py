# import the opencv library 
import cv2 


# define a video capture object 
vid = cv2.VideoCapture(0) 

# frame count
count = 0
# switch for triangle button on DS4
recording = False

while(recording): 
	# Capture the video frame 
	# by frame 
	ret, frame = vid.read()
	file_path = "../data/frames/frame_%i.jpg" % count
	cv2.imwrite(file_path, frame)
	count = count + 1
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 

