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
from bisect import bisect_left
from collections import defaultdict
from operator import itemgetter
from time import time
from typing import Union, List
from warnings import warn

from . import _version, _version_num
from .layout import *
from .wintypes import *
from .linker_binary import BinaryObject, BinaryObjectReader, link


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

    # compile-only
    sec_HEADER: Optional[BinaryObject] = None
    sec_data: Optional[BinaryObject] = None
    sec_rsrc: Optional[BinaryObject] = None
    sec_reloc: Optional[BinaryObject] = None

    # decompile-only
    base: Optional[int] = None
    sections: Optional[List[Tuple[int, int]]] = None
    vk_names: Optional[Dict[int, str]] = None

    assembly: Optional[BinaryObject] = None

    align_file: int = 0x200
    align_section: int = 0x1000

    def __init__(self, layout: Optional[Layout] = None, architecture: Optional[Architecture] = None):
        self.layout = layout or Layout()
        self.architecture = architecture or AMD64

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

    def decompile(self, data: bytes):
        self.assembly = BinaryObject(data, alignment=self.align_file)

        self.decompile_header()
        # skipping .reloc
        self.decompile_dir_export()
        self.decompile_tables()
        self.decompile_kbd_keymap()
        self.decompile_kbd_charmap()
        self.decompile_fix_names()
        self.decompile_dir_resource()

    def _extract_fixed(self, rva: int, size: int):
        section_rva, section_offset = self.sections[bisect_left(self.sections, (rva + 1, 0)) - 1]
        offset = section_offset + (rva - section_rva)
        return bytes(self.assembly.data[offset : offset + size])

    def _extract_array(self, rva: int, entry_size: int):
        data = bytearray()
        while True:
            entry = self._extract_fixed(rva, entry_size)
            rva += entry_size
            data.extend(entry)
            if entry.strip(b"\0") == b"":
                break
        return bytes(data), len(data) // entry_size - 1

    def compile_kbd_keymap(self):
        vsc_to_vk = BinaryObject(alignment=4)
        for vsc in range(max(map(lambda k: k.code, filter(lambda k: k.prefix == 0, self.layout.keymap))) + 1):
            key = self.layout.keymap.get(ScanCode(vsc), KeyCode("invalid", 0xFF))
            vsc_to_vk.append(USHORT(key.win_vk))
        self.kbd_vsc_to_vk = vsc_to_vk

        key_names = BinaryObject(alignment=8)  # TODO non-printable only
        key_names_ext = BinaryObject(alignment=8)  # TODO non-printable only
        vsc_to_vk_e0 = BinaryObject(alignment=4)
        vsc_to_vk_e1 = BinaryObject(alignment=4)
        for scan_code, key_code in self.layout.keymap.items():
            if scan_code.prefix == 0:
                if key_code.name != chr(key_code.win_vk & 0xFF):
                    key_names.append(BYTE(scan_code.code))
                    key_names.append(LPTR(self.architecture, WSTR(key_code.name)))
            elif scan_code.prefix == 0xE0:
                if key_code.name != chr(key_code.win_vk & 0xFF):
                    key_names_ext.append(BYTE(scan_code.code))
                    key_names_ext.append(LPTR(self.architecture, WSTR(key_code.name)))
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

    def decompile_kbd_keymap(self):
        names = {}
        self.vk_names = {}
        if self.kbd_key_names is not None:
            key_names = BinaryObjectReader(self.kbd_key_names)
            while True:
                vsc = BYTE.read(key_names)
                if vsc == 0:
                    break
                name_rva = LPTR.read(key_names, self.architecture) - self.base
                name = self._extract_array(name_rva, 2)[0][:-2].decode('utf-16le')
                names[ScanCode(vsc)] = name

        if self.kbd_key_names_ext is not None:
            key_names_ext = BinaryObjectReader(self.kbd_key_names_ext)
            while True:
                vsc = BYTE.read(key_names_ext)
                if vsc == 0:
                    break
                name_rva = LPTR.read(key_names_ext, self.architecture) - self.base
                name = self._extract_array(name_rva, 2)[0][:-2].decode('utf-16le')
                names[ScanCode(vsc, 0xE0)] = name

        vsc_to_vk = BinaryObjectReader(self.kbd_vsc_to_vk)
        vsc_to_vk_len = len(self.kbd_vsc_to_vk.data) // 2
        for vsc in range(vsc_to_vk_len):
            vk = USHORT.read(vsc_to_vk)
            if vk == 0xFF or vk == 0:
                continue
            scancode = ScanCode(vsc)
            name = names.get(scancode, chr(vk & 0xFF))
            if scancode in self.layout.keymap:
                warn("replacing duplicate scancode: 0x%X" % vsc)
            if vk in self.vk_names:
                warn("replacing duplicate vk name: (0x%X) '%s' -> '%s'" % (vk, self.vk_names[vk], name))
            self.vk_names[vk] = name
            self.layout.keymap[scancode] = KeyCode(name, vk)

        vsc_to_vk_e0 = BinaryObjectReader(self.kbd_vsc_to_vk_e0)
        while True:
            vsc = BYTE.read(vsc_to_vk_e0)
            if vsc == 0:
                break
            vk = USHORT.read(vsc_to_vk_e0)
            scancode = ScanCode(vsc, 0xE0)
            name = names.get(scancode, chr(vk & 0xFF))
            if scancode in self.layout.keymap:
                warn("replacing duplicate scancode: 0xE0 0x%X" % vsc)
            if vk in self.vk_names:
                warn("replacing duplicate vk name: (0x%X) '%s' -> '%s'" % (vk, self.vk_names[vk], name))
            self.vk_names[vk] = name
            self.layout.keymap[scancode] = KeyCode(name, vk)

        # only Pause key, no name table
        vsc_to_vk_e1 = BinaryObjectReader(self.kbd_vsc_to_vk_e1)
        while True:
            vsc = BYTE.read(vsc_to_vk_e1)
            if vsc == 0:
                break
            vk = USHORT.read(vsc_to_vk_e1)
            scancode = ScanCode(vsc, 0xE1)
            if vsc == 0x1D:
                name = "Pause"
            else:
                name = "0xE1%X" % vsc
            if scancode in self.layout.keymap:
                warn("replacing duplicate scancode: 0xE1 0x%X" % vsc)
            self.layout.keymap[scancode] = KeyCode(name, vk)
        
    def compile_kbd_charmap(self):
        vk_to_bits = BinaryObject(alignment=4)
        for key, shift in {0x10: 1, 0x11: 2, 0x12: 4, 0x15: 8}.items():  # pretty much guaranteed
            vk_to_bits.append(BYTE(key))
            vk_to_bits.append(BYTE(shift))
        vk_to_bits.append(WORD(0))  # end of table

        vk_translate = {
            # drop KBDEXT for VK_DIVIDE and VK_CANCEL
            0x16F: 0x6F, 0x103: 0x03,
            # drop KBDSPECIAL for VK_MULTIPLY if present
            # note: KBDSPECIAL is preserved for special keys without characters
            0x26A: 0x6A,
            # apply KBDNUMPAD | KBDSPECIAL translation to VK_NUMPAD* and VK_DECIMAL
            0xC24: 0x67, 0xC26: 0x68, 0xC21: 0x69,
            0xC25: 0x64, 0xC0C: 0x65, 0xC27: 0x66,
            0xC23: 0x61, 0xC28: 0x62, 0xC22: 0x63,
            0xC2D: 0x60, 0xC2E: 0x6E,
        }
        max_mask = 0
        shift_states = []
        shift_state_map = {}
        key_to_vk = {}
        for scancode, keycode in self.layout.keymap.items():
            if keycode.name not in self.layout.charmap:
                continue
            vk = keycode.win_vk
            if vk == 0xFF or vk == 0:
                warn("invalid vk, skipping: 0x%X" % vk)
                continue
            if vk > 0xFF:
                try:
                    vk = vk_translate[vk]
                except KeyError:
                    warn("unknown special vk, skipping: 0x%X" % vk)
                    continue
            key_to_vk[keycode.name] = vk
            for shiftstate, character in self.layout.charmap[keycode.name].items():
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
            if keycode not in key_to_vk:
                warn("unmapped key, skipping: " + keycode)
                continue
            dead = None
            vk_to_wchars.append(BYTE(key_to_vk[keycode]))
            vk_to_wchars.append(BYTE(0))  # Attributes  # TODO (CAPLOK, SGCAPS, CAPLOKALTGR, KANALOC)
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
        vk_to_wchar_table.append(LPTR(self.architecture, None))  # end of table
        vk_to_wchar_table.append(BYTE(0))
        vk_to_wchar_table.append(BYTE(0))
        vk_to_wchar_table.append_padding(self.architecture.long_pointer)
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
        key_names_dead.append(LPTR(self.architecture, None))  # end of table
        self.kbd_key_names_dead = key_names_dead

    def decompile_kbd_charmap(self):
        modifiers = BinaryObjectReader(self.kbd_modifiers)

        vk_to_bits_rva = LPTR.read(modifiers, self.architecture) - self.base
        vk_to_bits_data, vk_to_bits_len = self._extract_array(vk_to_bits_rva, 2)
        vk_to_bits = BinaryObjectReader(BinaryObject(vk_to_bits_data, alignment=4))
        bit_to_vk = {}
        for _ in range(vk_to_bits_len):
            key = BYTE.read(vk_to_bits)
            shift = BYTE.read(vk_to_bits)
            bit_to_vk[shift] = key

        max_mask = WORD.read(modifiers)
        shift_state_map = {}
        for mask in range(max_mask + 1):
            column = BYTE.read(modifiers)
            if column != 0xF:
                shift_state_map[column] = ShiftState.from_win_mask(mask)  # TODO use bit_to_vk

        vk_translate = {
            # add KBDEXT to VK_DIVIDE and VK_CANCEL
            0x6F: 0x16F, 0x03: 0x103,
            # add KBDSPECIAL to VK_MULTIPLY
            0x6A: 0x26A,
            # translate VK_NUMPAD* and VK_DECIMAL to KBDNUMPAD | KBDSPECIAL navigation keys
            0x67: 0xC24, 0x68: 0xC26, 0x69: 0xC21,
            0x64: 0xC25, 0x65: 0xC0C, 0x66: 0xC27,
            0x61: 0xC23, 0x62: 0xC28, 0x63: 0xC22,
            0x60: 0xC2D, 0x6E: 0xC2E,
        }
        vk_to_wchar_table = BinaryObjectReader(self.kbd_vk_to_wchar_table)
        while True:
            vk_to_wchar_ptr = LPTR.read(vk_to_wchar_table, self.architecture)
            if vk_to_wchar_ptr == 0:
                break
            vk_to_wchar_rva = vk_to_wchar_ptr - self.base
            vk_to_wchar_cols = BYTE.read(vk_to_wchar_table)
            vk_to_wchar_width = BYTE.read(vk_to_wchar_table)

            vk_to_wchar_data, vk_to_wchar_rows = self._extract_array(vk_to_wchar_rva, vk_to_wchar_width)
            vk_to_wchar = BinaryObjectReader(BinaryObject(vk_to_wchar_data, alignment=2))
            row = 0
            while row < vk_to_wchar_rows:
                vk = BYTE.read(vk_to_wchar)
                attributes = BYTE.read(vk_to_wchar)  # TODO (CAPLOK, SGCAPS, CAPLOKALTGR, KANALOC)
                if vk not in self.vk_names and vk in vk_translate:
                    keycode = self.vk_names.get(vk_translate[vk])
                else:
                    keycode = self.vk_names.get(vk)
                dead = None
                characters = {}
                for col in range(vk_to_wchar_cols):
                    shiftstate = shift_state_map[col]
                    character = Character(WCHAR.read(vk_to_wchar))
                    if character.char == "\uF000":  # Null
                        pass
                    elif character.char == "\uF001":  # Dead
                        if dead is None:
                            dead = {}
                        dead[col] = True
                    elif character.char == "\uF002":  # Ligature
                        warn("ligature detected, skipping")
                    else:
                        characters[shiftstate] = character
                row += 1
                if dead is not None:
                    vk_to_wchar.read_or_warn(BYTE(0xFF))
                    vk_to_wchar.read_or_warn(BYTE(0x00))
                    for col in range(vk_to_wchar_cols):
                        if not dead.get(col, False):
                            vk_to_wchar.read_or_warn(WCHAR("\uF000"))
                        else:
                            shiftstate = shift_state_map[col]
                            character = Character(WCHAR.read(vk_to_wchar), True)
                            if character.char in "\uF000\uF001\uF002":
                                warn("dead key maps to invalid character")
                            else:
                                characters[shiftstate] = character
                    row += 1
                if keycode is None:
                    warn("vk 0x%X is mapped but not assigned to any vsc" % vk)
                    keycode = characters.get(ShiftState(), chr(vk & 0xFF))
                if keycode in self.layout.charmap:
                    warn("replacing duplicate keycode: " + str(keycode))
                self.layout.charmap[keycode] = characters

        dead_key_names = {}
        if self.kbd_key_names_dead is not None:
            key_names_dead = BinaryObjectReader(self.kbd_key_names_dead)
            while True:
                name_ptr = LPTR.read(key_names_dead, self.architecture)
                if name_ptr == 0:
                    break
                name = self._extract_array(name_ptr - self.base, 2)[0][:-2].decode('utf-16le')  # TODO use WSTR
                dead_key_names[name[0]] = name[1:]

        if self.kbd_dead_key is not None:
            dead_key = BinaryObjectReader(self.kbd_dead_key)
            while True:
                character = WCHAR.read(dead_key)
                accent = WCHAR.read(dead_key)
                if character == '\0' and accent == '\0':
                    break
                composed_char = WCHAR.read(dead_key)
                composed_attr = USHORT.read(dead_key)
                if composed_attr > 1:
                    warn("unknown dead key attributes: 0x%x" % composed_attr)
                composed = Character(composed_char, composed_attr == 1)
                if accent not in self.layout.deadkeys:
                    self.layout.deadkeys[accent] = DeadKey(dead_key_names.get(accent, accent), {})
                if character in self.layout.deadkeys[accent].charmap:
                    warn("replacing duplicate dead key: '%s' + '%s'" % (accent, character))
                self.layout.deadkeys[accent].charmap[character] = composed

    def decompile_fix_names(self):
        rename = {}
        for scancode, keycode in self.layout.keymap.items():
            if keycode.name == chr(keycode.win_vk & 0xFF):
                new_name = self.layout.charmap.get(keycode.name, {}).get(ShiftState())
                if new_name is None:
                    warn("unnamed vsc without vk character mapping: 0x%s" % scancode.to_string())
                    rename[keycode.name] = "0x%X" % keycode.win_vk
                else:
                    rename[keycode.name] = new_name.char
        self.layout.keymap = {scancode: KeyCode(rename.get(keycode.name, keycode.name), keycode.win_vk)
                              for scancode, keycode in self.layout.keymap.items()}
        self.layout.charmap = {rename.get(keycode, keycode): character
                               for keycode, character in self.layout.charmap.items()}

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

    def decompile_tables(self):
        kbdtables = BinaryObjectReader(self.kbdtables)

        modifiers_rva = LPTR.read(kbdtables, self.architecture) - self.base
        modifiers_len = BinaryObject(self._extract_fixed(modifiers_rva + self.architecture.long_pointer, 2), alignment=2)
        modifiers_len = self.architecture.long_pointer + 2 * (WORD.read(BinaryObjectReader(modifiers_len)) + 2)
        self.kbd_modifiers = BinaryObject(self._extract_fixed(modifiers_rva, modifiers_len), alignment=8)

        vk_to_wchar_table_rva = LPTR.read(kbdtables, self.architecture) - self.base
        self.kbd_vk_to_wchar_table = BinaryObject(self._extract_array(vk_to_wchar_table_rva, 2 * self.architecture.long_pointer)[0], alignment=8)

        dead_key_ptr = LPTR.read(kbdtables, self.architecture)
        if dead_key_ptr != 0:
            dead_key_rva = dead_key_ptr - self.base
            self.kbd_dead_key = BinaryObject(self._extract_array(dead_key_rva, 8)[0], alignment=8)

        key_names_ptr = LPTR.read(kbdtables, self.architecture)
        if key_names_ptr != 0:
            key_names_rva = key_names_ptr - self.base
            self.kbd_key_names = BinaryObject(self._extract_array(key_names_rva, 2 * self.architecture.long_pointer)[0], alignment=8)

        key_names_ext_ptr = LPTR.read(kbdtables, self.architecture)
        if key_names_ext_ptr != 0:
            key_names_ext_rva = key_names_ext_ptr - self.base
            self.kbd_key_names_ext = BinaryObject(self._extract_array(key_names_ext_rva, 2 * self.architecture.long_pointer)[0], alignment=8)

        key_names_dead_ptr = LPTR.read(kbdtables, self.architecture)
        if key_names_dead_ptr != 0:
            key_names_dead_rva = key_names_dead_ptr - self.base
            self.kbd_key_names_dead = BinaryObject(self._extract_array(key_names_dead_rva, self.architecture.long_pointer)[0], alignment=8)

        vsc_to_vk_rva = LPTR.read(kbdtables, self.architecture) - self.base
        vsc_to_vk_len = BYTE.read(kbdtables)
        self.kbd_vsc_to_vk = BinaryObject(self._extract_fixed(vsc_to_vk_rva, 2 * vsc_to_vk_len), alignment=8)

        vsc_to_vk_e0_rva = LPTR.read(kbdtables, self.architecture) - self.base
        self.kbd_vsc_to_vk_e0 = BinaryObject(self._extract_array(vsc_to_vk_e0_rva, 4)[0], alignment=8)
        vsc_to_vk_e1_rva = LPTR.read(kbdtables, self.architecture) - self.base
        self.kbd_vsc_to_vk_e1 = BinaryObject(self._extract_array(vsc_to_vk_e1_rva, 4)[0], alignment=8)

        # TODO characteristics, types, ligatures, ...

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

    def decompile_dir_export(self):
        reader = BinaryObjectReader(self.dir_export)

        # we assume the dll has only one function: KbdLayerDescriptor (warn and guess otherwise)

        reader.offset = 12                  # -- Export Directory --
        dll_name_rva = DWORD.read(reader)   # Name RVA
        reader.read_or_warn(DWORD(1))       # Ordinal Base
        reader.read_or_warn(DWORD(1))       # Address Table Entries
        reader.read_or_warn(DWORD(1))       # Number of Name Pointers
        addresses = DWORD.read(reader)      # Export Address Table RVA

        # TODO this is temporary
        self.layout.name = self._extract_array(dll_name_rva, 1)[0][:-1].decode('utf-8')

        func_rva = DWORD.read(BinaryObjectReader(BinaryObject(self._extract_fixed(addresses, 4), alignment=4)))
        # function is typically shorter than 16 bytes
        func = BinaryObject(self._extract_fixed(func_rva, 16), alignment=4)

        reader = BinaryObjectReader(func)
        if self.architecture == AMD64:
            reader.read_or_fail(BYTE(0x48))
        ins = BYTE.read(reader)
        if ins == 0xB8:  # MOV EAX, ...
            table_rva = DWORD_PTR(self.architecture).read(reader, align=False) - self.base
            ins = BYTE.read(reader)
            if ins == 0x99:
                if self.architecture == X86:
                    self.architecture = WOW64
                elif self.architecture != WOW64:
                    raise IOError("unexpected instruction: 0x%X" % ins)
                ins = BYTE.read(reader)
        elif ins == 0x8D:  # LEA ...
            reader.read_or_fail(BYTE(0x05))  # (ModRM) ... [EAX] + disp32
            table_rva = INT.read(reader, align=False)
            table_rva += func_rva + reader.offset
            ins = BYTE.read(reader)
        else:
            raise IOError("unexpected instruction: 0x%X" % ins)
        if ins != 0xC3:
            raise IOError("unexpected instruction: 0x%X" % ins)

        self.kbdtables = BinaryObject(self._extract_fixed(table_rva, 11 * self.architecture.long_pointer + 16),
                                      alignment=self.architecture.long_pointer)

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

    def decompile_dir_resource(self):
        if self.dir_resource is None:
            warn("no resources")
            return

        try:
            entry_loc = _RSRC_TABLE_read(BinaryObjectReader(self.dir_resource))
            info_entry = entry_loc.get(0x10, {}).get(1, {}).get(0x409)
            if info_entry is None:
                warn("no version info")
                return
            info_rva, info_len, info_cp = info_entry
            info_data = BinaryObject(self._extract_fixed(info_rva, info_len), alignment=4)

            def read_node(reader: BinaryObjectReader):
                reader.read_padding(4)
                end = reader.offset + WORD.read(reader)
                value_len = WORD.read(reader)
                is_text = WORD.read(reader) == 1
                name = WSTR.read(reader)
                reader.read_padding(4)
                if is_text:
                    data = reader.read_bytes(2 * value_len).decode('utf-16le')
                else:
                    data = BinaryObject(reader.read_bytes(value_len), alignment=4)
                children = {}  # perhaps this should be an multimap? it doesn't matter for version info
                reader.read_padding(4)
                while reader.offset < end:
                    child_name, child_value, child_children = read_node(reader)
                    children[child_name] = (child_value, child_children)
                    reader.read_padding(4)
                return name, data, children

            vs_version_info, info_fixed, info_other = read_node(BinaryObjectReader(info_data))

            if vs_version_info != "VS_VERSION_INFO":
                warn("invalid resources, skipping")
                return

            # use file version as layout version
            version_minor, version_major = MAKELONG.read(BinaryObjectReader(info_fixed, 8))
            self.layout.version = (version_major, version_minor)

            info_string = info_other.get('StringFileInfo')
            if info_string is None:
                warn("no StringFileInfo")
            else:
                info_string = info_string[1]
                for lang, (_, strings) in info_string.items():
                    cp, lang = MAKELONG.read(BinaryObjectReader(BinaryObject(bytes.fromhex(lang)[::-1], alignment=4)))
                    if cp == 1200:  # utf-16le
                        print("using StringFileInfo for language 0x%X" % lang)
                        self.layout.name = strings.get("FileDescription", strings.get("ProductName", ("\0", {})))[0][:-1]
                        if "FileVersion" in strings:
                            self.layout.name += " " + strings["FileVersion"][0][:-1]
                        elif "ProductVersion" in strings:
                            self.layout.name += " " + strings["ProductVersion"][0][:-1]
                        self.layout.author = strings.get("CompanyName", ("\0", {}))[0][:-1]
                        self.layout.copyright = strings.get("LegalCopyright", ("\0", {}))[0][:-1]
                        self.layout.dll_name = strings.get("OriginalFilename", ("\0", {}))[0][:-1]
                        break
                else:
                    warn("no usable StringFileInfo found")
        except Exception as e:
            warn(e)

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

    def decompile_header(self):
        reader = BinaryObjectReader(self.assembly)

        reader.read_or_fail(b"MZ")  # MZ header -- file signature
        reader.offset = 0x3C

        # TODO extract notice

        reader.offset = DWORD.read(reader)      # -- PE header --
        reader.read_or_fail(b"PE\0\0")          # Signature
                                                            #   -- COFF header --
        coff_machine = WORD.read(reader)                    # Machine
        if coff_machine == 0x14C:
            self.architecture = X86  # could be WOW64, checked later
        elif coff_machine == 0x8664:
            self.architecture = AMD64
        else:
            raise IOError("unknown architecture: %x" % coff_machine)
        num_sections = WORD.read(reader)                    # NumberOfSections
        self.timestamp = DWORD.read(reader)                 # TimeDateStamp
        DWORD.read(reader)                                  # PointerToSymbolTable (deprecated)
        DWORD.read(reader)                                  # NumberOfSymbol (deprecated)
        opt_end = reader.offset + 4 + WORD.read(reader)     # SizeOfOptionalHeader
        coff_characteristics = 0x210E if self.architecture.pointer == 4 else 0x2022
        reader.read_or_warn(WORD(coff_characteristics))     # Characteristics

                                                                # -- Optional Header --
        opt_magic = 0x10B if self.architecture.pointer == 4 else 0x20B
        reader.read_or_fail(WORD(opt_magic))                    # Magic
        reader.offset += 26 if self.architecture.pointer == 4 else 22
        self.base = DWORD_PTR(self.architecture).read(reader)   # ImageBase
        if self.base != self.architecture.base:
            warn("image uses base 0x%x instead of preferred 0x%x" % (self.base, self.architecture.base))
        opt_align_section = DWORD.read(reader)                  # SectionAlignment
        if opt_align_section != self.align_section:
            warn("image uses section alignment 0x%x instead of preferred 0x%x" % (opt_align_section, self.align_section))
            self.align_section = opt_align_section
        opt_align_file = DWORD.read(reader)                     # FileAlignment
        if opt_align_file != self.align_file:
            warn("image uses file alignment 0x%x instead of preferred 0x%x" % (opt_align_file, self.align_file))
            self.align_file = opt_align_file
        reader.offset += 9 * 4 + 4 * self.architecture.pointer
        opt_dir_len = DWORD.read(reader)                        # Directories
        if opt_dir_len < 1:
            raise IOError("no Export directory in image")
        dir_export_rva = DWORD.read(reader)                     # Export - Rva
        dir_export_len = DWORD.read(reader)                     # Export - Size
        if dir_export_rva == 0:
            raise IOError("no Export directory in image")
        if opt_dir_len < 3:
            dir_resource_rva = 0                                # Resource - Rva
            dir_resource_len = 0                                # Resource - Size
        else:
            reader.offset += 8
            dir_resource_rva = DWORD.read(reader)               # Resource - Rva
            dir_resource_len = DWORD.read(reader)               # Resource - Size
        if reader.offset > opt_end:
            raise IOError("SizeOfOptionalHeader too low")
        reader.offset = opt_end                     # -- Section Table --
        self.sections = []
        for _ in range(num_sections):
            name = reader.read_bytes(8)             # Name
            sec_len = DWORD.read(reader)            # VirtualSize
            sec_rva = DWORD.read(reader)            # VirtualAddress
            sec_file_len = DWORD.read(reader)       # SizeOfRawData
            sec_file_off = DWORD.read(reader)       # PointerToRawData
            reader.offset += 16
            self.sections.append((sec_rva, sec_file_off))
        self.sections.sort()

        self.dir_export = BinaryObject(self._extract_fixed(dir_export_rva, dir_export_len), alignment=16)
        if dir_resource_rva == 0:
            warn("no Resource directory in image")
        else:
            self.dir_resource = BinaryObject(self._extract_fixed(dir_resource_rva, dir_resource_len), alignment=16)

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
_RSRC_TABLE_ENTRY_OFFSETS = Dict[Union[int, str], Union[Tuple[int, int, int], '_RSRC_TABLE_ENTRY_OFFSETS']]


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


