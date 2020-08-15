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

import dataclasses
from warnings import warn

from .types import *
from ..layout import Layout, KeyCode, ScanCode, ShiftState, Character, KeyAttributes, DeadKey

from . import _version


__version__ = _version


def compile(layout: Layout) -> KBDTABLES:
    kbdtables = KBDTABLES()
    
    kbdtables.fLocaleFlags = (1, 1)
    kbdtables.dwType = 0
    kbdtables.dwSubType = 0
    
    compile_kbd_keymap(kbdtables, layout)
    compile_kbd_charmap(kbdtables, layout)
    
    return kbdtables


def compile_kbd_keymap(kbdtables: KBDTABLES, layout: Layout):
    vsc_to_vk = [0xFF]
    for vsc in range(1, max(map(lambda k: k.code, filter(lambda k: k.prefix == 0, layout.keymap))) + 1):
        key = layout.keymap.get(ScanCode(vsc), KeyCode(0xFF))
        vsc_to_vk.append(key.win_vk)
    kbdtables.pusVSCtoVK = vsc_to_vk
    kbdtables.bMaxVSCtoVK = len(vsc_to_vk)

    key_names = []
    key_names_ext = []
    vsc_to_vk_e0 = []
    vsc_to_vk_e1 = []
    for scan_code, key_code in layout.keymap.items():
        if scan_code.prefix == 0xE0:
            vsc_to_vk_e0.append(VSC_VK(scan_code.code, key_code.win_vk))
        elif scan_code.prefix == 0xE1:
            vsc_to_vk_e1.append(VSC_VK(scan_code.code, key_code.win_vk))
        if key_code.name:
            # Pause (E1-1D-45)
            if scan_code == ScanCode(0x1D, 0xE1):
                key_names.append(VSC_LPWSTR(0x45, key_code.name))
            # extended (E0-XX) or NumLock (45); (E0-45) is not in use
            elif scan_code.prefix == 0xE0 or scan_code.code == 0x45:
                key_names_ext.append(VSC_LPWSTR(scan_code.code, key_code.name))
            else:
                key_names.append(VSC_LPWSTR(scan_code.code, key_code.name))
    kbdtables.pKeyNames = key_names
    kbdtables.pKeyNamesExt = key_names_ext
    kbdtables.pVSCtoVK_E0 = vsc_to_vk_e0
    kbdtables.pVSCtoVK_E1 = vsc_to_vk_e1


