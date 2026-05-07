from MotorDriver import MotorDriver
from gpiozero import RotaryEncoder
import time

# --- INICIALIZAR HARDWARE ---
driver = MotorDriver()
enc_a = RotaryEncoder(16, 17, max_steps=0)
enc_b = RotaryEncoder(5, 6, max_steps=0)

POTENCIA = 50   # <--- REDUCIDO AL 50%
TIEMPO = 10.0

print("===============================================")
print("  TEST DE ESTRÉS - MITAD DE VELOCIDAD (50%)    ")
print("===============================================")
print("⚠️ ATENCIÓN: Levanta el robot o ponlo boca arriba.")
print("Las ruedas girarán a MITAD DE POTENCIA durante 30s.")
print("Iniciando en 5 segundos...\n")
time.sleep(5)

# --- PRUEBA 1: SOLO MOTOR A ---
print("[1/3] Probando SOLO Motor A (10 segundos)...")
enc_a.steps = 0
enc_b.steps = 0
driver.MotorRun(0, 'forward', POTENCIA)
time.sleep(TIEMPO)
driver.MotorStop(0)

pulsos_A_solo = abs(enc_a.steps)
print(f" -> Resultado: {pulsos_A_solo} pulsos.\n")
time.sleep(2)  # Descanso

# --- PRUEBA 2: SOLO MOTOR B ---
print("[2/3] Probando SOLO Motor B (10 segundos)...")
enc_a.steps = 0
enc_b.steps = 0
driver.MotorRun(1, 'forward', POTENCIA)
time.sleep(TIEMPO)
driver.MotorStop(1)

pulsos_B_solo = abs(enc_b.steps)
print(f" -> Resultado: {pulsos_B_solo} pulsos.\n")
time.sleep(2)  # Descanso

# --- PRUEBA 3: AMBOS MOTORES ---
print("[3/3] Probando AMBOS MOTORES A LA VEZ (10 segundos)...")
enc_a.steps = 0
enc_b.steps = 0
driver.MotorRun(0, 'forward', POTENCIA)
driver.MotorRun(1, 'forward', POTENCIA)
time.sleep(TIEMPO)
driver.MotorStop(0)
driver.MotorStop(1)

pulsos_A_juntos = abs(enc_a.steps)
pulsos_B_juntos = abs(enc_b.steps)
print(f" -> Resultado Motor A: {pulsos_A_juntos} pulsos.")
print(f" -> Resultado Motor B: {pulsos_B_juntos} pulsos.\n")

# --- INFORME FINAL ---
print("===============================================")
print("                 INFORME FINAL                 ")
print("===============================================")

if pulsos_A_solo > 0 and pulsos_B_solo > 0:
    perdida_A = pulsos_A_solo - pulsos_A_juntos
    porcentaje_A = (perdida_A / pulsos_A_solo) * 100
    
    perdida_B = pulsos_B_solo - pulsos_B_juntos
    porcentaje_B = (perdida_B / pulsos_B_solo) * 100

    print(f"Motor A - Pulsos leídos solo:   {pulsos_A_solo}")
    print(f"Motor A - Pulsos leídos juntos: {pulsos_A_juntos}")
    print(f"⚠️ PÉRDIDA MOTOR A: {perdida_A} pulsos ({porcentaje_A:.2f}% menos)\n")

    print(f"Motor B - Pulsos leídos solo:   {pulsos_B_solo}")
    print(f"Motor B - Pulsos leídos juntos: {pulsos_B_juntos}")
    print(f"⚠️ PÉRDIDA MOTOR B: {perdida_B} pulsos ({porcentaje_B:.2f}% menos)")
else:
    print("Error: Uno de los motores no ha registrado pulsos.")

print("===============================================")
