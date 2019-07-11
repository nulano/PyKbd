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

from operator import itemgetter
from warnings import warn

import pytest

from PyKbd.layout import Layout
from PyKbd.wintypes import *
from PyKbd.linker_binary import BinaryObject
from PyKbd.compile_windll import WinDll

from .parse_helper import match_object


@pytest.fixture(scope='module')
def layout():
    return Layout("Dummy Test Layout", "PyKbd", "Public Domain", (1, 0), "kbdtst.dll")


@pytest.fixture(scope='module', params=[X86, WOW64, AMD64], ids=["x86", "WoW64", "amd64"])
def windll(request, layout: Layout):
    return WinDll(layout, request.param)


def test_compile_tables(windll: WinDll):
    windll.compile_tables()

    warn('test not implemented')  # TODO

    assert isinstance(windll.kbdtables, BinaryObject)


def test_compile_dir_export(windll: WinDll):
    windll.compile_dir_export()

    dll_name, addresses, names, ordinals = match_object((
        DWORD(0).data, DWORD(windll.timestamp).data, WORD(0).data * 2,
        "4(&)", DWORD(1).data * 3, "4(&)", "4(&)", "4(&)", "~"
    ), windll.dir_export)

    assert dll_name.data == STR(windll.layout.dll_name).data

    func, = match_object(("4(&)",), addresses)
    func_name, = match_object(("4(&)",), names)
    match_object((WORD(0).data,), ordinals)

    assert func_name.data == STR('KbdLayerDescriptor').data

    for obj in (dll_name, addresses, names, ordinals, func_name):
        assert obj.placement[0] == windll.dir_export

    if windll.architecture == X86:
        assert match_object((b'\xB8', "4(*)", b'\xC3'), func)[0] == windll.kbdtables
    elif windll.architecture == WOW64:
        assert match_object((b'\xB8', "4(*)", b'\x99\xC3'), func)[0] == windll.kbdtables
    elif windll.architecture == AMD64:
        assert match_object((b'\x48\xB8', "8(*)", b'\xC3'), func)[0] == windll.kbdtables


def test_compile_dir_resource(windll: WinDll):
    windll.compile_dir_resource()

    info, info_len = match_object((
        DWORD(0).data * 3, WORD(0).data, WORD(1).data, DWORD(0x10).data, DWORD(0x80000018).data,
        DWORD(0).data * 3, WORD(0).data, WORD(1).data, DWORD(1).data, DWORD(0x80000030).data,
        DWORD(0).data * 3, WORD(0).data, WORD(1).data, DWORD(0x409).data, DWORD(0x48).data,
        "4(&)", "4(=)", DWORD(0).data * 2, "~"
    ), windll.dir_resource)

    assert int.from_bytes(info_len, byteorder='little') == len(info.data)

    strings = {
        "CompanyName": windll.layout.author,
        "FileDescription": windll.layout.name,
        "FileVersion": "%i.%i" % windll.layout.version,
        "InternalName": windll.layout.dll_name[:-4],
        "LegalCopyright": windll.layout.copyright,
        "OriginalFilename": windll.layout.dll_name,
        "ProductName": windll.layout.name,
        "ProductVersion": "%i.%i" % windll.layout.version,
    }
    strings_pattern = []
    for key, value in sorted(strings.items(), key=itemgetter(0)):
        length = (3 + len(key) + 1 + len(value) + 1) * 2
        if (3 + len(key) + 1) % 2 == 1:
            length += 2
        strings_pattern.extend((
            "!4(0)", WORD(length).data, WORD(len(value) + 1).data, WORD(1).data,
            WSTR(key).data, "!4(0)", WSTR(value).data
        ))

    file_ver_minor, file_ver_major, file_ver_build, file_ver_rev, \
    prod_ver_minor, prod_ver_major, prod_ver_build, prod_ver_rev, \
    ro_sfi, len_sfi, ro_st, len_st, ro_sfi_end = match_object((
        WORD(len(info.data)).data, WORD(0x34).data, WORD(0).data, WSTR("VS_VERSION_INFO").data, b'\0\0',
        # begin VS_FIXEDFILEINFO
        DWORD(0xFEEF04BD).data, MAKELONG(0, 1).data, *(["2(+)"] * 8), "4(?)", DWORD(0).data,
        DWORD(0x00040004).data, DWORD(2).data, DWORD(2).data, "8(?)",
        # end   VS_FIXEDFILEINFO
        # begin StringFileInfo
        ">", "2(+)", WORD(0).data, WORD(1).data, WSTR("StringFileInfo").data,
        # begin     StringTable
        ">", "2(+)", WORD(0).data, WORD(1).data, WSTR("000004B0").data,
        *strings_pattern,
        # end       StringTable
        # end   StringFileInfo
        ">", "!4(0)",
        # begin VarFileInfo
        WORD(0x44).data, WORD(0).data, WORD(1).data, WSTR("VarFileInfo").data, "2(0)",
        # begin     Var
        WORD(0x24).data, WORD(4).data, WORD(0).data, WSTR("Translation").data, "2(0)", MAKELONG(0, 0x4b0).data
        # end       Var
        # end   VarFileInfo
    ), info)

    target_version = (*windll.layout.version, 0, 0)
    for version in ((file_ver_major, file_ver_minor, file_ver_rev, file_ver_build),
                    (prod_ver_major, prod_ver_minor, prod_ver_rev, prod_ver_build)):
        assert version == target_version

    assert len_sfi == ro_sfi - ro_sfi_end, "StringFileInfo length wrong"
    assert len_st == ro_st - ro_sfi_end, "StringTable length wrong"


