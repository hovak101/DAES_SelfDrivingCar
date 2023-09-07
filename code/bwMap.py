import numpy as np
import cv2
from matplotlib import pyplot as plt
import time

def getDisparity(bSize, imgLeft, imgRight):
    # Initialize the stereo block matching object 
    SBMObj = cv2.StereoBM_create(numDisparities=32, blockSize=bSize)

    # Compute the disparity image
    disparity = SBMObj.compute(imgLeft, imgRight)

    # Normalizing image
    min = disparity.min()
    max = disparity.max()
    disparity = np.uint8(255 * (disparity - min) / (max - min))

    return disparity

try:
    start_time = time.perf_counter()

    greyscale_threshold = 180
    imgLeft = cv2.imread('limg.ppm', 0)
    imgRight = cv2.imread('rimg.ppm', 0)

    if imgLeft.shape[0] != imgRight.shape[0]:
        raise Exception("Left and right image heights are not the same.")
    if imgLeft.shape[1] != imgRight.shape[1]:
        raise Exception("Left and right image widths are not the same.")
    
    # bSize has to be an odd number
    result = getDisparity(35, imgLeft, imgRight) 

    # boolean mask
    above_threshold = result > greyscale_threshold

    numClose = np.sum(above_threshold)

    totalSize = result.size

    percentClose = numClose/totalSize
    #print(str(percentClose) + "%")

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"The execution time is: {execution_time}")
    plt.imshow(result, 'gray') 
    plt.axis('off')
    plt.show()

except Exception as inst:
    print("Error: ", inst.args)
