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

from ..layout import *

layout = Layout(
    "English (US) Layout",
    "Nulano",
    "Unknown",
    (1, 0),
    "kbdus.dll",
    {
        ScanCode(0x01): KeyCode('ESCAPE', 0x1B),
        ScanCode(0x02): KeyCode('1', ord('1')),
        ScanCode(0x03): KeyCode('2', ord('2')),
        ScanCode(0x04): KeyCode('3', ord('3')),
        ScanCode(0x05): KeyCode('4', ord('4')),
        ScanCode(0x06): KeyCode('5', ord('5')),
        ScanCode(0x07): KeyCode('6', ord('6')),
        ScanCode(0x08): KeyCode('7', ord('7')),
        ScanCode(0x09): KeyCode('8', ord('8')),
        ScanCode(0x0A): KeyCode('9', ord('9')),
        ScanCode(0x0B): KeyCode('0', ord('0')),
        ScanCode(0x0C): KeyCode('OEM_MINUS', 0xBD),
        ScanCode(0x0D): KeyCode('OEM_PLUS', 0xBB),
        ScanCode(0x0E): KeyCode('BACK', 0x08),
        ScanCode(0x0F): KeyCode('TAB', 0x09),
        ScanCode(0x10): KeyCode('Q', ord('Q')),
        ScanCode(0x11): KeyCode('W', ord('W')),
        ScanCode(0x12): KeyCode('E', ord('E')),
        ScanCode(0x13): KeyCode('R', ord('R')),
        ScanCode(0x14): KeyCode('T', ord('T')),
        ScanCode(0x15): KeyCode('Y', ord('Y')),
        ScanCode(0x16): KeyCode('U', ord('U')),
        ScanCode(0x17): KeyCode('I', ord('I')),
        ScanCode(0x18): KeyCode('O', ord('O')),
        ScanCode(0x19): KeyCode('P', ord('P')),

    }
)
