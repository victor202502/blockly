import os
import subprocess
import time
from flask import Flask, request
from flask_cors import CORS
from MotorDriver import MotorDriver
app = Flask(name)
CORS(app)
Initialize the motor driver for emergency stops
driver = MotorDriver()
Variable to track the running process
current_process = None
def kill_running_script():
"""Stops the script and cuts power to motors immediately."""
global current_process

# 1. Kill the Python subprocess if it exists
if current_process and current_process.poll() is None:
    print("Stopping running script...")
    current_process.terminate()
    try:
        current_process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        current_process.kill()

# 2. Safety: Kill any orphaned scripts via system command
os.system("pkill -f temp_run.py")

# 3. PHYSICAL STOP: Set motor power to 0 directly on the HAT
print("EMERGENCY STOP: Cutting motor power.")
driver.MotorStop(0)
driver.MotorStop(1)
@app.route('/run', methods=['POST'])
def run_code():
global current_process
code
Code
# Before running new code, ensure the old one is dead
kill_running_script()
time.sleep(0.1)

data = request.json
code = data.get('code')

# Save the received code to the temp file
with open("temp_run.py", "w") as f:
    f.write(code)

try:
    print("Executing new code...")
    # Execute the script in the background
    current_process = subprocess.Popen(["python3", "temp_run.py"])
    return "Code started successfully"
except Exception as e:
    return f"Execution error: {str(e)}"
@app.route('/stop', methods=['POST'])
def stop_code():
"""Endpoint specifically for the Stop button."""
kill_running_script()
return "Robot stopped and power cut."
if name == 'main':
print("----------------------------------------------")
print(" SPIKE Pi Server - Active and Listening       ")
print(" IP Address: 0.0.0.0 | Port: 5000            ")
print("----------------------------------------------")
app.run(host='0.0.0.0', port=5000)
