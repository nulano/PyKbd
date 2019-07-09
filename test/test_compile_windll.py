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
from typing import Union, Sequence

from pytest import fixture

from PyKbd.wintypes import *
from PyKbd.linker_binary import BinaryObject
from PyKbd.compile_windll import WinDll


def match_object(pattern: Sequence[Union[bytes, str]], object: BinaryObject):
    offset = 0

    values = []

    for i, token in enumerate(pattern):
        if isinstance(token, str):
            match = re.match(r'^\s*([^() ]+)\(\s*([?=*&])\s*\)\s*$', token)
            assert match is not None, "token %i: %s" % (i, token)
            length, op = int(match.group(1), 0), match.group(2)
            assert offset + length <= len(object.data)
            if op == '?':
                pass
            elif op == '=':
                values.append(object.data[offset : offset + length])
            elif op == '&':
                values.append(dereference_rva(object, offset))
            elif op == '*':
                values.append(dereference_ptr(object, offset))
            else:
                raise NotImplementedError
            offset += length
        else:
            assert offset + len(token) <= len(object.data), "token %i: %s" % (i, token)
            assert token == object.data[offset : offset + len(token)], "token %i: %s" % (i, token)
            offset += len(token)

    assert offset == len(object.data), "unexpected extra data"

    return values


def dereference_rva(object: BinaryObject, offset: int) -> BinaryObject:
    assert isinstance(object.symbols[offset], RVA)
    return object.symbols[offset].target


def dereference_ptr(object: BinaryObject, offset: int) -> BinaryObject:
    assert isinstance(object.symbols[offset], PTR)
    return object.symbols[offset].target


@fixture
def layout():
    return object()


@fixture(params=[X86, WOW64, AMD64])
def windll(request, layout):
    return WinDll(layout, request.param)


def test_export_dir(windll: WinDll):
    windll.kbdtables = BinaryObject()
    windll.compile_export_dir()

    dll_name, addresses, names, ordinals = match_object((
        DWORD(0).data, DWORD(windll.timestamp).data,
        WORD(0).data * 2, "4(&)", DWORD(1).data * 3, "4(&)", "4(&)", "4(&)"
    ), windll.dir_export)

    assert STR(windll.filename).data == dll_name.data

    func, = match_object(("4(&)",), addresses)
    func_name, = match_object(("4(&)",), names)
    match_object((WORD(0).data,), ordinals)

    assert STR('KbdLayerDescriptor').data == func_name.data

    if windll.architecture == X86:
        assert windll.kbdtables == match_object((b'\xB8', "4(*)", b'\xC3'), func)[0]
    elif windll.architecture == WOW64:
        assert windll.kbdtables == match_object((b'\xB8', "4(*)", b'\x99\xC3'), func)[0]
    elif windll.architecture == AMD64:
        assert windll.kbdtables == match_object((b'\x48\xB8', "8(*)", b'\xC3'), func)[0]
