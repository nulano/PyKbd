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

from pytest import raises

from PyKbd.linker_binary import BinaryObject, link, Symbol


@dataclass(frozen=True)
class _TestSymbol(Symbol):
    target: BinaryObject
    value: int = 0

    def __call__(self, address: int) -> bytes:
        return (address ^ self.value).to_bytes(1, 'little')


def test_link_single():
    a = BinaryObject(b'\xAA')
    out = link([a])

    assert isinstance(out, BinaryObject)
    assert b'\xAA' == bytes(out.data)
    assert {} == out.symbols

    assert a.placement == (out, 0)


def test_link_two():
    a = BinaryObject(b'\xAA')
    b = BinaryObject(b'\xBB')
    out = link([a, b])

    assert b'\xAA\xBB' == out.data
    assert (out, 0) == a.placement
    assert (out, 1) == b.placement


def test_link_base():
    a = BinaryObject(b'\xAA')
    b = BinaryObject(b'\xBB')
    symbol = _TestSymbol(b, 0x33)
    a.append(symbol)
    out = link([a, b], base=0xCC)

    assert b'\xAA\xFD\xBB' == out.data
    assert {1: symbol} == a.symbols
    assert (out, 2) == b.placement


def test_link_self_ref():
    obj = BinaryObject()
    symb = _TestSymbol(obj, 0xAA)
    obj.append(symb)
    out = link([obj])

    assert b'\xAA' == out.data
    assert {0: symb} == out.symbols

    obj = BinaryObject(b'\x33')
    symb = _TestSymbol(obj, 0xAA)
    obj.append(symb)
    out = link([obj])

    assert b'\x33\xAA' == out.data
    assert {1: symb} == out.symbols


def test_link_find_ref():
    b = BinaryObject(b'\xCC')
    b_symbol = _TestSymbol(b, 0xAA)
    a = BinaryObject(b'\x33')
    a.append(b_symbol)
    out = link([a])

    assert b'\x33\xA8\xCC' == out.data
    assert {1: b_symbol}
    assert (out, 0) == a.placement
    assert (out, 2) == b.placement


def test_append():
    a = BinaryObject(b'\xAA')

    a.append(b'\xBB')

    c = _TestSymbol(a, 0xCC)
    a.append(c)

    d = BinaryObject(b'\xDD')
    a.append(d)

    # symbols are undefined until linking is done
    a.data[2] = 0xCC

    assert b'\xAA\xBB\xCC\xDD' == a.data
    assert {2: c} == a.symbols


# noinspection PyTypeChecker
def test_append_invalid():
    a = BinaryObject()
    with raises(TypeError):
        a.append(None)
    with raises(TypeError):
        a.append([])


def test_append_linked():
    a = BinaryObject()
    out = link([a])
    with raises(ValueError):
        a.append(b'')


def test_append_padding():
    a = BinaryObject(b'\xAA', alignment=8)
    a.append_padding(4)
    assert b'\xAA\0\0\0' == a.data
    a.append_padding(8)
    assert b'\xAA\0\0\0\0\0\0\0' == a.data
    with raises(ValueError):
        a.append_padding(16)


def test_find_placement():
    # +---+-------------------+
    # | A | B +---+-----------+
    # |   |   | C | D +---+---+
    # |   |   |   |   | E | F |
    # +---+---+---+---+---+---+

    a = BinaryObject(b'\xAA')
    b = BinaryObject(b'\xBB')
    c = BinaryObject(b'\xCC')
    d = BinaryObject(b'\xDD')
    e = BinaryObject(b'\xEE')
    f = BinaryObject(b'\xFF')

    d.append(e)
    d.append(f)

    b.append(c)
    b.append(d)

    out = link([a, b])

    assert (b, 1) == c.placement
    assert (b, 2) == d.placement
    assert (d, 1) == e.placement
    assert (d, 2) == f.placement
    assert (out, 0) == a.placement
    assert (out, 1) == b.placement

    assert (out, 0) == a.find_placement()
    assert (out, 1) == b.find_placement()
    assert (out, 2) == c.find_placement()
    assert (out, 3) == d.find_placement()
    assert (out, 4) == e.find_placement()
    assert (out, 5) == f.find_placement()

    assert b'\xAA\xBB\xCC\xDD\xEE\xFF' == out.data


def test_link_alignment():
    a = BinaryObject(b'\xAA', alignment=4)
    b = BinaryObject(b'\xBB\xBB', alignment=4)
    c = BinaryObject(b'\xCC\xCC\xCC', alignment=4)
    d = BinaryObject(b'\xDD\xDD\xDD\xDD', alignment=4)
    e = BinaryObject(b'\xEE', alignment=4)
    f = BinaryObject(b'\xFF', alignment=2)
    out = link([a, b, c, d, e, f])

    assert b'\xAA\x00\x00\x00' \
           b'\xBB\xBB\x00\x00' \
           b'\xCC\xCC\xCC\x00' \
           b'\xDD\xDD\xDD\xDD' \
           b'\xEE\x00\xFF' == out.data

    assert 4 == out.alignment


def test_alignment():
    a = BinaryObject(alignment=4)
    b = BinaryObject(alignment=2)
    a.append(b)

    assert 4 == a.alignment
    assert (a, 0) == b.placement


def test_alignment_invalid():
    with raises(ValueError):
        BinaryObject(alignment=0)
    with raises(ValueError):
        BinaryObject(alignment=-1)

    a = BinaryObject(alignment=1)
    b = BinaryObject(alignment=2)
    with raises(ValueError):
        a.append(b)
