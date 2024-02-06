import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

message = "vostikanutsyun\n"
while True:
    ser.write(message.encode('utf-8'))
    ser.flush()
    time.sleep(1)
