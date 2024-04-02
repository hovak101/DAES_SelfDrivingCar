# RUN ON RPI
# sets camera settings, including focus, exposure, color, etc.

source /home/pi/Desktop/DAES_SelfDrivingCar/.env;
python3 /home/pi/Desktop/cameractrls/cameractrls.py -c focus_automatic_continuous=0,focus_absolute=70,auto_exposure=manual_mode,exposure_time_absolute=77,exposure_dynamic_framerate=0,gain=255,white_balance_automatic=0,white_balance_temperature=2809,brightness=150;