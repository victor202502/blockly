from MotorDriver import MotorDriver
import pigpio
import time
import sys
import signal

class PigpioEncoder:
    def __init__(self, pi, pin_a, pin_b):
        self.pi = pi; self.pin_a = pin_a; self.pin_b = pin_b; self.pos = 0
        self.pi.set_mode(pin_a, pigpio.INPUT); self.pi.set_mode(pin_b, pigpio.INPUT)
        self.pi.set_pull_up_down(pin_a, pigpio.PUD_UP); self.pi.set_pull_up_down(pin_b, pigpio.PUD_UP)
        self.levA = self.pi.read(pin_a); self.levB = self.pi.read(pin_b)
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
            
    def cancelar(self):
        # Libera la memoria del sensor en pigpio
        self.cbA.cancel()
        self.cbB.cancel()
        
    @property
    def steps(self): return self.pos

# Inicialización global
pi = pigpio.pi()
if not pi.connected: sys.exit("Error pigpio")
driver = MotorDriver()
enc_a = PigpioEncoder(pi, 16, 17)
enc_b = PigpioEncoder(pi, 5, 6)

PULSOS_POR_VUELTA = 5892.0  
GIRO_180_VUELTAS = 1.19  
POT_MIN = 25

def get_distancia(): return 999 
def map_speed(s): return int(30 + (s - 1) * (70 / 9))

def robot_dual_maestro(dir, valor, modo, spike_speed):
    p_base = map_speed(spike_speed)
    da = 'forward' if dir == 'forward' else 'backward'
    db = 'backward' if dir == 'forward' else 'forward'
    if modo == 'SEG':
        driver.MotorRun(0, da, p_base); driver.MotorRun(1, db, p_base)
        time.sleep(valor); driver.MotorStop(0); driver.MotorStop(1); return
    ini_a, ini_b = enc_a.steps, enc_b.steps
    objetivo = int(valor * PULSOS_POR_VUELTA)
    driver.MotorRun(0, da, p_base); driver.MotorRun(1, db, p_base)
    while True:
        pa, pb = abs(enc_a.steps - ini_a), abs(enc_b.steps - ini_b)
        if (objetivo - max(pa, pb)) <= 0: break
        diff = pa - pb
        corr = int(diff * 0.05) 
        driver.MotorRun(0, da, max(min(p_base - corr, 100), POT_MIN))
        driver.MotorRun(1, db, max(min(p_base + corr, 100), POT_MIN))
        time.sleep(0.01)
    driver.MotorStop(0); driver.MotorStop(1)

def robot_girar_maestro(sentido, grados, speed):
    p_base = map_speed(speed)
    da = 'backward' if sentido == 'derecha' else 'forward'
    db = 'backward' if sentido == 'derecha' else 'forward'
    ini_a, ini_b = enc_a.steps, enc_b.steps
    objetivo = int((grados * (GIRO_180_VUELTAS / 180.0)) * PULSOS_POR_VUELTA)
    driver.MotorRun(0, da, p_base); driver.MotorRun(1, db, p_base)
    while abs(enc_a.steps - ini_a) < objetivo: time.sleep(0.01)
    driver.MotorStop(0); driver.MotorStop(1)

def robot_motor_maestro(id, dir, valor, modo, spike_speed):
    p_max = map_speed(spike_speed)
    if modo == 'SEG':
        driver.MotorRun(id, dir, p_max); time.sleep(valor); driver.MotorStop(id); return
    ini = enc_a.steps if id == 0 else enc_b.steps
    obj = int(valor * PULSOS_POR_VUELTA)
    driver.MotorRun(id, dir, p_max)
    while abs((enc_a.steps if id == 0 else enc_b.steps) - ini) < obj: time.sleep(0.01)
    driver.MotorStop(id)

def motor_grados(id_motor):
    enc = enc_a if id_motor == 0 else enc_b
    return int((enc.steps / PULSOS_POR_VUELTA) * 360)

def motor_vueltas(id_motor):
    enc = enc_a if id_motor == 0 else enc_b
    return round(enc.steps / PULSOS_POR_VUELTA, 2)

def reset_motor(id_motor):
    enc = enc_a if id_motor == 0 else enc_b
    enc.pos = 0

# --- EL SISTEMA DE RESCATE (TESTAMENTO) ---
def apagar_todo(sig=None, frame=None):
    try:
        driver.MotorStop(0)
        driver.MotorStop(1)
        enc_a.cancelar()
        enc_b.cancelar()
        pi.stop()
    except:
        pass
    # Si la función fue llamada por un asesinato (señal de Linux), salimos limpios
    if sig is not None:
        sys.exit(0)

# Enganchamos nuestra función de rescate a las señales de "muerte" de Linux
signal.signal(signal.SIGTERM, apagar_todo)
signal.signal(signal.SIGINT, apagar_todo)
