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
from dataclasses import dataclass, field, fields, is_dataclass
import json
from functools import partial
from typing import Tuple, Dict, Mapping, Collection, List, Optional, Union

from . import _version


__version__ = _version


def _asdict(obj):
    if is_dataclass(obj):
        if hasattr(obj, "to_string"):
            return getattr(obj, "to_string")()
        else:
            return {fld.name: _asdict(getattr(obj, fld.name))
                    for fld in fields(obj)
                    if getattr(obj, fld.name) != fld.default}
    elif isinstance(obj, Mapping):
        return {_asdict(k): _asdict(v) for k, v in obj.items()}
    elif isinstance(obj, Collection) and not isinstance(obj, str) and not isinstance(obj, bytes):
        return [_asdict(v) for v in obj]
    else:
        return obj


# noinspection PyUnresolvedReferences
def _fromdict(cls, data):
    generic_class = getattr(cls, '__origin__', cls)
    if generic_class == Union:
        if len(cls.__args__) != 2 or not issubclass(cls.__args__[1], type(None)):
            raise TypeError("unknown type: " + cls)
        if data is None:
            return None
        cls = cls.__args__[0]
        generic_class = getattr(cls, '__origin__', cls)
    if is_dataclass(cls) and isinstance(data, str):
        return cls.from_string(data)
    elif is_dataclass(cls) and isinstance(data, dict):
        return cls(**{fld.name: _fromdict(fld.type, data.get(fld.name, fld.default)) for fld in fields(cls)})
    elif issubclass(generic_class, Dict) and isinstance(data, dict):
        kt, vt = cls.__args__
        return dict((_fromdict(kt, k), _fromdict(vt, v)) for k, v in data.items())
    elif issubclass(generic_class, List) and isinstance(data, list):
        return list(_fromdict(tp, data[i]) for i, tp in enumerate(cls.__args__))
    elif issubclass(generic_class, Tuple) and isinstance(data, list):
        return tuple(_fromdict(tp, data[i]) for i, tp in enumerate(cls.__args__))
    elif isinstance(data, generic_class):
        return data
    elif issubclass(cls, type(0)) and isinstance(data, str):
        return int(data, 10)
    else:
        raise TypeError("can't convert %s to %s" % (str(type(data)), str(cls)))


def _flags(bits: Optional[Collection[str]] = None):
    def _impl(_bits, cls):
        _bits = _bits or [fld.name for fld in fields(cls)]

        def to_string(self):
            return ','.join(fld.name for fld in fields(self) if getattr(self, fld.name) != fld.default) or 'default'

        @staticmethod
        def from_string(string):
            if string == 'default':
                return cls()
            invert = string.split(',')
            return cls(**{fld.name: not fld.default for fld in fields(cls) if fld.name in invert})

        def to_bits(self):
            invert = [fld.name for fld in fields(self) if getattr(self, fld.name) != fld.default]
            return sum((1 << i) for i, name in enumerate(_bits) if name in invert)

        @staticmethod
        def from_bits(value):
            invert = [fld for i, fld in enumerate(_bits) if (value >> i) & 1]
            return cls(**{fld.name: not fld.default for fld in fields(cls) if fld.name in invert})

        cls.to_string = to_string
        cls.from_string = from_string
        cls.to_bits = to_bits
        cls.from_bits = from_bits
        return cls

    return partial(_impl, bits)


@dataclass(frozen=True)
class ScanCode:
    code: int
    prefix: int = 0

    def to_string(self):
        if self.prefix != 0:
            return "%X,%X" % (self.prefix, self.code)
        else:
            return "%X" % self.code

    @classmethod
    def from_string(cls, string):
        if ',' in string:
            return cls(*reversed([int(v, 16) for v in string.split(',')]))
        else:
            return cls(int(string, 16))


@_flags()
@dataclass(frozen=True)
class KeyAttributes:
    capslock: bool = False
    capslock_secondary: bool = False  # sgcaps
    capslock_altgr: bool = False
    kanalock: bool = False


@dataclass(frozen=True)
class KeyCode:
    win_vk: int
    name: Optional[str] = None
    attributes: KeyAttributes = KeyAttributes()

    @staticmethod
    def translate_vk(vk: int):
        return {
            # drop KBDEXT for VK_DIVIDE and VK_CANCEL
            0x16F: 0x6F, 0x103: 0x03,
            # drop KBDSPECIAL for VK_MULTIPLY if present
            # note: KBDSPECIAL is preserved for special keys without characters
            0x26A: 0x6A,
            # apply KBDNUMPAD | KBDSPECIAL translation to VK_NUMPAD* and VK_DECIMAL
            0xC24: 0x67, 0xC26: 0x68, 0xC21: 0x69,
            0xC25: 0x64, 0xC0C: 0x65, 0xC27: 0x66,
            0xC23: 0x61, 0xC28: 0x62, 0xC22: 0x63,
            0xC2D: 0x60, 0xC2E: 0x6E,
        }.get(vk, vk)

    @staticmethod
    def untranslate_vk(vk: int):
        return {
            # add KBDEXT to VK_DIVIDE and VK_CANCEL
            0x6F: 0x16F, 0x03: 0x103,
            # add KBDSPECIAL to VK_MULTIPLY
            0x6A: 0x26A,
            # translate VK_NUMPAD* and VK_DECIMAL to KBDNUMPAD | KBDSPECIAL navigation keys
            0x67: 0xC24, 0x68: 0xC26, 0x69: 0xC21,
            0x64: 0xC25, 0x65: 0xC0C, 0x66: 0xC27,
            0x61: 0xC23, 0x62: 0xC28, 0x63: 0xC22,
            0x60: 0xC2D, 0x6E: 0xC2E,
        }.get(vk, vk)


@_flags(['shift', 'control', 'alt', 'kana'])
@dataclass(frozen=True)
class ShiftState:
    shift: bool = False
    control: bool = False
    alt: bool = False
    kana: bool = False
    capslock: bool = False  # only compatible with shift, conflicts with WCH_DEAD


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
    name: str = ""
    author: str = ""
    copyright: str = ""
    version: Tuple[int, int] = (0, 0)
    dll_name: str = ""

    # VSC -> virtual key name (+ attrib)
    keymap: Dict[ScanCode, KeyCode] = field(default_factory=dict)
    # virtual key -> (modifiers -> char (+ attrib))
    charmap: Dict[int, Dict[ShiftState, Character]] = field(default_factory=dict)
    # dead char -> (char -> char (+ attrib)) (+ attrib)
    deadkeys: Dict[str, DeadKey] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(_asdict(self), sort_keys=True)

    @classmethod
    def from_json(cls, string):
        return _fromdict(cls, json.loads(string))
