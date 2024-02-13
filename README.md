# DAES_SelfDrivingCar
Car stuff that uses camera stuff to evade obstacles swoosh swoosh 👀🚗

Execution Stack:
1. Record Data (RPI)
RUN ON RPI
The goal of this file is to:
  1. Connect rpi to bluetooth controller
      a. Mappings for DS4
          i.   R2 = forward
          ii.  L2 = backward
          iii. L3 = steering
          iv.  Triangle = Start/Stop Recording
  2. Record video frames and corresponding actuator values
      a. Frames go in frames folder, named "frame_x"
      b. Actuator values go in csv
          i. Columns: frame_id, act_1, act_2, act_3, act_4
          iii. actuators are measured by duty load percentage, 
          so the values should be from 0 to 1.

4. Send Data (RPI)
5. Train Model (PC)
6. Send Model (PC)
7. Run Car (RPI)
