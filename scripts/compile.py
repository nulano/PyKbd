import os
import sys

from PyKbd.compile_windll import WinDll
from PyKbd.crc16 import crc16xmodem
from PyKbd.layout import Layout
from PyKbd.wininf import generate_inf_file, generate_inf_launcher
from PyKbd.wintypes import X86, AMD64, WOW64

with open(sys.argv[1] + ".json", "r", encoding="utf-8") as f:
    data = f.read()

layout = Layout.from_json(data)

# keep in sync with compile_windll, wininf, TODO refactor this
revision = crc16xmodem(layout.to_json())
name = f"{layout.name} {layout.version[0]}.{layout.version[1]} ({revision})"
print(f"Compiling {name}...")

for arch in (X86, AMD64, WOW64):
    windll = WinDll(layout, arch)
    data = windll.compile()
    with open(sys.argv[1] + arch.suffix + ".dll", "wb") as f:
        f.write(data)
with open(sys.argv[1] + ".inf", "w", encoding="utf-8") as f:
    f.write(generate_inf_file(layout))
# TODO add quotes around path?
with open(sys.argv[1] + "_install.cmd", "w", encoding="utf-8") as f:
    f.write(generate_inf_launcher(sys.argv[1] + ".inf"))
with open(sys.argv[1] + "_uninstall.cmd", "w", encoding="utf-8") as f:
    f.write(generate_inf_launcher(sys.argv[1] + ".inf", uninstall=True))
os.system(f"7zr a {sys.argv[1]}.7z {sys.argv[1]}.inf {sys.argv[1]}32.dll {sys.argv[1]}64.dll {sys.argv[1]}WW.dll {sys.argv[1]}_install.cmd -mx")
os.system(f"copy /b 7zS2.sfx + {sys.argv[1]}.7z {sys.argv[1]}.exe")
