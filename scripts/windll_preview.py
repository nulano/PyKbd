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

import sys
import unicodedata

from PyKbd.compile_windll import WinDll
from PyKbd.layout import Layout
from PyKbd.visualizer import draw_keyboard, ISO, draw_dead_keys, draw_dead_keys_tree, how_to_type

windll = WinDll()

with open(sys.argv[1], "rb") as f:
    windll.decompile(f.read())


def show(im, suffix):
    if len(sys.argv) >= 3:
        im.save(f"{sys.argv[2]}_{suffix}.png")
    else:
        im.show()


show(draw_keyboard(windll.layout, ISO), "main")
for dead, dead_key in windll.layout.deadkeys.items():
    if dead_key.name == dead:
        name = unicodedata.name(dead)
    else:
        name = dead_key.name
    name = name.replace(" ", "_")
    show(draw_keyboard(windll.layout, ISO, dead), f"dead_{name}")
# draw_dead_keys(windll.layout).show()
json = windll.layout.to_json()
assert Layout.from_json(json) == windll.layout
print(json)
print(draw_dead_keys_tree(windll.layout))
howto = how_to_type(windll.layout)
print(len(howto))
