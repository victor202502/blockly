from PCA9685 import PCA9685

class MotorDriver():
    def __init__(self):
        # Inicializamos con la dirección 0x40
        self.pwm = PCA9685(0x40)
        self.pwm.setPWMFreq(50)

    def MotorRun(self, motor, direction, speed):
        if speed > 100: speed = 100
        
        if motor == 0:
            # Motor A: Canal 0=PWM, 1=DIR1, 2=DIR2
            self.pwm.setDutycycle(0, speed)
            if direction == 'forward':
                self.pwm.setLevel(1, 0)
                self.pwm.setLevel(2, 1)
            else:
                self.pwm.setLevel(1, 1)
                self.pwm.setLevel(2, 0)
        else:
            # Motor B: Canal 5=PWM, 3=DIR1, 4=DIR2
            self.pwm.setDutycycle(5, speed)
            if direction == 'forward':
                self.pwm.setLevel(3, 0)
                self.pwm.setLevel(4, 1)
            else:
                self.pwm.setLevel(3, 1)
                self.pwm.setLevel(4, 0)

    def MotorStop(self, motor):
        if motor == 0:
            self.pwm.setDutycycle(0, 0)
            self.pwm.setLevel(1, 0)
            self.pwm.setLevel(2, 0)
        else:
            self.pwm.setDutycycle(5, 0)
            self.pwm.setLevel(3, 0)
            self.pwm.setLevel(4, 0)
  
    def MotorBrake(self, motor):
        if motor == 0:
            # Motor A: Bloqueamos poniendo los 3 canales al máximo
            self.pwm.setPWM(0, 0, 4095) # Velocidad a tope
            self.pwm.setPWM(1, 0, 4095) # Dirección 1 a tope
            self.pwm.setPWM(2, 0, 4095) # Dirección 2 a tope
        else:
            # Motor B: Canales 5, 3 y 4
            self.pwm.setPWM(5, 0, 4095)
            self.pwm.setPWM(3, 0, 4095)
            self.pwm.setPWM(4, 0, 4095)
