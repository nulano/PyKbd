# This file is part of PyKbd
#
# Copyright (C) 2019-2020  Nulano
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
from typing import Optional

from . import _version
from .linker_binary import Symbol, BinaryObject, BinaryObjectReader


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

    def read(self, reader: BinaryObjectReader, align: bool = True):
        return int.from_bytes(reader.read_bytes(self.bytes, alignment=self.bytes if align else None),
                              byteorder='little', signed=self.signed)


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


MAKELONG.read = lambda reader: (WORD.read(reader), WORD.read(reader))


def STR(text: str) -> BinaryObject:
    return BinaryObject((text + '\0').encode('ascii'), alignment=1)


def WSTR(text: str, align: bool = True) -> BinaryObject:
    return BinaryObject((text + '\0').encode('utf-16le'), alignment=2 if align else None)


def _WSTR_read(reader: BinaryObjectReader, align: bool = True) -> str:
    data = bytearray()
    while True:
        char = reader.read_bytes(2, alignment=2 if align else None)
        if char == b"\0\0":
            break
        data.extend(char)
    return data.decode('utf-16le')


WSTR.read = _WSTR_read


# def CHAR(char: str) -> BinaryObject:
#     if len(char) != 1:
#         raise ValueError("char must have length 1")
#     return BinaryObject(char.encode('ascii'))


def WCHAR(char: str) -> BinaryObject:
    # TODO check for UCS-2 range
    if len(char) != 1:
        raise ValueError("char must have length 1")
    return BinaryObject(char.encode('utf-16le'))


WCHAR.read = lambda reader, align=True: reader.read_bytes(2, alignment=2 if align else None).decode('utf-16le')


@dataclass(frozen=True)
class PTR(Symbol):
    """
    .. highlight:: c
    Windows pointer symbol::

        typedef void *equivalent_type;
    """
    target: Optional[BinaryObject]
    architecture: Architecture
    align: bool = True

    # override order of parameters
    def __init__(self, architecture: Architecture, target: Optional[BinaryObject], align: bool = True):
        super().__init__(target)
        object.__setattr__(self, 'architecture', architecture)
        object.__setattr__(self, 'align', align)

    def __call__(self) -> BinaryObject:
        alignment = self.architecture.pointer if self.align else None
        offset = (self.architecture.base + (self.target.find_placement() or (None, 0))[1]) \
            if self.target is not None else 0
        data = offset.to_bytes(self.architecture.pointer, byteorder='little', signed=False)
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
    target: Optional[BinaryObject]
    architecture: Architecture
    align: bool = True

    # override order of parameters
    def __init__(self, architecture: Architecture, target: Optional[BinaryObject], align: bool = True):
        super().__init__(target)
        object.__setattr__(self, 'architecture', architecture)
        object.__setattr__(self, 'align', align)

    def __call__(self) -> BinaryObject:
        alignment = self.architecture.long_pointer if self.align else None
        offset = (self.architecture.base + (self.target.find_placement() or (None, 0))[1]) \
            if self.target is not None else 0
        data = offset.to_bytes(self.architecture.long_pointer, byteorder='little', signed=False)
        return BinaryObject(data, alignment=alignment)

    @staticmethod
    def read(reader: BinaryObjectReader, architecture: Architecture, align: bool = True):
        alignment = architecture.long_pointer if align else None
        data = reader.read_bytes(architecture.long_pointer, alignment=alignment)
        return int.from_bytes(data, byteorder='little', signed=False)


@dataclass(frozen=True)
class RVA(Symbol):
    """
    Windows RVA (relative virtual address) symbol

    Essentially a 32-bit pointer without the image base offset
    """
    target: Optional[BinaryObject]
    align: bool = True

    def __call__(self) -> BinaryObject:
        alignment = 4 if self.align else None
        offset = (self.target.find_placement() or (None, 0))[1] if self.target is not None else 0
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
