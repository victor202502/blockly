from MotorDriver import MotorDriver
from gpiozero import RotaryEncoder
import time

PULSOS_POR_VUELTA = 357.74
VUELTAS = 10
OBJETIVO = int(PULSOS_POR_VUELTA * VUELTAS)

encoder = RotaryEncoder(23, 24, max_steps=0)
driver = MotorDriver()

try:
    print(f"--- TEST DE {VUELTAS} VUELTAS ---")
    encoder.steps = 0
    driver.MotorRun(0, 'forward', 35) # Un poco más de potencia para el test
    
    while abs(encoder.steps) < (OBJETIVO - 16):
        print(f"Progreso: {abs(encoder.steps)} / {OBJETIVO}    ", end="\r")
        time.sleep(0.001)
        
    driver.MotorStop(0)
    print(f"\nResultado final: {abs(encoder.steps)} pulsos.")

except KeyboardInterrupt:
    driver.MotorStop(0)
