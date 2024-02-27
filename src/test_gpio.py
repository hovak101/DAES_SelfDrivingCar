from gpiozero import LED, PWMLED
from time import sleep

# front left
f_ena = PWMLED(13)
f_in1 = LED(27)
f_in2 = LED(22)

# front right
f_enb = PWMLED(19)
f_in3 = LED(17)
f_in4 = LED(4)

# back left
b_enb = PWMLED(18)
b_in3 = LED(15)
b_in4 = LED(24)

# back right
b_ena = PWMLED(12)
b_in1 = LED(14)
b_in2 = LED(23)

try:
    while True:
        f_ena.value = 0.5
        f_in1.off()
        f_in2.on()
        
        f_enb.value = 0.5
        f_in3.off()
        f_in4.on()
        
        b_ena.value = 0.5
        b_in1.off()
        b_in2.on()
        
        b_enb.value = 0.5
        b_in3.off()
        b_in4.on()
        
        sleep(1)
except KeyboardInterrupt:
    print("\nExiting Program...")
    f_in1.off()
    f_in2.off()
    f_ena.off()
    # f_in3.off()
    # f_in4.off()
    # f_enb.off()