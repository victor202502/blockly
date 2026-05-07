from MotorDriver import MotorDriver
from gpiozero import RotaryEncoder
import time

# --- AJUSTES DE ALTA VELOCIDAD ---
PULSOS_POR_VUELTA = 1473.0   # Ajustado un pelín al alza por ese cm que faltaba
POTENCIA_ALTA = 100           # Velocidad de crucero
POTENCIA_BAJA = 30           # Velocidad de aproximación final
OFFSET_FRENADO = 53          # Tu inercia medida a potencia 30
UMBRAL_LENTO = 600          # Pulsos antes del final para empezar a frenar (aprox 2 vueltas)

NUMERO_MOTOR = 0             
encoder = RotaryEncoder(16, 17, max_steps=0)
driver = MotorDriver()

def girar_100_vueltas_rapido():
    objetivo = int(10 * PULSOS_POR_VUELTA)
    punto_lento = objetivo - UMBRAL_LENTO
    punto_corte = objetivo - OFFSET_FRENADO
    
    print(f"=== TEST 100 VUELTAS A POTENCIA {POTENCIA_ALTA} ===")
    print(f"Objetivo: {objetivo} pulsos. ¡Arrancamos!")
    
    encoder.steps = 0
    driver.MotorRun(NUMERO_MOTOR, 'forward', POTENCIA_ALTA)
    
    en_modo_lento = False
    
    while abs(encoder.steps) < punto_corte:
        actual = abs(encoder.steps)
        
        # Lógica de desaceleración
        if actual >= punto_lento and not en_modo_lento:
            driver.MotorRun(NUMERO_MOTOR, 'forward', POTENCIA_BAJA)
            en_modo_lento = True
            print(f"\n[!] Cerca del objetivo. Reduciendo a potencia {POTENCIA_BAJA}...")

        # Print de progreso cada 1000 pulsos para no saturar la CPU
        if actual % 1000 == 0:
            print(f"Progreso: {actual} / {objetivo}    ", end="\r")
        
        time.sleep(0.0001)

    # Parada final
    driver.MotorStop(NUMERO_MOTOR)
    time.sleep(2.0)
    
    posicion_final = abs(encoder.steps)
    print(f"\n--- RESULTADO FINAL ---")
    print(f"Pulsos finales: {posicion_final}")
    print(f"Diferencia: {posicion_final - objetivo} pulsos.")

try:
    girar_100_vueltas_rapido()

except KeyboardInterrupt:
    driver.MotorStop(NUMERO_MOTOR)
