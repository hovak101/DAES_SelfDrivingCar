# RUN ON RPI
# Deletes all data on the pi

source /home/pi/Desktop/DAES_SelfDrivingCar/.env;
rm -r $ROOT_DIR_PI/data/frames/*;
> /home/pi/Desktop/DAES_SelfDrivingCar/data/act_values.csv;
