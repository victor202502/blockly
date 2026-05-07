from gpiozero import RotaryEncoder
import time

encoder = RotaryEncoder(23, 24, max_steps=0)

print("Gira la rueda con la mano. Ctrl+C para salir.")
try:
    while True:
        print(f"Pasos: {encoder.steps}    ", end="\r")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nTest finalizado.")
