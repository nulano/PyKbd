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
