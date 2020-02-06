
import sys
from time import sleep

from PyKbd.compile_windll import WinDll
from PyKbd.layout import Layout
from PyKbd.visualizer import draw_keyboard, ISO, draw_dead_keys

windll = WinDll(Layout("", "", "", (0, 0), "", {}, {}, {}), None)

with open(sys.argv[1], "rb") as f:
    windll.decompile(f.read())

draw_keyboard(windll.layout, ISO).show()
draw_dead_keys(windll.layout).show()
sleep(5)
