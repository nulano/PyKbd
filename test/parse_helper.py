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

import re
from typing import Union, Iterable

from PyKbd.linker_binary import BinaryObject
from PyKbd.wintypes import PTR, LPTR, RVA, Architecture


def match_object(pattern: Iterable[Union[bytes, str]], object: BinaryObject):
    """
    Verifies that object matches the pattern and returns extracted values.

    Supported tokens:

    ==========  ==========================  ==========
    Token       Matches                     Returns
    ==========  ==========================  ==========
    *bytes*     token exactly
    4(0)        4 bytes equal 0
    4(?)        4 bytes
    4(=)        4 bytes                     bytes
    4(+)        4 bytes                     unsigned int
    4(-)        4 bytes                     signed int
    4(*)        4 byte PTR symbol           symbol.target
    4($)        4 byte LPTR symbol          symbol.target
    4(&)        4 byte RVA symbol           symbol.target
    !4(?)       align to 4 bytes
    <                                       offset
    >                                       length - offset
    ~           rest of input
    ==========  ==========================  ==========
    :param pattern: sequence of tokens
    :param object: object being tested
    :return: list of converted values matched for tokens
    """
    offset = 0

    values = []

    for i, token in enumerate(pattern):
        if isinstance(token, str):
            if token == '~':
                return values
            elif token == '<':
                values.append(offset)
                continue
            elif token == '>':
                values.append(len(object.data) - offset)
                continue

            match = re.match(r'^\s*(!?)\s*([x\d]+)\(\s*(?:([?=+\-*$&])|([x\d]+))\s*\)\s*$', token)
            assert match is not None, "invalid token %i: %s" % (i, token)

            align, length, op = match.group(1) == '!', int(match.group(2), 0), match.group(3)

            if align:
                length = (-offset) % length

            assert offset + length <= len(object.data)
            value = object.data[offset : offset + length]

            if op is None:
                assert bytes([int(match.group(4), 0)] * length) == value
            elif op == '?':
                pass
            elif op == '=':
                values.append(value)
            elif op == '+':
                values.append(int.from_bytes(value, 'little', signed=False))
            elif op == '-':
                values.append(int.from_bytes(value, 'little', signed=True))
            elif op == '*':
                symbol = object.symbols[offset]
                assert isinstance(symbol, PTR)
                values.append(symbol.target)
            elif op == '$':
                symbol = object.symbols[offset]
                assert isinstance(symbol, LPTR)
                values.append(symbol.target)
            elif op == '&':
                symbol = object.symbols[offset]
                assert isinstance(symbol, RVA)
                values.append(symbol.target)
            else:
                raise NotImplementedError
            offset += length
        else:
            assert offset + len(token) <= len(object.data), "token %i (%s), offset 0x%x" % (i, token, offset)
            value = object.data[offset : offset + len(token)]

            assert token == value, "token %i (%s) != offset 0x%x (%s)" % (i, token, offset, value)
            offset += len(token)

    assert offset == len(object.data), "unexpected extra 0x%x bytes, offset 0x%x" % (len(object.data) - offset, offset)

    return values


def token_ptr(architecture: Architecture):
    return '%i(*)' % architecture.pointer


def token_lptr(architecture: Architecture):
    return '%i($)' % architecture.long_pointer
