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

from dataclasses import dataclass
from typing import Tuple, Dict

from . import _version


__version__ = _version


@dataclass(frozen=True)
class ScanCode:
    code: int
    prefix: int = 0


@dataclass(frozen=True)
class KeyCode:
    name: str
    win_vk: int


@dataclass(frozen=True)
class ShiftState:
    shift: bool = False
    control: bool = False
    alt: bool = False
    kana: bool = False

    def to_win_mask(self):
        mask = 0
        if self.shift:
            mask |= 1
        if self.control:
            mask |= 2
        if self.alt:
            mask |= 4
        if self.kana:
            mask |= 8
        return mask

    @classmethod
    def from_win_mask(cls, mask: int):
        return cls(mask & 1 != 0, mask & 2 != 0, mask & 4 != 0, mask & 8 != 0)


@dataclass(frozen=True)
class Character:
    char: str
    dead: bool = False


@dataclass(frozen=True)
class DeadKey:
    name: str
    charmap: Dict[str, Character]


@dataclass
class Layout:
    name: str
    author: str
    copyright: str
    version: Tuple[int, int]
    dll_name: str

    keymap: Dict[ScanCode, KeyCode]
    charmap: Dict[KeyCode, Dict[ShiftState, Character]]
    deadkeys: Dict[str, DeadKey]
