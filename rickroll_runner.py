import os
import time
from ascii_rickroll import Rickroll

FLAG = "terminado.flag"

if os.path.exists(FLAG):
    os.remove(FLAG)

roller = Rickroll()

# Reproducir en loop hasta que aparezca el flag
try:
    while not os.path.exists(FLAG):
        roller.play()  # una pasada completa
except KeyboardInterrupt:
    pass

print("\n✅ Proceso finalizado")
time.sleep(2)