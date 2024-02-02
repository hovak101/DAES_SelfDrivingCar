import tensorflow as tf 
import keras
import csv # to convert .csv -> nparray
from PIL import Image # to convert jpg -> nparray
from keras import layers

model = keras.Sequential # define model

img = Image.open('frame.jpg') # replace this with frame
nparr = asarray(img) # np array formed from frame


# ...

# xs = numframes * 1920*1080*3
model.fit(xs,ys)



# RUN ON PC
# The goal of this file is to: 
#   1. Define model: model.Sequential.blablabla
#   2. Use opencv or np to create np arrays from jpgs
#   3. Use pandas or np to extract data from csv and put into numpy array
#   4. Compile model and then train: model.fit(xs, ys, epochs="...")
#       a. xs should be (# of frames) * 1920 * 1080 * 3
#       b. ys should be (# of frames) * 4     