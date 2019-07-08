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

from typing import Callable, Tuple, Sequence

from pytest import raises

from PyKbd.wintypes import *


# helpers for int types

def check_valid(func: Callable[[int], BinaryObject], values: Sequence[Tuple[int, bytes]]):
    for value, target in values:
        returned = func(value)
        assert target == returned.data, "for value %x" % value
        assert len(target) == returned.alignment, "for value %x" % value


def check_overflow(func: Callable[[int], BinaryObject], values: Sequence[int]):
    for value in values:
        with raises(OverflowError):
            func(value)


# first check all unsigned int types


def test_byte():
    check_valid(BYTE, ((0, b'\x00'), (0xAB, b'\xAB'), (0xFF, b'\xFF')))
    check_overflow(BYTE, (-1, 0x100))


def test_uchar():
    check_valid(UCHAR, ((0, b'\x00'), (0xAB, b'\xAB'), (0xFF, b'\xFF')))
    check_overflow(UCHAR, (-1, 0x100))


def test_word():
    check_valid(WORD, ((0, b'\x00\x00'), (0xABCD, b'\xCD\xAB'), (0xFFFF, b'\xFF\xFF')))
    check_overflow(WORD, (-1, 0x10000))


def test_ushort():
    check_valid(USHORT, ((0, b'\x00\x00'), (0xABCD, b'\xCD\xAB'), (0xFFFF, b'\xFF\xFF')))
    check_overflow(USHORT, (-1, 0x10000))


def test_dword():
    check_valid(DWORD, (
        (0, b'\x00\x00\x00\x00'),
        (0x89ABCDEF, b'\xEF\xCD\xAB\x89'),
        (0xFFFFFFFF, b'\xFF\xFF\xFF\xFF')))
    check_overflow(DWORD, (-1, 0x100000000))


def test_uint():
    check_valid(UINT, (
        (0, b'\x00\x00\x00\x00'), (0x89ABCDEF, b'\xEF\xCD\xAB\x89'), (0xFFFFFFFF, b'\xFF\xFF\xFF\xFF'))
    )
    check_overflow(UINT, (-1, 0x100000000))


def test_ulong():
    check_valid(ULONG, (
        (0, b'\x00\x00\x00\x00'), (0x89ABCDEF, b'\xEF\xCD\xAB\x89'), (0xFFFFFFFF, b'\xFF\xFF\xFF\xFF'))
    )
    check_overflow(ULONG, (-1, 0x100000000))


def test_qword():
    check_valid(QWORD, (
        (0, b'\x00\x00\x00\x00\x00\x00\x00\x00'),
        (0x89ABCDEF01234567, b'\x67\x45\x23\x01\xEF\xCD\xAB\x89'),
        (0xFFFFFFFFFFFFFFFF, b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'))
    )
    check_overflow(QWORD, (-1, 0x10000000000000000))


def test_ulonglong():
    check_valid(ULONGLONG, (
        (0, b'\x00\x00\x00\x00\x00\x00\x00\x00'),
        (0x89ABCDEF01234567, b'\x67\x45\x23\x01\xEF\xCD\xAB\x89'),
        (0xFFFFFFFFFFFFFFFF, b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'))
    )
    check_overflow(ULONGLONG, (-1, 0x10000000000000000))


# then check all signed int types


def test_char():
    check_valid(CHAR, ((0, b'\x00'), (0x6B, b'\x6B'), (0x7F, b'\x7F'), (-0x80, b'\x80')))
    check_overflow(CHAR, (-0x81, 0x80))


def test_short():
    check_valid(SHORT, ((0, b'\x00\x00'), (0x6BCD, b'\xCD\x6B'), (0x7FFF, b'\xFF\x7F'), (-0x8000, b'\x00\x80')))
    check_overflow(SHORT, (-0x8001, 0x8000))


def test_int():
    check_valid(INT, (
        (0x00000000, b'\x00\x00\x00\x00'),
        (0x69ABCDEF, b'\xEF\xCD\xAB\x69'),
        (0x7FFFFFFF, b'\xFF\xFF\xFF\x7F'),
        (-0x80000000, b'\x00\x00\x00\x80'),
    ))
    check_overflow(INT, (-0x80000001, 0x80000000))


def test_long():
    check_valid(LONG, (
        (0x00000000, b'\x00\x00\x00\x00'),
        (0x69ABCDEF, b'\xEF\xCD\xAB\x69'),
        (0x7FFFFFFF, b'\xFF\xFF\xFF\x7F'),
        (-0x80000000, b'\x00\x00\x00\x80'),
    ))
    check_overflow(LONG, (-0x80000001, 0x80000000))


def test_longlong():
    check_valid(LONGLONG, (
        (0x0000000000000000, b'\x00\x00\x00\x00\x00\x00\x00\x00'),
        (0x69ABCDEF01234567, b'\x67\x45\x23\x01\xEF\xCD\xAB\x69'),
        (0x7FFFFFFFFFFFFFFF, b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x7F'),
        (-0x8000000000000000, b'\x00\x00\x00\x00\x00\x00\x00\x80'),
    ))
    check_overflow(LONGLONG, (-0x8000000000000001, 0x8000000000000000))


# now check other types

def test_str():
    assert b"Hello World!\0" == STR("Hello World!").data
    with raises(ValueError):
        STR("\xAA")


def test_wstr():
    assert b"T\0e\0s\0t\0\0\0" == WSTR("Test").data
    assert b"\x61\x01\x70\x00\x65\x00\x09\x01\x69\x00\xe4\x00\x6c\x00\x20\x00" \
           b"\x63\x00\x68\x00\xe2\x00\x72\x00\xe3\x00\xe7\x00\x74\x00\xe9\x00\x72\x00\x73\x00\x00\x00" \
           == WSTR("špeĉiäl chârãçtérs").data

# TODO PTR, RVA

# TODO test arch
