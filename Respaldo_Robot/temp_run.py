from spike_pro import *

try:
    for count in range(1000):
      print(motor_vueltas(1))
      time.sleep(0.2)

finally:
    apagar_todo()
    print("FINISHED")