def test_link(windll: WinDll):
    windll.link()

    warn('test not implemented')  # TODO


def test_compile_dir_reloc(windll: WinDll):
    windll.compile_dir_reloc()

    symbols = []
    offset = 0

    while offset < len(windll.dir_reloc.data):
        base = int.from_bytes(windll.dir_reloc.data[offset + 0 : offset + 4], 'little')
        size = int.from_bytes(windll.dir_reloc.data[offset + 4 : offset + 8], 'little')
        end = offset + size
        offset += 8
        while offset < end:
            reloc = int.from_bytes(windll.dir_reloc.data[offset : offset + 2], 'little')
            offset += 2
            type, reloc = reloc // 0x1000, reloc % 0x1000
            if type == 0:
                continue
            position = base + reloc - windll.sec_data.placement[1]
            symbols.append(position)
            if type == 3:
                assert len(windll.sec_data.symbols[position]().data) == 4
            elif type == 0xA:
                assert len(windll.sec_data.symbols[position]().data) == 8
            else:
                raise AssertionError('invalid relocation type')
        assert offset == end
        assert offset % 4 == 0
    assert offset == len(windll.dir_reloc.data)

    assert list(sorted(windll.sec_data.symbols.keys())) == symbols

    assert windll.sec_reloc.data == windll.dir_reloc.data


def test_compile_header(windll: WinDll):
    windll.compile_header()

    pe, o_msg, o_msg_tgt = match_object((
        b'MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xFF\xFF\x00\x00'
        b'\xB8\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00', "4(0)",
        "16(0)", "12(0)", "4(&)",
        b'\x0E\x1F\xBA', "2(+)", b'\xB4\x09\xCD\x21\xB8\x01\x4C\xCD\x21',
        "<", b'This program cannot be run in DOS mode.\n\n\r$', "~"
    ), windll.sec_HEADER)

    assert o_msg + 0x40 == o_msg_tgt
    assert pe.placement[1] % 8 == 0

    match_object((
        b'PE\0\0', "~"  # TODO
    ), pe)


def test_assemble(windll: WinDll):
    windll.assemble()

    warn('test not implemented')  # TODO


def test_compile(windll: WinDll):
    assert windll.compile() == bytes(windll.assembly.data)
