
import sys

from PyKbd.compile_windll import WinDll
from PyKbd.layout import Layout
from PyKbd.wintypes import X86, AMD64, WOW64

with open(sys.argv[1] + ".json", "r", encoding="utf-8") as f:
    data = f.read()

layout = Layout.from_json(data)

for arch in (X86, AMD64, WOW64):
    windll = WinDll(layout, arch)
    data = windll.compile()
    with open(sys.argv[1] + arch.suffix + ".dll", "wb") as f:
        f.write(data)
