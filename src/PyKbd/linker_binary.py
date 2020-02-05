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

from __future__ import annotations

from math import gcd
from collections import deque
from dataclasses import dataclass
from typing import Optional, Union, Tuple, Iterable, Dict
from warnings import warn

from . import _version


__version__ = _version


@dataclass(frozen=True)
class Symbol:
    target: Optional[BinaryObject]

    def __call__(self) -> BinaryObject:
        raise NotImplementedError


class BinaryObject:
    data: bytearray
    alignment: int
    symbols: Dict[int, Symbol]
    placement: Optional[Tuple[Optional[BinaryObject], int]]

    def __init__(self, data: bytes = (), alignment: Optional[int] = None):
        if alignment is None:
            alignment = 1
        if alignment < 1:
            raise ValueError('alignment cannot be negative')

        self.data = bytearray(data)
        self.alignment = alignment
        self.symbols = {}
        self.placement = None

    def append_padding(self, alignment):
        if self.alignment % alignment != 0:
            raise ValueError('invalid padding alignment %i for object with alignment %i'
                             % (alignment, self.alignment))
        self.data.extend(bytes((alignment - len(self.data)) % alignment))

    def append(self, value: Union[bytes, Symbol, BinaryObject]):
        if self.placement is not None:
            raise ValueError('this object has already been placed into another object')

        if isinstance(value, bytes):
            self.data.extend(value)

        elif isinstance(value, Symbol):
            template = value()
            self.append_padding(template.alignment)
            self.symbols[len(self.data)] = value
            self.data.extend(template.data)

        elif isinstance(value, BinaryObject):
            if value.placement is not None:
                raise ValueError('value has been placed in another object')
            if self == value:
                raise ValueError('value must not be self')

            self.append_padding(value.alignment)
            value.placement = (self, len(self.data))
            self.data.extend(value.data)
            for offset, symbol in value.symbols.items():
                self.symbols[value.placement[1] + offset] = symbol

        else:
            raise TypeError(value)

    def extend(self, values: Iterable[Union[bytes, Symbol, BinaryObject]]):
        for value in values:
            self.append(value)

    def find_placement(self) -> Optional[Tuple[Optional[BinaryObject], int]]:
        if self.placement is None:
            return None
        target, address = self, 0
        while target is not None and target.placement is not None:
            target, offset = target.placement
            address += offset
        return target, address


class BinaryObjectReader:
    target: BinaryObject
    offset: int

    def __init__(self, target: BinaryObject):
        assert target is not None
        self.target = target
        self.offset = 0

    def read_padding(self, alignment):
        if self.target.alignment % alignment != 0:
            raise ValueError('invalid padding alignment %i for object with alignment %i'
                             % (alignment, self.target.alignment))
        self.offset += (alignment - self.offset) % alignment

    def read_bytes(self, length, alignment=0):
        if alignment is not None and alignment > 0:
            self.read_padding(alignment)
        if self.offset + length > len(self.target.data):
            raise IOError("end of stream")
        data = self.target.data[self.offset : self.offset + length]
        self.offset += length
        return data

    def read_or_warn(self, object: Union[bytes, BinaryObject], category=RuntimeWarning, message="read object differs"):
        alignment = 0
        if isinstance(object, bytes):
            target = object
        elif isinstance(object, BinaryObject):
            target = object.data
            alignment = object.alignment
        else:
            raise ValueError("invalid target object")

        data = self.read_bytes(len(target), alignment)
        if data != target:
            warn(message, category, stacklevel=2)

    def read_or_fail(self, object: Union[bytes, BinaryObject], category=IOError, message="read object differs"):
        alignment = 0
        if isinstance(object, bytes):
            target = object
        elif isinstance(object, BinaryObject):
            target = object.data
            alignment = object.alignment
        else:
            raise ValueError("invalid target object")

        data = self.read_bytes(len(target), alignment)
        if data != target:
            raise category(message)


def link(objects: Iterable[BinaryObject], base: int = 0) -> BinaryObject:
    out = BinaryObject()

    seen = {out}
    queue = deque([x for x in objects if x not in seen and (seen.add(x) or True)])

    while len(queue) > 0:
        obj = queue.popleft()
        out.alignment *= obj.alignment // gcd(out.alignment, obj.alignment)
        out.append(obj)
        for offset, symbol in obj.symbols.items():
            target = symbol.target
            if target is not None and target.placement is not None:
                target = target.find_placement()[0]
            if target is not None and target not in seen:
                seen.add(target)
                queue.append(target)

    out.placement = (None, base)

    for offset, symbol in out.symbols.items():
        value = symbol()
        if isinstance(value, BinaryObject):
            value = value.data
        out.data[offset: offset + len(value)] = value

    return out
