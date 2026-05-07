from MotorDriver import MotorDriver
import pigpio
import time
import sys

# --- NUEVO MOTOR DE LECTURA POR HARDWARE (DMA) ---
class PigpioEncoder:
    def __init__(self, pi, pin_a, pin_b):
        self.pi = pi
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.pos = 0
        
        self.pi.set_mode(pin_a, pigpio.INPUT)
        self.pi.set_mode(pin_b, pigpio.INPUT)
        self.pi.set_pull_up_down(pin_a, pigpio.PUD_UP)
        self.pi.set_pull_up_down(pin_b, pigpio.PUD_UP)
        
        self.levA = self.pi.read(pin_a)
        self.levB = self.pi.read(pin_b)
        
        self.cbA = self.pi.callback(pin_a, pigpio.EITHER_EDGE, self._cb)
        self.cbB = self.pi.callback(pin_b, pigpio.EITHER_EDGE, self._cb)

    def _cb(self, gpio, level, tick):
        if level == pigpio.TIMEOUT: return
        if gpio == self.pin_a:
            self.levA = level
            if level == self.levB: self.pos += 1
            else: self.pos -= 1
        else:
            self.levB = level
            if level != self.levA: self.pos += 1
            else: self.pos -= 1
            
    @property
    def steps(self):
        return self.pos
        
    @steps.setter
    def steps(self, value):
        self.pos = value

# --- INICIALIZAR ---
print("Conectando con el demonio pigpio...")
pi = pigpio.pi()
if not pi.connected:
    print("Error: No se pudo conectar a pigpio. Asegúrate de ejecutar 'sudo systemctl start pigpiod'")
    sys.exit()

driver = MotorDriver()
enc_a = PigpioEncoder(pi, 16, 17)
enc_b = PigpioEncoder(pi, 5, 6)

POTENCIA = 100   # <--- VOLVEMOS A VELOCIDAD MÁXIMA
TIEMPO = 10.0

print("===============================================")
print("  TEST ESTRÉS PIGPIO - MÁXIMA VELOCIDAD (100)  ")
print("===============================================")
print("⚠️ ATENCIÓN: Levanta el robot o ponlo boca arriba.")
print("Las ruedas girarán a MÁXIMA POTENCIA durante 30s.")
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
time.sleep(2)

# --- PRUEBA 2: SOLO MOTOR B ---
print("[2/3] Probando SOLO Motor B (10 segundos)...")
enc_a.steps = 0
enc_b.steps = 0
driver.MotorRun(1, 'forward', POTENCIA)
time.sleep(TIEMPO)
driver.MotorStop(1)

pulsos_B_solo = abs(enc_b.steps)
print(f" -> Resultado: {pulsos_B_solo} pulsos.\n")
time.sleep(2)

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
pi.stop()
