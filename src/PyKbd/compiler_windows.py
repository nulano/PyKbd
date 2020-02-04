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
from io import BytesIO, StringIO

from .compiler import struct

STRUCT_PE_FILE = 'pefile'
STRUCT_PE_SECTION = 'pefile_section'


@dataclass(eq=False, frozen=True)
class Architecture:
    """
    Stores Architecture-dependant values for Windows builds

    :ivar pointer: sizeof(PTR)
    :ivar long_pointer: sizeof(LPTR)
    :ivar base: image base
    :ivar suffix: dll file suffix
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


def _win_int(wrapped):
    @struct
    class WinInt:
        value: int

        def write(self, stream: BytesIO, **kwargs):
            stream.write(self.value.to_bytes(wrapped.size, 'little', signed=wrapped.signed))

        @classmethod
        def read(cls, stream: BytesIO, **kwargs):
            data = stream.read(wrapped.size)
            if len(data) != wrapped.size:
                raise EOFError
            return cls(int.from_bytes(data, 'little', signed=wrapped.signed))

    WinInt.__name__ = wrapped.__name__
    WinInt.__qualname__ = wrapped.__qualname__
    return WinInt


# BYTE, WORD, DWORD, QWORD

@_win_int
class BYTE:
    size = 1
    signed = False


@_win_int
class WORD:
    size = 2
    signed = False


@_win_int
class DWORD:
    size = 4
    signed = False


@_win_int
class QWORD:
    size = 8
    signed = False


# CHAR, SHORT, INT, LONG, LONGLONG

@_win_int
class CHAR:
    size = 1
    signed = True


@_win_int
class SHORT:
    size = 2
    signed = True


@_win_int
class INT:
    size = 4
    signed = True


@_win_int
class LONG:
    size = 4
    signed = True


@_win_int
class LONGLONG:
    size = 8
    signed = True


# UCHAR, USHORT, UINT, ULONG, ULONGLONG

@_win_int
class UCHAR:
    size = 1
    signed = False


@_win_int
class USHORT:
    size = 2
    signed = False


@_win_int
class UINT:
    size = 4
    signed = False


@_win_int
class ULONG:
    size = 4
    signed = False


@_win_int
class ULONGLONG:
    size = 8
    signed = False


# MAKELONG, STR, WSTR, WCHAR

@struct
class MAKELONG:
    low: WORD
    high: WORD


@struct
class STR:
    text: str

    def write(self, stream: BytesIO, **kwargs):
        stream.write((self.text + '\0').encode('ascii'))

    @classmethod
    def read(cls, stream: BytesIO, **kwargs):
        out = StringIO()
        while True:
            next = stream.read(1).decode('ascii')
            if next == '\0':
                break
            if len(next) == 0:
                raise EOFError
            out.write(next)
        return cls(out.getvalue())


@struct
class WSTR:
    text: str

    def write(self, stream: BytesIO, **kwargs):
        stream.write((self.text + '\0').encode('utf-16le'))

    @classmethod
    def read(cls, stream: BytesIO, **kwargs):
        out = StringIO()
        while True:
            next = stream.read(2).decode('utf-16le')
            if next == '\0':
                break
            if len(next) == 0:
                raise EOFError
            out.write(next)
        return cls(out.getvalue())


@struct
class WCHAR:
    value: str

    def write(self, stream: BytesIO, **kwargs):
        if len(self.value) != 1:
            raise ValueError('char must have length 1')
        stream.write(self.value.encode('utf-16le'))

    @classmethod
    def read(cls, stream: BytesIO, **kwargs):
        value = stream.read(2).decode('utf-16le')
        if len(value) == 0:
            raise EOFError
        return cls(value)
