
import sys

from PyKbd.compile_windll import WinDll
from PyKbd.layout import Layout
from PyKbd.visualizer import draw_keyboard, ISO, draw_dead_keys

windll = WinDll()

with open(sys.argv[1], "rb") as f:
    windll.decompile(f.read())

draw_keyboard(windll.layout, ISO).show()
draw_dead_keys(windll.layout).show()
json = windll.layout.to_json()
assert Layout.from_json(json) == windll.layout
print(json)
