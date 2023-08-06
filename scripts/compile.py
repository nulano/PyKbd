import os
import sys

from PyKbd.compile_windll import WinDll
from PyKbd.layout import Layout
from PyKbd.wininf import generate_inf_file
from PyKbd.wintypes import X86, AMD64, WOW64

with open(sys.argv[1] + ".json", "r", encoding="utf-8") as f:
    data = f.read()

layout = Layout.from_json(data)

for arch in (X86, AMD64, WOW64):
    windll = WinDll(layout, arch)
    data = windll.compile()
    with open(sys.argv[1] + arch.suffix + ".dll", "wb") as f:
        f.write(data)
with open(sys.argv[1] + ".inf", "w", encoding="utf-8") as f:
    f.write(generate_inf_file(layout))
# TODO add quotes around path?
with open(sys.argv[1] + "_install.cmd", "w", encoding="utf-8") as f:
    f.write("%windir%\\Sysnative\\rundll32.exe setupapi,InstallHinfSection DefaultInstall 132 %~dp0" + sys.argv[1] + ".inf")
with open(sys.argv[1] + "_uninstall.cmd", "w", encoding="utf-8") as f:
    f.write("%windir%\\Sysnative\\rundll32.exe setupapi,InstallHinfSection DefaultUninstall 132 %~dp0" + sys.argv[1] + ".inf")
os.system(f"7zr a {sys.argv[1]}.7z {sys.argv[1]}.inf {sys.argv[1]}32.dll {sys.argv[1]}64.dll {sys.argv[1]}WW.dll {sys.argv[1]}_install.cmd -mx")
os.system(f"copy /b 7zS2.sfx + {sys.argv[1]}.7z {sys.argv[1]}.exe")
