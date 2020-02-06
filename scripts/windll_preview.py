
import sys

from PyKbd.compile_windll import WinDll
from PyKbd.layout import Layout
from PyKbd.visualizer import draw_keyboard, ISO

windll = WinDll(Layout("", "", "", (0, 0), "", {}, {}, {}), None)

with open(sys.argv[1], "rb") as f:
    windll.decompile(f.read())

draw_keyboard(windll.layout, ISO).show()
