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

from typing import Callable, Iterable, Tuple

from pytest import raises, mark

from PyKbd.wintypes import *


# helpers for int types

def check_valid(func: Callable[[int], BinaryObject], values: Iterable[Tuple[int, bytes]]):
    for value, target in values:
        returned = func(value)
        assert target == returned.data, "for value %x" % value
        assert len(target) == returned.alignment, "for value %x" % value
    for value, target in values:
        returned = func(value, False)
        assert target == returned.data, "for value %x" % value
        assert 1 == returned.alignment, "for value %x" % value


def check_overflow(func: Callable[[int], BinaryObject], values: Iterable[int]):
    for value in values:
        with raises(OverflowError):
            func(value)


# first check all unsigned int types


@mark.parametrize("type", (UCHAR, BYTE), ids=("UCHAR", "BYTE"))
def test_uint8(type):
    check_valid(type, ((0, b'\x00'), (0xAB, b'\xAB'), (0xFF, b'\xFF')))
    check_overflow(type, (-1, 0x100))


@mark.parametrize("type", (USHORT, WORD), ids=("USHORT", "WORD"))
def test_uint16(type):
    check_valid(type, ((0, b'\x00\x00'), (0xABCD, b'\xCD\xAB'), (0xFFFF, b'\xFF\xFF')))
    check_overflow(type, (-1, 0x10000))


@mark.parametrize("type", (
        UINT, ULONG, DWORD,
        UINT_PTR(X86), ULONG_PTR(X86), DWORD_PTR(X86),
        UINT_PTR(WOW64), ULONG_PTR(WOW64), DWORD_PTR(WOW64)
), ids=(
        "UINT", "ULONG", "DWORD",
        "UINT_PTR(X86)", "ULONG_PTR(X86)", "DWORD_PTR(X86)",
        "UINT_PTR(WOW64)", "ULONG_PTR(WOW64)", "DWORD_PTR(WOW64)"
))
def test_uint32(type):
    check_valid(type, (
        (0x00000000, b'\x00\x00\x00\x00'),
        (0x89ABCDEF, b'\xEF\xCD\xAB\x89'),
        (0xFFFFFFFF, b'\xFF\xFF\xFF\xFF'))
    )
    check_overflow(type, (-1, 0x100000000))


@mark.parametrize("type", (ULONGLONG, QWORD, UINT_PTR(AMD64), ULONG_PTR(AMD64), DWORD_PTR(AMD64)),
                  ids=("ULONGLONG", "QWORD", "UINT_PTR(AMD64)", "ULONG_PTR(AMD64)", "DWORD_PTR(AMD64)"))
def test_uint64(type):
    check_valid(type, (
        (0x0000000000000000, b'\x00\x00\x00\x00\x00\x00\x00\x00'),
        (0x89ABCDEF01234567, b'\x67\x45\x23\x01\xEF\xCD\xAB\x89'),
        (0xFFFFFFFFFFFFFFFF, b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'))
    )
    check_overflow(type, (-1, 0x10000000000000000))


# then check all signed int types


@mark.parametrize("type", (CHAR,), ids=("CHAR",))
def test_int8(type):
    check_valid(type, ((0, b'\x00'), (0x6B, b'\x6B'), (0x7F, b'\x7F'), (-0x80, b'\x80')))
    check_overflow(type, (-0x81, 0x80))


@mark.parametrize("type", (SHORT,), ids=("SHORT",))
def test_int16(type):
    check_valid(type, ((0, b'\x00\x00'), (0x6BCD, b'\xCD\x6B'), (0x7FFF, b'\xFF\x7F'), (-0x8000, b'\x00\x80')))
    check_overflow(type, (-0x8001, 0x8000))


@mark.parametrize("type", (INT, LONG, INT_PTR(X86), LONG_PTR(X86), INT_PTR(WOW64), LONG_PTR(WOW64)),
                  ids=("INT", "LONG", "INT_PTR(X86)", "LONG_PTR(X86)", "INT_PTR(WOW64)", "LONG_PTR(WOW64)"))
def test_int32(type):
    check_valid(type, (
        (0x00000000, b'\x00\x00\x00\x00'),
        (0x69ABCDEF, b'\xEF\xCD\xAB\x69'),
        (0x7FFFFFFF, b'\xFF\xFF\xFF\x7F'),
        (-0x80000000, b'\x00\x00\x00\x80'),
    ))
    check_overflow(type, (-0x80000001, 0x80000000))


@mark.parametrize("type", (LONGLONG, INT_PTR(AMD64), LONG_PTR(AMD64)),
                  ids=("LONGLONG", "INT_PTR(AMD64)", "LONG_PTR(AMD64)"))
def test_int64(type):
    check_valid(type, (
        (0x0000000000000000, b'\x00\x00\x00\x00\x00\x00\x00\x00'),
        (0x69ABCDEF01234567, b'\x67\x45\x23\x01\xEF\xCD\xAB\x69'),
        (0x7FFFFFFFFFFFFFFF, b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x7F'),
        (-0x8000000000000000, b'\x00\x00\x00\x00\x00\x00\x00\x80'),
    ))
    check_overflow(type, (-0x8000000000000001, 0x8000000000000000))


# now check other types

def test_makelong():
    for values, target in (
            ((0x0000, 0x0000), b'\x00\x00\x00\x00'),
            ((0xABCD, 0x9876), b'\xCD\xAB\x76\x98'),
            ((0xFFFF, 0xFFFF), b'\xFF\xFF\xFF\xFF'),
    ):
        returned = MAKELONG(*values)
        assert target == returned.data, "for values %x, %x" % values
        assert 4 == returned.alignment, "for values %x, %x" % values
    for values in ((-1, 0), (0, -1), (-1, -1), (0x10000, 0), (0, 0x10000), (0x10000, 0x10000)):
        with raises(OverflowError):
            MAKELONG(*values)


def test_str():
    assert b"Hello World!\0" == STR("Hello World!").data
    with raises(ValueError):
        STR("\xAA")


def test_wstr():
    assert b"T\0e\0s\0t\0\0\0" == WSTR("Test").data
    assert b"\x61\x01\x70\x00\x65\x00\x09\x01\x69\x00\xe4\x00\x6c\x00\x20\x00" \
           b"\x63\x00\x68\x00\xe2\x00\x72\x00\xe3\x00\xe7\x00\x74\x00\xe9\x00\x72\x00\x73\x00\x00\x00" \
           == WSTR("špeĉiäl chârãçtérs").data


# next check symbols

# TODO PTR, LPTR, RVA, SIZEOF
