from MotorDriver import MotorDriver
from gpiozero import RotaryEncoder
import time

# 1. Inicialización
driver = MotorDriver()
enc_a = RotaryEncoder(16, 17, max_steps=0)
enc_b = RotaryEncoder(5, 6, max_steps=0)

print("=== DIAGNÓSTICO DE ENCODERS ===")
print("Las ruedas girarán durante 5 segundos.")
print("Levanta el robot para que no se escape.")

# 2. Reset de pasos
enc_a.steps = 0
enc_b.steps = 0

# 3. Arrancar motores (Ajusta 'forward'/'backward' según tu cableado)
# En el modo dual usas uno de cada para ir recto:
driver.MotorRun(0, 'forward', 30)
driver.MotorRun(1, 'backward', 30)

try:
    for i in range(10):
        pa = abs(enc_a.steps)
        pb = abs(enc_b.steps)
        print(f"Tiempo: {i*0.5}s | Motor A: {pa} | Motor B: {pb} | Dif: {abs(pa-pb)}")
        time.sleep(0.5)

finally:
    driver.MotorStop(0)
    driver.MotorStop(1)
    print("\n=== TEST FINALIZADO ===")
    print(f"TOTAL Motor A: {abs(enc_a.steps)}")
    print(f"TOTAL Motor B: {abs(enc_b.steps)}")
