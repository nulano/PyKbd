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
from typing import Tuple, Dict, Mapping, Collection, List

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
    else:
        raise TypeError("can't convert %s to %s" % (str(type(data)), str(cls)))


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

    def to_string(self):
        return ','.join([fld.name for fld in fields(self) if getattr(self, fld.name)]) or 'default'

    @classmethod
    def from_string(cls, string):
        if string == 'default':
            return cls()
        else:
            return cls(**{v: True for v in string.split(',')})


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
    # virtual key name -> (modifiers -> char (+ attrib))
    charmap: Dict[str, Dict[ShiftState, Character]] = field(default_factory=dict)
    # dead char -> (char -> char (+ attrib)) (+ attrib)
    deadkeys: Dict[str, DeadKey] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(_asdict(self), sort_keys=True)

    @classmethod
    def from_json(cls, string):
        return _fromdict(cls, json.loads(string))
