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

from . import _version
from .linker_binary import Symbol, BinaryObject


__version__ = _version


@dataclass(eq=False, frozen=True)
class Architecture:
    """
    Stores Architecture-dependant values for Windows builds

    :ivar pointer: sizeof(PTR)
    :ivar long_pointer: sizeof(LPTR)
    :ivar base: image base
    :ivar name: name
    """
    pointer: int
    long_pointer: int
    base: int
    suffix: str
    name: str

    def __str__(self):
        return self.name


X86 = Architecture(4, 4, 0x00005FFF0000, '32', 'Windows-x86')
WOW64 = Architecture(4, 8, 0x00005FFE0000, 'WW', 'Windows-WoW64')
AMD64 = Architecture(8, 8, 0x001800000000, '64', 'Windows-amd64')


@dataclass(frozen=True)
class _WinInt:
    bytes: int
    signed: bool

    def __call__(self, value: int, align: bool = True):
        return BinaryObject(value.to_bytes(self.bytes, byteorder='little', signed=self.signed),
                            alignment=self.bytes if align else None)


BYTE = _WinInt(1, signed=False)
WORD = _WinInt(2, signed=False)
DWORD = _WinInt(4, signed=False)
QWORD = _WinInt(8, signed=False)

CHAR = _WinInt(1, signed=True)
SHORT = _WinInt(2, signed=True)
INT = _WinInt(4, signed=True)
LONG = _WinInt(4, signed=True)
LONGLONG = _WinInt(8, signed=True)

UCHAR = _WinInt(1, signed=False)
USHORT = _WinInt(2, signed=False)
UINT = _WinInt(4, signed=False)
ULONG = _WinInt(4, signed=False)
ULONGLONG = _WinInt(8, signed=False)


@dataclass(frozen=True)
class _WinIntPtr:
    signed: bool

    def __call__(self, architecture: Architecture):
        return {
            (4, False): DWORD,
            (4, True ): LONG,
            (8, False): QWORD,
            (8, True ): LONGLONG
        }[architecture.pointer, self.signed]


DWORD_PTR = _WinIntPtr(signed=False)
UINT_PTR = _WinIntPtr(signed=False)
ULONG_PTR = _WinIntPtr(signed=False)

INT_PTR = _WinIntPtr(signed=True)
LONG_PTR = _WinIntPtr(signed=True)


def MAKELONG(low: int, high: int):
    long = BinaryObject(alignment=4)
    long.append(WORD(low))
    long.append(WORD(high))
    return long


def STR(text: str) -> BinaryObject:
    return BinaryObject((text + '\0').encode('ascii'))


def WSTR(text: str) -> BinaryObject:
    return BinaryObject((text + '\0').encode('utf-16le'))


@dataclass(frozen=True)
class PTR(Symbol):
    """
    .. highlight:: c
    Windows pointer symbol::

        typedef void *equivalent_type;
    """
    target: BinaryObject
    architecture: Architecture
    align: bool = True

    def __call__(self) -> BinaryObject:
        alignment = self.architecture.pointer if self.align else None
        data = (self.architecture.base + (self.target.find_placement() or (None, 0))[1]) \
            .to_bytes(self.architecture.pointer, byteorder='little', signed=False)
        return BinaryObject(data, alignment=alignment)


@dataclass(frozen=True)
class LPTR(Symbol):
    """
    .. highlight:: c
    Windows long pointer symbol::

        #if defined(BUILD_WOW6432)
            #define KBD_LONG_POINTER __ptr64
        #else
            #define KBD_LONG_POINTER
        #endif
        typedef void *KBD_LONG_POINTER equivalent_type;
    """
    target: BinaryObject
    architecture: Architecture
    align: bool = True

    def __call__(self) -> BinaryObject:
        alignment = self.architecture.long_pointer if self.align else None
        data = (self.architecture.base + (self.target.find_placement() or (None, 0))[1]) \
            .to_bytes(self.architecture.long_pointer, byteorder='little', signed=False)
        return BinaryObject(data, alignment=alignment)


@dataclass(frozen=True)
class RVA(Symbol):
    """
    Windows RVA (relative virtual address) symbol

    Essentially a 32-bit pointer without the image base offset
    """
    target: BinaryObject
    align: bool = True

    def __call__(self) -> BinaryObject:
        alignment = 4 if self.align else None
        offset = (self.target.find_placement() or (None, 0))[1]
        return BinaryObject(offset.to_bytes(4, byteorder='little', signed=False), alignment=alignment)


@dataclass(frozen=True)
class SIZEOF(Symbol):
    target: BinaryObject
    type: _WinInt
    align: bool = True

    # override order of parameters
    def __init__(self, type: _WinInt, target: BinaryObject, align: bool = True):
        super().__init__(target)
        object.__setattr__(self, 'type', type)
        object.__setattr__(self, 'align', align)

    def __call__(self) -> BinaryObject:
        return self.type(len(self.target.data), align=self.align)
