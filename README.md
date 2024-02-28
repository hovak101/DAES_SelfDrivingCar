# DAES_SelfDrivingCar
Car stuff that uses camera stuff to evade obstacles swoosh swoosh 👀🚗

Execution Stack:
1. Record Data (RPI)
4. Send Data (RPI)
5. Train Model (PC)
6. Send Model (PC)
7. Run Car (RPI)

## To replicate this setup on your own raspberry pi(rc car):

1. navigate to the root directory of this project and create a virtual
environment with the following command: 

  ```python -m venv rc_env```

2. Then install all dependencies with the  following command: 

  ```pip install -r pi_requirements.txt```

## To replicate this setup on PC(neural net training):

1. navigate to the root directory of this project and create a virtual
environment with the following command: 

  ```python -m venv train_env```

2. Then install all dependencies with the  following command: 

  ```pip install -r train_requirements.txt```