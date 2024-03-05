from gpiozero import LED, PWMLED

class RcDriver:
    # front left gpio
    F_ENA = PWMLED(13)
    F_IN1 = LED(27)
    F_IN2 = LED(22)

    # front right gpio
    F_ENB = PWMLED(19)
    F_IN3 = LED(17)
    F_IN4 = LED(4)

    # back left gpio
    B_ENB = PWMLED(18)
    B_IN3 = LED(15)
    B_IN4 = LED(24) 
    
    # back right gpio
    B_ENA = PWMLED(12)
    B_IN1 = LED(14)
    B_IN2 = LED(23)
    
    # turn_reversal_percent: float from 0 to 1; determines what percent the 
    # relative right or left speed needs to be engaged in order for the opposite
    # wheels to start reversing
    # def __init__(self):
    #     pass
        
    def set_pins(self, left_pwm, right_pwm, reverse_left, reverse_right):
        self.F_ENA.value = left_pwm
        self.B_ENB.value = left_pwm
        self.F_ENB.value = right_pwm
        self.B_ENA.value = right_pwm
        
        if reverse_left:
            # front left reverse
            self.F_IN1.off()
            self.F_IN2.on()
            
            # back left reverse
            self.B_IN3.off()
            self.B_IN4.on()
            
        else:
            # front left forward
            self.F_IN1.on()
            self.F_IN2.off()
            
            # back left forward
            self.B_IN3.on()
            self.B_IN4.off()
            
        if reverse_right:
            # front right reverse
            self.F_IN3.off()
            self.F_IN4.on()
            
            # back right reverse
            self.B_IN1.off()
            self.B_IN2.on()
        
        else:
            # front right forward
            self.F_IN3.on()
            self.F_IN4.off()
            
            # back right forward
            self.B_IN1.on()
            self.B_IN2.off()