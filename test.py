from pyboy import PyBoy
from pyboy.utils import WindowEvent

pyboy = PyBoy('pokemon_red.gb',
              # window="OpenGL",
              log_level="DEBUG"
              )
while pyboy.tick():
    pass
pyboy.stop()
