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

from collections import defaultdict
from operator import itemgetter
from time import time
from typing import Union
from warnings import warn

from . import _version, _version_num
from .layout import *
from .wintypes import *
from .linker_binary import BinaryObject, link


__version__ = _version


@dataclass(eq=False)
class WinDll:
    layout: Layout
    architecture: Architecture

    timestamp: int

    kbd_modifiers: Optional[BinaryObject] = None
    kbd_vk_to_wchar_table: Optional[BinaryObject] = None
    kbd_dead_key: Optional[BinaryObject] = None
    kbd_key_names: Optional[BinaryObject] = None
    kbd_key_names_ext: Optional[BinaryObject] = None
    kbd_key_names_dead: Optional[BinaryObject] = None
    kbd_vsc_to_vk: Optional[BinaryObject] = None
    kbd_vsc_to_vk_e0: Optional[BinaryObject] = None
    kbd_vsc_to_vk_e1: Optional[BinaryObject] = None
    # kbd_ligature: Optional[BinaryObject] = None

    kbdtables: Optional[BinaryObject] = None

    dir_export: Optional[BinaryObject] = None
    dir_resource: Optional[BinaryObject] = None
    dir_reloc: Optional[BinaryObject] = None

    sec_HEADER: Optional[BinaryObject] = None
    sec_data: Optional[BinaryObject] = None
    sec_rsrc: Optional[BinaryObject] = None
    sec_reloc: Optional[BinaryObject] = None

    assembly: Optional[BinaryObject] = None

    align_file: int = 0x200
    align_section: int = 0x1000

    def __init__(self, layout: Layout, architecture: Architecture):
        self.layout = layout
        self.architecture = architecture

        self.timestamp = int(time())

    def compile(self) -> bytes:
        self.compile_kbd_keymap()
        self.compile_kbd_charmap()
        # self.compile_kbd_ligature()
        self.compile_tables()
        self.compile_dir_export()
        self.compile_dir_resource()
        self.link()
        self.compile_dir_reloc()
        self.compile_header()
        self.assemble()

        return bytes(self.assembly.data)

    def compile_kbd_keymap(self):
        vsc_to_vk = BinaryObject(alignment=4)
        for vsc in range(max(map(lambda k: k.code, filter(lambda k: k.prefix == 0, self.layout.keymap))) + 1):
            key = self.layout.keymap.get(ScanCode(vsc), KeyCode("invalid", 0xFF))
            vsc_to_vk.append(USHORT(key.win_vk))  # TODO attributes
        self.kbd_vsc_to_vk = vsc_to_vk

        key_names = BinaryObject(alignment=8)  # TODO non-printable only
        key_names_ext = BinaryObject(alignment=8)  # TODO non-printable only
        vsc_to_vk_e0 = BinaryObject(alignment=4)
        vsc_to_vk_e1 = BinaryObject(alignment=4)
        for scan_code, key_code in self.layout.keymap.items():
            if scan_code.prefix == 0:
                key_names.append(BYTE(scan_code.code))
                key_names.append(LPTR(self.architecture, WSTR("%x" % scan_code.code)))  # TODO
            elif scan_code.prefix == 0xE0:
                key_names_ext.append(BYTE(scan_code.code))
                key_names_ext.append(LPTR(self.architecture, WSTR("+%x" % scan_code.code)))  # TODO
                vsc_to_vk_e0.append(BYTE(scan_code.code))
                vsc_to_vk_e0.append(USHORT(key_code.win_vk))
            elif scan_code.prefix == 0xE1:
                vsc_to_vk_e1.append(BYTE(scan_code.code))
                vsc_to_vk_e1.append(USHORT(key_code.win_vk))
        key_names.append(BYTE(0))
        key_names.append(LPTR(self.architecture, None))
        self.kbd_key_names = key_names
        key_names_ext.append(BYTE(0))
        key_names_ext.append(LPTR(self.architecture, None))
        self.kbd_key_names_ext = key_names_ext
        vsc_to_vk_e0.append(BYTE(0))
        vsc_to_vk_e0.append(USHORT(0))
        self.kbd_vsc_to_vk_e0 = vsc_to_vk_e0
        vsc_to_vk_e1.append(BYTE(0))
        vsc_to_vk_e1.append(USHORT(0))
        self.kbd_vsc_to_vk_e1 = vsc_to_vk_e1

    def compile_kbd_charmap(self):
        vk_to_bits = BinaryObject(alignment=4)
        for key, shift in {0x10: 1, 0x11: 2, 0x12: 4, 0x15: 8}.items():  # TODO
            vk_to_bits.append(BYTE(key))
            vk_to_bits.append(BYTE(shift))
        vk_to_bits.append(WORD(0))  # end of table

        max_mask = 0
        shift_states = []
        shift_state_map = {}
        for scancode, keycode in self.layout.keymap.items():
            for shiftstate, character in self.layout.charmap.get(keycode, {}).items():
                if not shiftstate in shift_state_map:
                    shift_state_map[shiftstate] = len(shift_state_map)
                    shift_states.append(shiftstate)
                    max_mask = max(max_mask, shiftstate.to_win_mask())

        if len(shift_state_map) >= 15:
            raise RuntimeError("Too many shift states: %i >= 15" % len(shift_state_map))
        elif len(shift_state_map) > 10:
            warn("Too many shift states: %i > 10" % len(shift_state_map))

        modifiers = BinaryObject(alignment=8)
        modifiers.append(LPTR(self.architecture, vk_to_bits))
        modifiers.append(WORD(max_mask))
        for mask in range(max_mask + 1):
            modifiers.append(BYTE(shift_state_map.get(ShiftState.from_win_mask(mask), 0xF)))
        self.kbd_modifiers = modifiers

        vk_to_wchars = BinaryObject(alignment=2)
        for keycode, characters in self.layout.charmap.items():
            dead = None
            vk_to_wchars.append(BYTE(keycode.win_vk))
            vk_to_wchars.append(BYTE(0))  # Attributes  # TODO
            for shiftstate in range(len(shift_states)):
                character = characters.get(shift_states[shiftstate], Character("\uF000"))  # WCH_NONE
                if character.dead:
                    # TODO check entry exists?
                    if dead is None:
                        dead = {}
                    dead[shiftstate] = character.char
                    character = Character("\uF001")  # WCH_DEAD
                vk_to_wchars.append(WCHAR(character.char))
            if dead is not None:
                vk_to_wchars.append(BYTE(0xFF))
                vk_to_wchars.append(BYTE(0))
                for shiftstate in range(len(shift_states)):
                    vk_to_wchars.append(WCHAR(dead.get(shiftstate, "\uF000")))
        vk_to_wchars.append(BYTE(0))  # end of table
        vk_to_wchars.append(BYTE(0))
        for shiftstate in range(len(shift_states)):
            vk_to_wchars.append(WCHAR('\0'))

        vk_to_wchar_table = BinaryObject(alignment=8)
        vk_to_wchar_table.append(LPTR(self.architecture, vk_to_wchars))
        vk_to_wchar_table.append(BYTE(len(shift_states)))
        vk_to_wchar_table.append(BYTE(len(shift_states) * 2 + 2))
        self.kbd_vk_to_wchar_table = vk_to_wchar_table

        dead_key = BinaryObject(alignment=4)
        for accent, key in self.layout.deadkeys.items():
            for character, composed in key.charmap.items():
                dead_key.append(MAKELONG(ord(character), ord(accent)))
                dead_key.append(WCHAR(composed.char))
                dead_key.append(USHORT(1 if composed.dead else 0))
        dead_key.append(DWORD(0))  # end of table
        dead_key.append(WORD(0))  # WCHAR
        dead_key.append(USHORT(0))
        self.kbd_dead_key = dead_key

        key_names_dead = BinaryObject(alignment=8)
        for accent, key in self.layout.deadkeys.items():
            key_names_dead.append(LPTR(self.architecture, WSTR(accent + key.name)))
        self.kbd_key_names_dead = key_names_dead

    def compile_tables(self):
        kbdtables = BinaryObject(alignment=self.architecture.long_pointer)
        kbdtables.append(LPTR(self.architecture, self.kbd_modifiers))
        kbdtables.append(LPTR(self.architecture, self.kbd_vk_to_wchar_table))
        kbdtables.append(LPTR(self.architecture, self.kbd_dead_key))
        kbdtables.append(LPTR(self.architecture, self.kbd_key_names))
        kbdtables.append(LPTR(self.architecture, self.kbd_key_names_ext))
        kbdtables.append(LPTR(self.architecture, self.kbd_key_names_dead))
        kbdtables.append(LPTR(self.architecture, self.kbd_vsc_to_vk))
        kbdtables.append(BYTE(len(self.kbd_vsc_to_vk.data) // 2))
        kbdtables.append(LPTR(self.architecture, self.kbd_vsc_to_vk_e0))
        kbdtables.append(LPTR(self.architecture, self.kbd_vsc_to_vk_e1))
        kbdtables.append(MAKELONG(1, 1))  # TODO KLLF_ALTGR, KLLF_SHIFTLOCK, KLLF_LRM_RLM
        kbdtables.append(BYTE(0))
        kbdtables.append(BYTE(0))
        kbdtables.append(LPTR(self.architecture, None))  # ligature  # TODO ?
        kbdtables.append(DWORD(0))  # dwType, optional  # TODO ???
        kbdtables.append(DWORD(0))  # dwSubType, optional  # TODO ???

        self.kbdtables = kbdtables

    def compile_dir_export(self):
        func = BinaryObject(alignment=16)                           # -- PKBDTABLES KbdLayerDescriptor() --
        if self.architecture.pointer == 8:                          #
            func.append(BYTE(0x48))                                 # (if AMD64) REX ...
        func.append(BYTE(0xB8))                                     # MOV EAX, ...
        func.append(PTR(self.architecture, self.kbdtables, False))  # ... offset KbdLayerDescriptorTable
        if self.architecture == WOW64:                              #
            func.append(BYTE(0x99))                                 # (if WOW64) CDQ
        func.append(BYTE(0xC3))                                     # RET

        dll_name = STR(self.layout.dll_name)

        addresses = BinaryObject(alignment=4)
        addresses.append(RVA(func))

        func_name = STR("KbdLayerDescriptor")

        names = BinaryObject(alignment=4)
        names.append(RVA(func_name))

        ordinals = BinaryObject(alignment=4)
        ordinals.append(WORD(0))

        export = BinaryObject(alignment=16)     # -- Export Directory --
        export.append(DWORD(0))                 # Export Flags (reserved)
        export.append(DWORD(self.timestamp))    # Timestamp
        export.append(WORD(0))                  # Major Version (unused)
        export.append(WORD(0))                  # Minor Version (unused)
        export.append(RVA(dll_name))            # Name RVA
        export.append(DWORD(1))                 # Ordinal Base
        export.append(DWORD(1))                 # Address Table Entries
        export.append(DWORD(1))                 # Number of Name Pointers
        export.append(RVA(addresses))           # Export Address Table RVA
        export.append(RVA(names))               # Name Pointer Table RVA
        export.append(RVA(ordinals))            # Ordinal Table RVA

        # directories must be self-contained
        export.extend((addresses, names, ordinals, dll_name, func_name))

        self.dir_export = export

    def compile_dir_resource(self):
        def version_word():
            return MAKELONG(self.layout.version[1], self.layout.version[0])

        # https://docs.microsoft.com/en-us/windows/win32/api/verrsrc/ns-verrsrc-tagvs_fixedfileinfo
        info_fixed = BinaryObject(alignment=4)      # -- VS_FIXEDFILEINFO --
        info_fixed.append(DWORD(0xFEEF04BD))        # dwSignature (must be 0xFEEF04BD)
        info_fixed.append(MAKELONG(0, 1))           # dwStrucVersion (MAKELONG(minor, major))
        info_fixed.append(version_word())           # dwFileVersionMS (MAKELONG(minor, major))
        info_fixed.append(MAKELONG(0, 0))           # dwFileVersionLS (MAKELONG(build, revision))
        info_fixed.append(version_word())           # dwProductVersionMS (MAKELONG(minor, major))
        info_fixed.append(MAKELONG(0, 0))           # dwProductVersionLS (MAKELONG(build, revision))
        info_fixed.append(DWORD(0x3F))              # dwFileFlagsMask
        info_fixed.append(DWORD(0))                 # dwFileFlags
        info_fixed.append(DWORD(0x00040004))        # dwFileOS (VOS_NT_WINDOWS32)
        info_fixed.append(DWORD(2))                 # dwFileType (VFT_DLL)
        info_fixed.append(DWORD(2))                 # dwFileSubtype (VFT2_DRV_KEYBOARD)
        info_fixed.append(DWORD(0))                 # dwFileDateMS (unused)
        info_fixed.append(DWORD(0))                 # dwFileDateLS (unused)

        # https://docs.microsoft.com/en-us/windows/win32/menurc/stringtable
        string_table = BinaryObject(alignment=4)    # -- StringTable --
        string_table.append(WORD(0xFFFF))           # wLength (replaced at the end)
        string_table.append(WORD(0))                # wValueLength (must be zero)
        string_table.append(WORD(1))                # wType (0=binary, 1=text)
        string_table.append(WSTR("000004B0"))       # szKey (MAKELONG(codepage, language); UNICODE=0x04b0)
        string_table.append_padding(4)              # Padding
        for key, value in sorted({                  # Children (String{1,})
            "CompanyName": self.layout.author,
            "FileDescription": self.layout.name,
            "FileVersion": "%i.%i" % self.layout.version,
            "InternalName": self.layout.dll_name[:-4],
            "LegalCopyright": self.layout.copyright,
            "OriginalFilename": self.layout.dll_name,
            "ProductName": self.layout.name,
            "ProductVersion": "%i.%i" % self.layout.version,
        }.items(), key=itemgetter(0)):
            key = WSTR(key)
            value = WSTR(value)
            # https://docs.microsoft.com/en-us/windows/win32/menurc/string-str
            string = BinaryObject(alignment=4)          # -- String --
            string.append(WORD(0xFFFF))                 # wLength (replaced at the end)
            string.append(WORD(len(value.data) // 2))   # wValueLength (in words!)
            string.append(WORD(1))                      # wType (0=binary, 1=text)
            string.append(key)                          # szKey
            string.append_padding(4)                    # Padding
            string.append(value)                        # Value (WSTR)
            string.data[0:2] = WORD(len(string.data)).data
            string_table.append(string)
        string_table.data[0:2] = WORD(len(string_table.data)).data

        # https://docs.microsoft.com/en-us/windows/win32/menurc/stringfileinfo
        info_string = BinaryObject(alignment=4)     # -- StringFileInfo --
        info_string.append(WORD(0xFFFF))            # wLength (replaced at the end)
        info_string.append(WORD(0))                 # wValueLength (must be zero)
        info_string.append(WORD(1))                 # wType (0=binary, 1=text)
        info_string.append(WSTR("StringFileInfo"))  # szKey
        info_string.append_padding(4)               # Padding
        info_string.append(string_table)            # Children (StringTable{1,})
        info_string.data[0:2] = WORD(len(info_string.data)).data

        # https://docs.microsoft.com/en-us/windows/win32/menurc/var-str
        var = BinaryObject(alignment=4)             # -- Var --
        var.append(WORD(0xFFFF))                    # wLength (replaced at the end)
        var.append(WORD(4))                         # wValueLength
        var.append(WORD(0))                         # wType (0=binary, 1=text)
        var.append(WSTR("Translation"))             # szKey
        var.append_padding(4)                       # Padding
        var.append(MAKELONG(0, 0x04B0))             # Value (MAKELONG(language, codepage){1,}; UNICODE=0x04b0)
        var.data[0:2] = WORD(len(var.data)).data

        # https://docs.microsoft.com/en-us/windows/win32/menurc/varfileinfo
        info_var = BinaryObject(alignment=4)        # -- VarFileInfo --
        info_var.append(WORD(0xFFFF))               # wLength (replaced at the end)
        info_var.append(WORD(0))                    # wValueLength (must be zero)
        info_var.append(WORD(1))                    # wType (0=binary, 1=text)
        info_var.append(WSTR("VarFileInfo"))        # szKey
        info_var.append_padding(4)                  # Padding
        info_var.append(var)                        # Children (Var{1})
        info_var.data[0:2] = WORD(len(info_var.data)).data

        # https://docs.microsoft.com/en-us/windows/win32/menurc/vs-versioninfo
        info = BinaryObject(alignment=16)           # -- VS_VERSIONINFO --
        info.append(WORD(0xFFFF))                   # wLength (replaced at the end)
        info.append(WORD(len(info_fixed.data)))     # wValueLength
        info.append(WORD(0))                        # wType (0=binary, 1=text)
        info.append(WSTR("VS_VERSION_INFO"))        # szKey
        info.append_padding(4)                      # Padding1
        info.append(info_fixed)                     # Value (VS_FIXEDFILEINFO)
        info.append_padding(4)                      # Padding2
        info.append(info_string)                    # Children (StringFileInfo{0,1})
        info.append(info_var)                       # Children (VarFileInfo{0,1})
        info.data[0:2] = WORD(len(info.data)).data

        rsrc = BinaryObject(alignment=16)
        rsrc.append(RSRC_TABLES({0x10: {1: {0x409: (info, 0)}}}))
        rsrc.append(info)

        self.dir_resource = rsrc

    def link(self):
        base = self.align_section
        self.sec_data = link([self.dir_export], base=base)
        self.sec_data.alignment = self.align_file

        base += len(self.sec_data.data)
        base += (-base) % self.align_section
        self.sec_rsrc = link([self.dir_resource], base=base)
        self.sec_rsrc.alignment = self.align_file

        base += len(self.sec_rsrc.data)
        base += (-base) % self.align_section
        self.sec_reloc = link([], base=base)
        self.sec_reloc.alignment = self.align_file

    def compile_dir_reloc(self):
        reloc = BinaryObject(alignment=4)

        blocks = defaultdict(set)
        for offset, symbol in self.sec_data.symbols.items():
            if (isinstance(symbol, PTR) or isinstance(symbol, LPTR)) and symbol.target is not None:
                offset += self.sec_data.placement[1]
                blocks[offset // 0x1000].add((offset % 0x1000, symbol))

        for base, symbols in sorted(blocks.items(), key=itemgetter(0)):
            reloc.append(DWORD(base * 0x1000))
            length = 8 + 2 * len(symbols)
            if len(symbols) % 2 == 1:
                length += 2
            reloc.append(DWORD(length))
            for offset, symbol in sorted(symbols, key=itemgetter(0)):
                type = 0x3000 if len(symbol().data) == 4 else 0xA000
                reloc.append(WORD(offset + type))
            reloc.append_padding(4)

        self.dir_reloc = reloc

        # section is already linked, insert data directly
        self.sec_reloc.data.extend(reloc.data)
        self.dir_reloc.placement = (self.sec_reloc, 0)

    def compile_header(self):
        def len_file(section: BinaryObject):
            length = len(section.data)
            length += (-length) % self.align_file
            return length

        header = BinaryObject(alignment=self.align_file)

        # https://docs.microsoft.com/en-us/windows/win32/debug/pe-format#section-table-section-headers
        sec = BinaryObject(alignment=4)             # -- Section Table --
        for name, section, characteristics in (
                (b".data\0\0\0", self.sec_data, 0x60000040),  # char: init data, read, execute
                (b".rsrc\0\0\0", self.sec_rsrc, 0x42000040),  # char: init data, read, discard
                (b".reloc\0\0", self.sec_reloc, 0x42000040),  # char: init data, read, discard
        ):
            sec.append(name)                        # Name
            sec.append(DWORD(len(section.data)))    # VirtualSize
            sec.append(RVA(section)())              # VirtualAddress
            sec.append(DWORD(len_file(section)))    # SizeOfRawData
            sec.append(RVA(section))                # PointerToRawData
            sec.append(DWORD(0))                    # PointerToRelocations
            sec.append(DWORD(0))                    # PointerToLinenumbers
            sec.append(WORD(0))                     # NumberOfRelocations
            sec.append(WORD(0))                     # NumberOfLinenumbers
            sec.append(DWORD(characteristics))      # Characteristics

        # https://docs.microsoft.com/en-us/windows/win32/debug/pe-format#optional-header-standard-fields-image-only
        opt = BinaryObject(alignment=self.architecture.pointer)  # -- Optional Header --
        opt_magic = 0x10B if self.architecture.pointer == 4 else 0x20B
        opt.append(WORD(opt_magic))                 # Magic
        opt.append(BYTE(_version_num[0]))           # MajorLinkerVersion
        opt.append(BYTE(_version_num[1]))           # MinorLinkerVersion
        opt.append(DWORD(0))                        # SizeOfCode
        opt_size_data = sum(map(len_file, (self.sec_data, self.sec_rsrc, self.sec_reloc)))
        opt.append(DWORD(opt_size_data))            # SizeOfInitializedData
        opt.append(DWORD(0))                        # SizeOfUninitializedData
        opt.append(DWORD(0))                        # AddressOfEntryPoint
        opt.append(RVA(self.sec_data)())            # BaseOfCode
        if self.architecture.pointer == 4:
            opt.append(RVA(self.sec_data)())        # BaseOfData (PE32 only)
        opt.append(PTR(self.architecture, header))  # ImageBase
        opt.append(DWORD(self.align_section))       # SectionAlignment
        opt.append(DWORD(self.align_file))          # FileAlignment
        opt.append(WORD(5))                         # MajorOSVersion  # TODO is XP ok?
        opt.append(WORD(1))                         # MinorOSVersion  # TODO is WinXP SP1 ok?
        opt.append(WORD(self.layout.version[0]))    # MajorImageVersion
        opt.append(WORD(self.layout.version[1]))    # MinorImageVersion
        opt.append(WORD(5))                         # MajorSubsystemVersion  # TODO is XP ok?
        opt.append(WORD(1))                         # MinorSubsystemVersion  # TODO is WinXP SP1 ok?
        opt.append(DWORD(0))                        # Win32VersionValue (reserved)
        # assuming .reloc section is shorter than section alignment
        opt_img_size = self.sec_reloc.placement[1] + self.align_section
        opt.append(DWORD(opt_img_size))             # SizeOfImage
        opt.append(SIZEOF(DWORD, header))           # SizeOfHeaders
        opt.append(DWORD(0))                        # CheckSum  # FIXME
        opt.append(WORD(1))                         # Subsystem (1=native)
        opt.append(WORD(0x0540))                    # DllCharacteristics  # TODO
        _DWORD_PTR = DWORD_PTR(self.architecture)
        opt.append(_DWORD_PTR(0x040000))            # SizeOfStackReserve
        opt.append(_DWORD_PTR(0x001000))            # SizeOfStackCommit
        opt.append(_DWORD_PTR(0x100000))            # SizeOfHeapReserve
        opt.append(_DWORD_PTR(0x001000))            # SizeOfHeapCommit
        opt.append(DWORD(0))                        # LoaderFlags (reserved)
        directories = (                                         # Data Directories:
            self.dir_export, None, self.dir_resource, None,     # Export, Import, Resource, Exception
            None, self.dir_reloc, None, None,                   # Certificate, Relocation, Debug, Architecture
            None, None, None, None,                             # Global Ptr, TLS, Load Config, Bound Import
            None, None, None, None,                             # IAT, Delay Import, CLR Runtime, (reserved)
        )
        opt.append(DWORD(len(directories)))         # NumberOfRvaAndSizes
        for directory in directories:
            if directory is not None:
                opt.append(RVA(directory)())
                opt.append(SIZEOF(DWORD, directory))
            else:
                opt.append(DWORD(0))
                opt.append(DWORD(0))

        # https://docs.microsoft.com/en-us/windows/win32/debug/pe-format#coff-file-header-object-and-image
        coff = BinaryObject(alignment=4)            # -- COFF header --
        coff_machine = 0x14C if self.architecture.pointer == 4 else 0x8664
        coff.append(WORD(coff_machine))             # Machine
        coff.append(WORD(3))                        # NumberOfSections
        coff.append(DWORD(self.timestamp))          # TimeDateStamp
        coff.append(DWORD(0))                       # PointerToSymbolTable (deprecated)
        coff.append(DWORD(0))                       # NumberOfSymbol (deprecated)
        coff.append(WORD(len(opt.data)))            # SizeOfOptionalHeader
        coff_characteristics = 0x210E if self.architecture.pointer == 4 else 0x2022
        coff.append(WORD(coff_characteristics))     # Characteristics

        pe = BinaryObject(alignment=8)      # -- PE header --
        pe.append(b"PE\0\0")                # Signature
        pe.extend((coff, opt, sec))

        # https://www.fileformat.info/format/exe/corion-mz.htm
        # https://en.wikibooks.org/wiki/X86_Disassembly/Windows_Executable_Files#MS-DOS_header
        mz = BinaryObject(alignment=16)     # -- MZ header --
        mz.append(b"MZ")                    # signature
        mz.append(WORD(0x90))               # length of last page
        mz.append(WORD(3))                  # number of (512-byte) pages
        mz.append(WORD(0))                  # number of reloc entries
        mz.append(WORD(4))                  # header size (paragraphs / 16-byte blocks)
        mz.append(WORD(0))                  # min extra paragraphs
        mz.append(WORD(0xFFFF))             # max extra paragraphs
        mz.append(WORD(0))                  # initial SS
        mz.append(WORD(0xB8))               # initial SP
        mz.append(WORD(0))                  # checksum or 0
        mz.append(MAKELONG(0, 0))           # initial CS:IP
        mz.append(WORD(0x40))               # reloc offset
        mz.append(WORD(0))                  # overlay number (0 = main program)
        mz.append(b'\0\0' * 16)             # varies
        mz.append(RVA(pe))                  # PE offset
                                            # -- DOS stub --
        mz.append(b'\x0E')                  # PUSH CS
        mz.append(b'\x1F')                  # POP DS
        mz.append(b'\xBA')                  # MOV DX, ...
        mz.append(WORD(0xE, False))         # ... offset 0xE
        mz.append(b'\xB4\x09')              # MOV AH, 0x09
        mz.append(b'\xCD\x21')              # INT 0x21
        mz.append(b'\xB8')                  # MOV AX, ...
        mz.append(WORD(0x4C01, False))      # ... 0x4C01 (exit(1))
        mz.append(b'\xCD\x21')              # INT 0x21
        mz.append(b'This program cannot be run in DOS mode.\n\n\r$')  # message

        notice = BinaryObject(alignment=16)
        notice.append(STR("Generated with PyKbd %s for %s" % (__version__, self.architecture.name)))

        header.extend([mz, notice, pe])
        header.append_padding(self.align_file)

        self.sec_HEADER = header

    def assemble(self):
        for section in (self.sec_data, self.sec_rsrc, self.sec_reloc):
            section.placement = None
            section.symbols = {}
        self.assembly = link((
            self.sec_HEADER,
            self.sec_data,
            self.sec_rsrc,
            self.sec_reloc,
            BinaryObject(alignment=self.align_file)
        ))


_RSRC_TABLE_ENTRIES = Dict[Union[int, str], Union[Tuple[BinaryObject, int], '_RSRC_TABLE_ENTRIES']]


@dataclass(frozen=True)
class _RSRC_OFFSET(Symbol):
    target: BinaryObject
    xor: int = 0

    def __call__(self) -> BinaryObject:
        offset = (self.target.find_placement() or (None, 0))[1]
        return DWORD(offset ^ self.xor)


def _RSRC_ENTRY(data: BinaryObject, codepage: int):
    rsrc = BinaryObject(alignment=4)
    rsrc.append(RVA(data))
    rsrc.append(DWORD(len(data.data)))
    rsrc.append(DWORD(codepage))
    rsrc.append(DWORD(0))
    return rsrc


def _RSRC_TABLE(entries: _RSRC_TABLE_ENTRIES):
    children = []
    strings = []

    name_entries = {key: value for key, value in entries.items() if isinstance(key, str)}
    id_entries = {key: value for key, value in entries.items() if isinstance(key, int)}

    table = BinaryObject(alignment=4)
    table.append(DWORD(0))
    table.append(DWORD(0))
    table.append(WORD(0))
    table.append(WORD(0))
    table.append(WORD(len(name_entries)))
    table.append(WORD(len(id_entries)))

    for key, value in sorted(name_entries.items(), key=itemgetter(0)):
        name = BinaryObject(WORD(len(key)).data, alignment=2)
        name.append(WSTR(key))
        strings.append(name)
        table.append(_RSRC_OFFSET(name))
        xor = 0
        if isinstance(value, tuple):
            value = _RSRC_ENTRY(*value)
        else:
            value, value_strings = _RSRC_TABLE(value)
            strings.extend(value_strings)
            xor = 0x80000000
        table.append(_RSRC_OFFSET(value, xor))
        children.append(value)

    for key, value in sorted(id_entries.items(), key=itemgetter(0)):
        table.append(DWORD(key))
        xor = 0
        if isinstance(value, tuple):
            value = _RSRC_ENTRY(*value)
        else:
            value, value_strings = _RSRC_TABLE(value)
            strings.extend(value_strings)
            xor = 0x80000000
        table.append(_RSRC_OFFSET(value, xor))
        children.append(value)

    table.extend(children)

    return table, strings


def RSRC_TABLES(entries: _RSRC_TABLE_ENTRIES):
    rsrc = BinaryObject(alignment=4)
    table, strings = _RSRC_TABLE(entries)
    rsrc.append(table)
    rsrc.extend(strings)

    for offset, symbol in [(offset, symbol) for offset, symbol in rsrc.symbols.items()
                           if isinstance(symbol, _RSRC_OFFSET)]:
        del rsrc.symbols[offset]
        rsrc.data[offset : offset + 4] = symbol().data

    return rsrc
