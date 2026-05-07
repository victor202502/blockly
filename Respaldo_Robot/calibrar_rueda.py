from gpiozero import RotaryEncoder
import time

# Usamos el encoder profesional en los pines correctos
encoder = RotaryEncoder(16, 17, max_steps=0)

print("=== CALIBRADOR DE PRECISIÓN ===")
print("1. Pon una marca clara en la rueda (un trozo de cinta o rotulador).")
print("2. Gira la rueda A MANO dando EXACTAMENTE 10 VUELTAS.")
print("3. Cuando acabes la vuelta 10, pulsa Ctrl+C.\n")
print("(Nota: El motor está libre, puedes girarlo sin problema)")

try:
    # Ponemos el contador a 0
    encoder.steps = 0
    
    while True:
        # Usamos abs() para que el número siempre sea positivo en pantalla
        print(f"Pulsos acumulados: {abs(encoder.steps)}    ", end="\r")
        time.sleep(0.1)

except KeyboardInterrupt:
    total_pulsos = abs(encoder.steps)
    pulsos_por_vuelta = total_pulsos / 10
    
    print("\n\n--- RESULTADOS ---")
    print(f"Pulsos totales (10 vueltas): {total_pulsos}")
    print(f"PULSOS EXACTOS POR 1 VUELTA: {pulsos_por_vuelta}")
    print("------------------")
    print(f"-> En tu código 'vuelta_perfecta.py', pon PULSOS_OBJETIVO = {int(pulsos_por_vuelta)}")
