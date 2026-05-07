import asyncio
import os
import subprocess
import time
from bless import (
    BlessServer,
    BlessGATTCharacteristic,
    GATTCharacteristicProperties,
    GATTAttributePermissions
)

SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
CHARACTERISTIC_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

class SpikeServer:
    def __init__(self):
        self.code_buffer = ""
        self.current_process = None

    def kill_script(self):
        # 1. Parar el proceso de Python si está corriendo
        if self.current_process and self.current_process.poll() is None:
            self.current_process.terminate()
            try:
                self.current_process.wait(timeout=1)
            except:
                self.current_process.kill()

        os.system("pkill -f temp_run.py")

        # 2. Apagar los motores de forma aislada para no bloquear la placa
        os.system("python3 -c 'from MotorDriver import MotorDriver; d=MotorDriver(); d.MotorStop(0); d.MotorStop(1)'")

        # 3. PAUSA DE SEGURIDAD (Esto es lo que arregla tu problema de la rueda)
        time.sleep(0.3)

    def on_write(self, characteristic: BlessGATTCharacteristic, value: bytearray):
        try:
            data = value.decode("utf-8")

            if data == "==START==":
                self.code_buffer = ""
            elif data == "==END==":
                print(f"\n[OK] Código listo ({len(self.code_buffer)} bytes). Ejecutando...")
                self.execute_code()
            elif data == "STOP":
                print("\n[!] BOTON STOP PRESIONADO")
                self.kill_script()
            else:
                self.code_buffer += data
        except Exception as e:
            print(f"Error BLE: {e}")

    def execute_code(self):
        self.kill_script()
        with open("temp_run.py", "w") as f:
            f.write(self.code_buffer)

        # EL TRUCO DEL -u ESTÁ EN ESTA LÍNEA (Unbuffered mode)
        self.current_process = subprocess.Popen(["python3", "-u", "temp_run.py"])

async def run_server():
    spike = SpikeServer()
    server = BlessServer(name="SpikePi-Robot")

    await server.add_new_service(SERVICE_UUID)
    await server.add_new_characteristic(
        SERVICE_UUID, CHARACTERISTIC_UUID,
        GATTCharacteristicProperties.write | GATTCharacteristicProperties.write_without_response | GATTCharacteristicProperties.read,
        None, GATTAttributePermissions.readable | GATTAttributePermissions.writeable
    )

    server.write_request_func = spike.on_write
    await server.start()
    print("------------------------------------------")
    print(" SERVIDOR BLUETOOTH (MODO SEGURO) ACTIVO")
    print("------------------------------------------")

    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\nServidor cerrado correctamente. ¡Hasta luego!")
