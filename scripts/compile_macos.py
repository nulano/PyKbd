
import sys

from PyKbd.layout import Layout
from PyKbd.macos import compiler

with open(sys.argv[1] + ".json", "r", encoding="utf-8") as f:
    data = f.read()

layout = Layout.from_json(data)

with open(sys.argv[1] + ".keylayout", "w", encoding="utf-8") as f:
    text = compiler.compile_keylayout(layout)
    f.write(text)
