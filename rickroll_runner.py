import os, time
from ascii_rickroll import Rickroll

FLAG = "terminado.flag"
if os.path.exists(FLAG):
    os.remove(FLAG)

roller = Rickroll()
try:
    while not os.path.exists(FLAG):
        roller.play()
except KeyboardInterrupt:
    pass