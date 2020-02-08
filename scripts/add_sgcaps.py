# This file is part of PyKbd
#
# Copyright (C) 2019  Nulano
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import dataclasses
import sys
from time import sleep

from PyKbd.compile_windll import WinDll
from PyKbd.visualizer import draw_keyboard, ISO


windll = WinDll()

with open(sys.argv[1], "rb") as f:
    windll.decompile(f.read())
    layout = windll.layout

print(layout.to_json())

vks = (0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30, 0xDB, 0xDD, 0xBA, 0xDC)

# add SGCAPS attribute
layout.keymap = {
    scancode: dataclasses.replace(keycode, attributes=
        dataclasses.replace(keycode.attributes, capslock_secondary=keycode.win_vk in vks))
    for scancode, keycode in layout.keymap.items()
}
for vk in vks:
    # add SGCAPS entries
    layout.charmap[vk].update({
        dataclasses.replace(shiftstate, capslock=True): dataclasses.replace(character, char=character.char.upper())
        for shiftstate, character in layout.charmap[vk].items()
    })
    # conflicts with dead keys :(
    layout.charmap[vk] = {shiftstate: dataclasses.replace(character, dead=False)
                          for shiftstate, character in layout.charmap[vk].items()}

print(layout.to_json())

with open(sys.argv[2], "wb") as f:
    f.write(windll.compile())

# show decompiled output as reference
windll.decompile(windll.assembly.data)
draw_keyboard(layout, ISO).show()
