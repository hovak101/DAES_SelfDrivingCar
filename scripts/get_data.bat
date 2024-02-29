@REM RUN ON PC
@REM This script deletes all content in the data folder and upates the data folder
@REM with the latest data from the RPI

for /f "delims=" %%a in ('type "C:\Users\CoreV21\Desktop\DAES_SelfDrivingCar\.env"') do set %%a
for /f "delims=" %%a in ('type "C:\Users\CoreV21\Desktop\DAES_SelfDrivingCar\.env.private"') do set %%a
rmdir /S %ROOT_DIR_PC%\data
scp -r %SSH_USERNAME%@%SSH_ADDRESS%:%ROOT_DIR_PI%/data %ROOT_DIR_PC%