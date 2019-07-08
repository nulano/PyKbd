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
from typing import Union, Dict, Optional, Sequence, Tuple


@dataclass(frozen=True)
class Symbol:
    target: BinaryObject

    def __call__(self, address: int) -> Union[bytes, BinaryObject]:
        raise NotImplementedError


class BinaryObject:
    data: bytearray
    alignment: int
    symbols: Dict[int, Symbol]
    placement: Optional[Tuple[BinaryObject, int]]

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
            template = value(0)
            if isinstance(template, BinaryObject):
                self.append_padding(template.alignment)
                template = template.data
            self.symbols[len(self.data)] = value
            self.data.extend(template)

        elif isinstance(value, BinaryObject):
            if value.placement is not None:
                raise ValueError('value has been placed in another object')

            self.append_padding(value.alignment)
            value.placement = (self, len(self.data))
            self.data.extend(value.data)
            for offset, symbol in value.symbols.items():
                self.symbols[value.placement[1] + offset] = symbol

        else:
            raise TypeError(value)

    def find_placement(self) -> Optional[Tuple[BinaryObject, int]]:
        if self.placement is None:
            return None
        target, address = self, 0
        while target.placement is not None:
            target, offset = target.placement
            address += offset
        return target, address


def link(objects: Sequence[BinaryObject], base: int = 0) -> BinaryObject:
    out = BinaryObject()

    seen = set()
    queue = deque([x for x in objects if x not in seen and (seen.add(x) or True)])

    while len(queue) > 0:
        obj = queue.popleft()
        out.alignment *= obj.alignment // gcd(out.alignment, obj.alignment)
        out.append(obj)
        for offset, symbol in obj.symbols.items():
            if symbol.target not in seen:
                seen.add(symbol.target)
                queue.append(symbol.target)

    for offset, symbol in out.symbols.items():
        value = symbol(base + symbol.target.find_placement()[1])
        out.data[offset: offset + len(value)] = value

    return out
