# RUN ON RPI
# The goal of this file is to: 
#   1. Define and then load the model weights
#   2. Run car
#       a. Loop: 
#           i.   Get video frame as np array
#           ii.  Then something like (act_1, act_2 ...) = model.fit(frame as np array)
#           iii. Set actuator values to rc car