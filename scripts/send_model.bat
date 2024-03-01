@REM RUN ON PC
@REM This scripts sends model weights to RPI over SSH

for /f "delims=" %%a in ('type "C:\Users\CoreV21\Desktop\DAES_SelfDrivingCar\.env"') do set %%a
for /f "delims=" %%a in ('type "C:\Users\CoreV21\Desktop\DAES_SelfDrivingCar\.env.private"') do set %%a

scp -r %ROOT_DIR_PC%\model.tflite %SSH_USERNAME%@%SSH_ADDRESS%:%ROOT_DIR_PI%

