from machine import UART, Pin
import time

# Initialize UART0
uart = UART(0, baudrate=115200)

# Led Control Pin
led = Pin('LED', Pin.OUT)

while True:
  if uart.any():
      data = uart.read().decode('utf-8')
      print(data)
  time.sleep(0.1)