def compile_kbd_charmap(kbdtables: KBDTABLES, layout: Layout):
    vk_to_bits = [
        VK_TO_BIT(0x10, 1), VK_TO_BIT(0x11, 2), VK_TO_BIT(0x12, 4), VK_TO_BIT(0x15, 8)
    ]

    max_mask = 0
    shift_states = []
    shift_state_map = {}
    vk_attributes = {}
    for scancode, keycode in layout.keymap.items():
        vk = KeyCode.translate_vk(keycode.win_vk)
        if vk in (0, 0xFF) or len(layout.charmap.get(vk, {})) == 0:
            continue
        elif vk > 0xFF:
            warn("unknown special vk, skipping: 0x%X" % vk)
            continue
        vk_attributes[vk] = keycode.attributes
        for shiftstate, character in layout.charmap[vk].items():
            shiftstate = dataclasses.replace(shiftstate, capslock=False)
            if shiftstate not in shift_state_map:
                shift_state_map[shiftstate] = len(shift_state_map)
                shift_states.append(shiftstate)
                max_mask = max(max_mask, shiftstate.to_bits())

    # XXX it might be possible to use more columns if we skip column 15 (invalid)
    if len(shift_state_map) >= 15:
        raise RuntimeError("Too many shift states: %i >= 15" % len(shift_state_map))
    elif len(shift_state_map) > 10:
        warn("Too many shift states: %i > 10" % len(shift_state_map))

    modifiers = MODIFIERS(
        vk_to_bits,
        max_mask,
        [
            shift_state_map.get(ShiftState.from_bits(mask), 0xF)
            for mask in range(max_mask + 1)
        ],
    )
    kbdtables.pCharModifiers = modifiers

    vk_to_wchars = []
    for vk, attributes in sorted(vk_attributes.items(), key=lambda e: KeyCode.untranslate_vk(e[0])):
        characters = layout.charmap[vk]

        secondary = {}
        dead = {shiftstate: character.char
                for shiftstate, character in characters.items()
                if character.dead and not shiftstate.capslock}

        if attributes.capslock_secondary:
            if dead:
                warn("CAPSLOCK_SECONDARY is incompatible with dead keys, ignoring")
                attributes = dataclasses.replace(attributes, capslock_secondary=False)
            else:
                secondary = {dataclasses.replace(shiftstate, capslock=False): character
                             for shiftstate, character in characters.items()
                             if shiftstate.capslock}
                # while unusual, deadkeys are valid in secondary capslock layer
                dead = {dataclasses.replace(shiftstate, capslock=False): character
                        for shiftstate, character in characters.items()
                        if character.dead and shiftstate.capslock}

        # base row
        row = VK_TO_WCHARS(vk, attributes.to_bits(), [])
        for shiftstate in range(len(shift_states)):
            character = characters.get(shift_states[shiftstate], Character("\uF000"))  # WCH_NONE
            if character.dead:
                character = Character("\uF001")  # WCH_DEAD
            row.wch.append(character.char)
        vk_to_wchars.append(row)

        # secondary capslock row (SGCAPS)
        if attributes.capslock_secondary:
            row = VK_TO_WCHARS(vk, 0, [])
            for shiftstate in range(len(shift_states)):
                character = secondary.get(shift_states[shiftstate], Character("\uF000"))  # WCH_NONE
                if character.dead:
                    character = Character("\uF001")  # WCH_DEAD
                row.wch.append(character.char)
            vk_to_wchars.append(row)

        # dead keys row
        if dead:
            row = VK_TO_WCHARS(0xFF, 0, [
                dead.get(shift_states[shiftstate], "\uF000")
                for shiftstate in range(len(shift_states)) 
            ])
            vk_to_wchars.append(row)

    vk_to_wchar_table = VK_TO_WCHAR_TABLE(
        vk_to_wchars,
        len(shift_states),
        len(shift_states) * 2 + 2,
    )
    kbdtables.pVkToWcharTable = [vk_to_wchar_table]

    dead_key = [
        DEADKEY(
            (character, accent),
            composed.char,
            1 if composed.dead else 0,
        )
        for accent, key in layout.deadkeys.items()
        for character, composed in key.charmap.items()
    ]
    kbdtables.pDeadKey = dead_key

    key_names_dead = [
        DEADKEY_LPWSTR(accent, key.name)
        for accent, key in layout.deadkeys.items()
    ]
    kbdtables.pKeyNamesDead = key_names_dead
    
    kbdtables.nLgMax = 0
    kbdtables.cbLgEntry = 0
    kbdtables.pLigature = None


def decompile(kbdtables: KBDTABLES) -> Layout:
    layout = Layout()

    # TODO fLocaleFlags, pLigature, dwType, dwSubType

    decompile_kbd_keymap(kbdtables, layout)
    decompile_kbd_charmap(kbdtables, layout)

    return layout


def decompile_kbd_keymap(kbdtables: KBDTABLES, layout: Layout):
    names, names_ext = {}, {}
    for k, n in ((kbdtables.pKeyNames, names), (kbdtables.pKeyNamesExt, names_ext)):
        if k is not None:
            for row in k:
                if row.vsc in n and n[row.vsc] != row.pwsz:
                    warn("skipping duplicate name for vsc: 0x%X" % row.vsc)
                    continue
                n[row.vsc] = row.pwsz

    def get_keycode(scancode, vk):
        # Pause (E1-1D-45)
        if scancode == ScanCode(0x1D, 0xE1):
            return KeyCode(vk, names.get(0x45))
        # extended (E0-XX) or NumLock (45); (E0-45) is not in use
        elif scancode.prefix == 0xE0 or scancode.code == 0x45:
            return KeyCode(vk, names_ext.get(scancode.code))
        else:
            return KeyCode(vk, names.get(scancode.code))

    layout.keymap = {
        ScanCode(vsc): get_keycode(ScanCode(vsc), vk)
        for vsc, vk in enumerate(kbdtables.pusVSCtoVK)
        if vk not in (0, 0xFF)
    } | {
        ScanCode(vsc_vk.Vsc, 0xE0): get_keycode(ScanCode(vsc_vk.Vsc, 0xE0), vsc_vk.Vk)
        for vsc_vk in kbdtables.pVSCtoVK_E0
    } | {
        ScanCode(vsc_vk.Vsc, 0xE1): get_keycode(ScanCode(vsc_vk.Vsc, 0xE1), vsc_vk.Vk)
        for vsc_vk in kbdtables.pVSCtoVK_E1
    }


