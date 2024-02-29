# RUN ON PC
# The goal of this file is to: 
#   1. Define model: model.Sequential.blablabla
#   2. Use opencv or np to create np arrays from jpgs
#   3. Use pandas or np to extract data from csv and put into numpy array
#   4. Compile model and then train: model.fit(xs, ys, epochs="...")
#       a. xs should be (# of frames) * 1920 * 1080 * 3
#       b. ys should be (# of frames) * 4     

import numpy as np
from PIL import Image
import csv
import os
from dotenv import load_dotenv
import numpy as np
import tensorflow as tf 
import keras
from keras import layers

load_dotenv()

# convert csv actuator values to numpy array
with open(os.path.join(os.getenv('ROOT_DIR_PC'), 'data', 'act_values.csv'), 'r') as file:
    reader = csv.reader(file)
    data = list(reader)
    act_vals = np.array(data[1:], dtype=float)

frames_dir = os.path.join(os.getenv('ROOT_DIR_PC'), 'data', 'frames')
frames = []

for img_name in os.listdir(frames_dir):
    # create numpy array from image
    img_path = os.path.join(frames_dir, img_name)
    img = Image.open(img_path)
    np_img = np.asarray(img)
    
    # add numpy image to frames
    frames.append(np_img)
    
# convert list of numpy arrays to numpy array
frames = np.array(frames)