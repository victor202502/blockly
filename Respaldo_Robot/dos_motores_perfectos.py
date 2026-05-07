from MotorDriver import MotorDriver
from gpiozero import RotaryEncoder
import time

# --- ESTIMACIÓN BASADA EN TUS DATOS ---
PULSOS_POR_VUELTA = 1393.0  # Corregido: antes era 1471
OFFSET_FRENADO = 465        # Para frenar en seco a Potencia 80
POTENCIA = 80 

# Motores
encoder_a = RotaryEncoder(16, 17, max_steps=0)
encoder_b = RotaryEncoder(5, 6, max_steps=0)
driver = MotorDriver()

def avanzar_vueltas(vueltas):
    objetivo = int(vueltas * PULSOS_POR_VUELTA)
    punto_corte = objetivo - OFFSET_FRENADO

    print(f"--- AVANCE 80% + FRENO ACTIVO ---")
    print(f"Objetivo: {objetivo} pulsos.")

    encoder_a.steps = 0
    encoder_b.steps = 0

    driver.MotorRun(0, 'forward', POTENCIA)
    driver.MotorRun(1, 'backward', POTENCIA)

    running_a = True
    running_b = True

    while running_a or running_b:
        pasos_a = abs(encoder_a.steps)
        pasos_b = abs(encoder_b.steps)

        # Control Motor A (MA) con Freno
        if running_a and pasos_a >= punto_corte:
            driver.MotorBrake(0) # ¡FRENAZO!
            running_a = False
            print(f"\n[!] Motor A frenado en {pasos_a}")

        # Control Motor B (MB) con Freno
        if running_b and pasos_b >= punto_corte:
            driver.MotorBrake(1) # ¡FRENAZO!
            running_b = False
            print(f"\n[!] Motor B frenado en {pasos_b}")

        print(f"A: {pasos_a}/{objetivo} | B: {pasos_b}/{objetivo}    ", end="\r")
        time.sleep(0.001)

    # Dejamos el freno activo 0.2 segundos para clavar la posición
    time.sleep(0.2)
    driver.MotorStop(0)
    driver.MotorStop(1)

    print(f"\nPosición Final -> A: {abs(encoder_a.steps)} | B: {abs(encoder_b.steps)}")
    print(f"Error A: {abs(encoder_a.steps) - objetivo} pulsos")

try:
    # Probamos las 20 vueltas de nuevo
    avanzar_vueltas(20.0)

except KeyboardInterrupt:
    driver.MotorStop(0)
    driver.MotorStop(1)