def _RSRC_ENTRY_read(reader: BinaryObjectReader) -> Tuple[int, int, int]:
    rva = DWORD.read(reader)
    len = DWORD.read(reader)
    cp = DWORD.read(reader)
    reader.read_or_warn(DWORD(0))  # reserved
    return rva, len, cp


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


def _RSRC_TABLE_read(reader: BinaryObjectReader) -> _RSRC_TABLE_ENTRIES:
    reader.read_or_warn(bytes(b"\0\0\0\0\0\0\0\0\0\0\0\0"))
    name_entries_len = WORD.read(reader)
    id_entries_len = WORD.read(reader)

    entries = {}

    for _ in range(name_entries_len):
        name_off = DWORD.read(reader)
        name_reader = BinaryObjectReader(reader.target, name_off)
        name_len = WORD.read(name_reader)
        name = name_reader.read_bytes(2 * name_len).decode('utf-16le')

        data_off = DWORD.read(reader)
        is_table = (data_off & 0x80000000) != 0
        data_off = data_off & 0x7FFFFFFF
        if is_table:
            data = _RSRC_TABLE_read(BinaryObjectReader(reader.target, data_off))
        else:
            data = _RSRC_ENTRY_read(BinaryObjectReader(reader.target, data_off))
        entries[name] = data

    for _ in range(id_entries_len):
        key = DWORD.read(reader)

        data_off = DWORD.read(reader)
        is_table = (data_off & 0x80000000) != 0
        data_off = data_off & 0x7FFFFFFF
        if is_table:
            data = _RSRC_TABLE_read(BinaryObjectReader(reader.target, data_off))
        else:
            data = _RSRC_ENTRY_read(BinaryObjectReader(reader.target, data_off))
        entries[key] = data

    return entries


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
