from MotorDriver import MotorDriver
from gpiozero import RotaryEncoder
import time

# --- CONSTANTES MAESTRAS CALIBRADAS ---
PULSOS_POR_VUELTA = 1473.15  # Ajustado para corregir el último medio cm
POTENCIA_CRUCERO = 80        # Velocidad rápida
POTENCIA_APROXIMACION = 30   # Velocidad de precisión
OFFSET_FRENADO = 55          # Pulsos de inercia a potencia 30
UMBRAL_DESACELERACION = 3000 # 2 vueltas antes de llegar, frenamos

# --- CONFIGURACIÓN DE HARDWARE ---
# Motor A (Izquierdo) -> MA | Encoder D16 (16, 17)
enc_a = RotaryEncoder(16, 17, max_steps=0)
# Motor B (Derecho)   -> MB | Encoder D5 (5, 6)
enc_b = RotaryEncoder(5, 6, max_steps=0)

driver = MotorDriver()

def avanzar(vueltas):
    objetivo = int(vueltas * PULSOS_POR_VUELTA)
    punto_lento = objetivo - UMBRAL_DESACELERACION
    punto_stop = objetivo - OFFSET_FRENADO
    
    print(f"\n=== MOVIMIENTO DUAL: {vueltas} VUELTAS ===")
    print(f"Objetivo: {objetivo} pulsos.")

    # Reseteamos contadores
    enc_a.steps = 0
    enc_b.steps = 0
    
    # Arrancamos motores (DIRECCIONES ENFRENTADAS)
    # Si el robot va hacia atrás, cambia 'forward' por 'backward' en ambos
    driver.MotorRun(0, 'forward', POTENCIA_CRUCERO)
    driver.MotorRun(1, 'backward', POTENCIA_CRUCERO)
    
    # Estados de control
    corriendo_a = True
    corriendo_b = True
    lento_a = False
    lento_b = False

    while corriendo_a or corriendo_b:
        pasos_a = abs(enc_a.steps)
        pasos_b = abs(enc_b.steps)

        # --- LÓGICA MOTOR A ---
        if corriendo_a:
            if pasos_a >= punto_lento and not lento_a:
                driver.MotorRun(0, 'forward', POTENCIA_APROXIMACION)
                lento_a = True
            if pasos_a >= punto_stop:
                driver.MotorStop(0)
                corriendo_a = False

        # --- LÓGICA MOTOR B ---
        if corriendo_b:
            if pasos_b >= punto_lento and not lento_b:
                driver.MotorRun(1, 'backward', POTENCIA_APROXIMACION)
                lento_b = True
            if pasos_b >= punto_stop:
                driver.MotorStop(1)
                corriendo_b = False

        # Mostrar progreso
        print(f"A: {pasos_a}/{objetivo} | B: {pasos_b}/{objetivo}    ", end="\r")
        time.sleep(0.001)

    print(f"\n--- LLEGADA: A:{abs(enc_a.steps)} | B:{abs(enc_b.steps)} ---")

try:
    # Prueba con 10 vueltas para verificar simetría y marca
    avanzar(10.0)

except KeyboardInterrupt:
    driver.MotorStop(0)
    driver.MotorStop(1)