def decompile_kbd_charmap(kbdtables: KBDTABLES, layout: Layout):
    layout.charmap = {}
    layout.deadkeys = {}

    bit_to_vk = {
        vk_to_bit.ModBits: vk_to_bit.Vk
        for vk_to_bit in kbdtables.pCharModifiers.pVkToBit
    }

    shift_state_map = {
        column: ShiftState.from_bits(mask)
        for mask, column in enumerate(kbdtables.pCharModifiers.ModNumber)
        if column != 0x0F
    }

    attributes_update = {}
    for vk_to_wchar_table in kbdtables.pVkToWcharTable:
        row = 0
        while row < len(vk_to_wchar_table.pVkToWchars):
            the_row = vk_to_wchar_table.pVkToWchars[row]
            vk = the_row.VirtualKey
            attributes = KeyAttributes.from_bits(the_row.Attributes)
            if vk == 0xFF:
                warn("unexpected dead key continuation line")
                continue
            dead = {}
            characters = {}
            for col, char in enumerate(the_row.wch):
                shiftstate = shift_state_map[col]
                character = Character(char)
                if character.char == "\uF000":  # Null
                    pass
                elif character.char == "\uF001":  # Dead
                    if attributes.capslock_secondary:
                        warn("ignoring dead key for key with SGCAPS: 0x%X" % vk)
                    else:
                        dead[col] = True
                elif character.char == "\uF002":  # Ligature
                    warn("ligature detected, skipping")
                else:
                    characters[shiftstate] = character
            row += 1
            if attributes.capslock_secondary:
                the_row = vk_to_wchar_table.pVkToWchars[row]
                if the_row.VirtualKey != vk:
                    warn("expected SGCAPS continuation, not 0x%X" % the_row.VirtualKey)
                if the_row.Attributes != 0:
                    warn("expected 0 Attributes, not 0x%X" % the_row.Attributes)
                for col, char in enumerate(the_row.wch):
                    shiftstate = dataclasses.replace(shift_state_map[col], capslock=True)
                    character = Character(char)
                    if character.char == "\uF000":  # Null
                        pass
                    elif character.char == "\uF001":  # Dead
                        dead[col] = True
                    elif character.char == "\uF002":  # Ligature
                        warn("ligature detected, skipping")
                    else:
                        characters[shiftstate] = character
                row += 1
            if dead:
                the_row = vk_to_wchar_table.pVkToWchars[row]
                if the_row.VirtualKey != 0xFF:
                    warn("expected WCH_DEAD continuation, not 0x%X" % the_row.VirtualKey)
                if the_row.Attributes != 0:
                    warn("expected 0 Attributes, not 0x%X" % the_row.Attributes)
                for col, char in enumerate(the_row.wch):
                    if not dead.get(col, False):
                        if char != "\uF000":
                            warn("expected WCH_NONE, not 0x%X" % ord(char))
                    else:
                        shiftstate = dataclasses.replace(shift_state_map[col], capslock=attributes.capslock_secondary)
                        character = Character(char, True)
                        if character.char in "\uF000\uF001\uF002":
                            warn("dead key maps to invalid character")
                        else:
                            characters[shiftstate] = character
                row += 1
            if vk in layout.charmap:
                warn("duplicate keycode, skipping: 0x%X" % vk)
                continue
            layout.charmap[vk] = characters
            attributes_update[vk] = attributes
    layout.keymap = {
        scancode: dataclasses.replace(keycode, attributes=attributes_update.get(keycode.win_vk, KeyAttributes()))
        for scancode, keycode in layout.keymap.items()
    }

    dead_key_names = {}
    if kbdtables.pKeyNamesDead is not None:
        dead_key_names = {
            deadkey.deadkey: deadkey.name
            for deadkey in kbdtables.pKeyNamesDead
        }

    if kbdtables.pDeadKey is not None:
        for deadkey in kbdtables.pDeadKey:
            character, accent = deadkey.dwBoth
            composed_char = deadkey.wchComposed
            composed_attr = deadkey.uFlags
            if composed_attr > 1:
                warn("unknown dead key attributes: 0x%x" % composed_attr)
            composed = Character(composed_char, composed_attr == 1)
            if accent not in layout.deadkeys:
                layout.deadkeys[accent] = DeadKey(dead_key_names.get(accent, accent), {})
            if character in layout.deadkeys[accent].charmap:
                warn("skipping duplicate dead key: '%s' + '%s'" % (accent, character))
                continue
            layout.deadkeys[accent].charmap[character] = composed

