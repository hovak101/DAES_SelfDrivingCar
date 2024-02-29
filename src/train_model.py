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
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization, Input, GlobalAveragePooling2D
from keras.callbacks import EarlyStopping

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

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    # Currently, memory growth needs to be the same across GPUs
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
  except RuntimeError as e:
    # Memory growth must be set before GPUs have been initialized
    print(e)

# Define model
model = Sequential([
    Input(shape=(480, 640, 3)),
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    BatchNormalization(),
    
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    BatchNormalization(),
    
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    BatchNormalization(),
    
    GlobalAveragePooling2D(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(5, activation='sigmoid')
])

model.compile(optimizer='adam', loss='mse')

early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=1, 
                               mode='min', restore_best_weights=True)

model.fit(frames, act_vals, epochs=100, batch_size=8, validation_split=0.2, 
                                callbacks=[early_stopping])