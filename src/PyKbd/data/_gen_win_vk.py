# This file is part of PyKbd
#
# Copyright (C) 2020  Nulano
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
from typing import Optional

from . import _version

__version__ = _version


@dataclass(frozen=True)
class Vk:
    code: int
    name: str
    reserved: bool = False
    """Reserved keys cannot be bound to a VSC."""
    mappable: bool = True
    """Function keys cannot have characters mapped to them."""
    extended: bool = False
    """Must have KBDEXT flag even if mapped to non-prefixed VSC."""
    comment: Optional[str] = None
    fake: bool = False
    """This key was generated by PyKbd and is not defined in Windows SDKs."""

    def __str__(self):
        return f"*{self.name}" if self.fake else self.name

    def __int__(self):
        return self.code
    
    def __lt__(self, other):
        if self.__class__ == other.__class__:
            return (translate(self.code), self.code) < (translate(other.code), other.code)
        return NotImplemented
    
    def __le__(self, other):
        if self.__class__ == other.__class__:
            return (translate(self.code), self.code) <= (translate(other.code), other.code)
        return NotImplemented
    
    def __gt__(self, other):
        if self.__class__ == other.__class__:
            return (translate(self.code), self.code) > (translate(other.code), other.code)
        return NotImplemented
    
    def __ge__(self, other):
        if self.__class__ == other.__class__:
            return (translate(self.code), self.code) >= (translate(other.code), other.code)
        return NotImplemented

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return self.code == other.code
        return NotImplemented

    def __hash__(self):
        return hash(self.code)

    def __repr__(self):
        r = f"Vk(code={hex(self.code)}, name={repr(self.name)}"
        if self.reserved:
            r += ", reserved=True"
        if not self.mappable:
            r += ", mappable=False"
        if self.extended:
            r += ", extended=True"
        if self.comment is not None:
            r += f", comment={repr(self.comment)}"
        if self.fake:
            r += ", fake=True"
        r += ")"
        return r


_reserved = {
    # mouse cannot be assigned to the keyboard
    "VK_LBUTTON",
    "VK_RBUTTON",
    "VK_MBUTTON",
    "VK_XBUTTON1",
    "VK_XBUTTON2",

    # use VK_L* or VK_R* instead
    "VK_SHIFT",
    "VK_CONTROL",
    "VK_MENU",

    # UI navigation (reserved)
    "VK_NAVIGATION_VIEW",
    "VK_NAVIGATION_MENU",
    "VK_NAVIGATION_UP",
    "VK_NAVIGATION_DOWN",
    "VK_NAVIGATION_LEFT",
    "VK_NAVIGATION_RIGHT",
    "VK_NAVIGATION_ACCEPT",
    "VK_NAVIGATION_CANCEL",

    # Gamepad input
    "VK_GAMEPAD_A",
    "VK_GAMEPAD_B",
    "VK_GAMEPAD_X",
    "VK_GAMEPAD_Y",
    "VK_GAMEPAD_RIGHT_SHOULDER",
    "VK_GAMEPAD_LEFT_SHOULDER",
    "VK_GAMEPAD_LEFT_TRIGGER",
    "VK_GAMEPAD_RIGHT_TRIGGER",
    "VK_GAMEPAD_DPAD_UP",
    "VK_GAMEPAD_DPAD_DOWN",
    "VK_GAMEPAD_DPAD_LEFT",
    "VK_GAMEPAD_DPAD_RIGHT",
    "VK_GAMEPAD_MENU",
    "VK_GAMEPAD_VIEW",
    "VK_GAMEPAD_LEFT_THUMBSTICK_BUTTON",
    "VK_GAMEPAD_RIGHT_THUMBSTICK_BUTTON",
    "VK_GAMEPAD_LEFT_THUMBSTICK_UP",
    "VK_GAMEPAD_LEFT_THUMBSTICK_DOWN",
    "VK_GAMEPAD_LEFT_THUMBSTICK_RIGHT",
    "VK_GAMEPAD_LEFT_THUMBSTICK_LEFT",
    "VK_GAMEPAD_RIGHT_THUMBSTICK_UP",
    "VK_GAMEPAD_RIGHT_THUMBSTICK_DOWN",
    "VK_GAMEPAD_RIGHT_THUMBSTICK_RIGHT",
    "VK_GAMEPAD_RIGHT_THUMBSTICK_LEFT",
}

_reserved_codes = {
    # after VK_LAUNCH_APP2
    0xB8, 0xB9,
    # after VK_OEM_3
    0xC1, 0xC2,
    # after VK_OEM_8
    0xE0,
    # VK__none_
    0xFF,
}

_function = {
    *_reserved,

    # modifier keys
    "VK_LSHIFT",
    "VK_RSHIFT",
    "VK_LCONTROL",
    "VK_RCONTROL",
    "VK_LMENU",
    "VK_RMENU",
    "VK_LWIN",
    "VK_RWIN",

    # toggle keys
    "VK_CAPITAL",
    "VK_KANA",
    "VK_HANGEUL",
    "VK_HANGUL",
    "VK_IME_ON",
    "VK_JUNJA",
    "VK_FINAL",
    "VK_HANJA",
    "VK_KANJI",
    "VK_IME_OFF",
    "VK_CONVERT",
    "VK_NONCONVERT",
    "VK_ACCEPT",
    "VK_MODECHANGE",
    "VK_NUMLOCK",
    "VK_SCROLL",

    # keys with special function
    "VK_PAUSE",
    "VK_PRIOR",
    "VK_NEXT",
    "VK_END",
    "VK_HOME",
    "VK_LEFT",
    "VK_UP",
    "VK_RIGHT",
    "VK_DOWN",
    "VK_SELECT",
    "VK_PRINT",
    "VK_EXECUTE",
    "VK_SNAPSHOT",
    "VK_INSERT",
    "VK_DELETE",
    "VK_HELP",
    "VK_APPS",
    "VK_SLEEP",

    # function keys
    "VK_F1",
    "VK_F2",
    "VK_F3",
    "VK_F4",
    "VK_F5",
    "VK_F6",
    "VK_F7",
    "VK_F8",
    "VK_F9",
    "VK_F10",
    "VK_F11",
    "VK_F12",
    "VK_F13",
    "VK_F14",
    "VK_F15",
    "VK_F16",
    "VK_F17",
    "VK_F18",
    "VK_F19",
    "VK_F20",
    "VK_F21",
    "VK_F22",
    "VK_F23",
    "VK_F24",

    # media keys
    "VK_BROWSER_BACK",
    "VK_BROWSER_FORWARD",
    "VK_BROWSER_REFRESH",
    "VK_BROWSER_STOP",
    "VK_BROWSER_SEARCH",
    "VK_BROWSER_FAVORITES",
    "VK_BROWSER_HOME",
    "VK_VOLUME_MUTE",
    "VK_VOLUME_DOWN",
    "VK_VOLUME_UP",
    "VK_MEDIA_NEXT_TRACK",
    "VK_MEDIA_PREV_TRACK",
    "VK_MEDIA_STOP",
    "VK_MEDIA_PLAY_PAUSE",
    "VK_LAUNCH_MAIL",
    "VK_LAUNCH_MEDIA_SELECT",
    "VK_LAUNCH_APP1",
    "VK_LAUNCH_APP2",

    # VK_ICO_00 has special handling
    # TODO is KBDSPECIAL needed?
    "VK_ICO_00",
}

KBDEXT = 0x100
KBDMULTIVK = 0x200
KBDSPECIAL = 0x400
KBDNUMPAD = 0x800

_extended = {
    # VK_R* must have KBDEXT to map to correct VK
    "VK_RWIN",
    "VK_RSHIFT",
    "VK_RCONTROL",
    "VK_RMENU",
    # VK_NUMLOCK must have KBDEXT due to VK_PAUSE name conflict
    "VK_NUMLOCK",
}

_multivk_101 = {
    "VK_CONTROL": {
        "VK_NUMLOCK": "VK_PAUSE",
        "VK_SCROLL": "VK_CANCEL",
    },
}

_multivk_84 = {
    "VK_SHIFT": {
        "VK_MULTIPLY": "VK_SNAPSHOT",
    },
    **_multivk_101,
}
_multivk_84["VK_MENU"] = _multivk_84["VK_SHIFT"]

_multivk_ibm102 = {
    "VK_SHIFT": {
        "VK_SCROLL": "VK_CANCEL",
        "VK_NUMLOCK": "VK_PAUSE",
    },
    "VK_CONTROL": {
        "VK_PAUSE": "VK_CANCEL",
        "VK_SCROLL": "VK_CANCEL",
    },
}

_multivk_tbl = {
    "101/102 key (type 4)": _multivk_101,
    "84-86 key (type 3)": _multivk_84,
    # TODO name and type number
    "IBM JP 102": _multivk_ibm102,
}

_multivk = {}


def _multivk_func():
    from collections import defaultdict
    conversions = defaultdict(set)
    for kbd, tbls in _multivk_tbl.items():
        for modifier, tbl in tbls.items():
            for base, conv in tbl.items():
                conversions[base].add(conv)
    for base, lst in conversions.items():
        comment = f"changes to {' or '.join(lst)} with a modifier"
        _multivk[base] = comment


_multivk_func()

_numpad = {
    # TODO is KBDSPECIAL needed?
    "VK_INSERT": "VK_NUMPAD0",
    "VK_END": "VK_NUMPAD1",
    "VK_DOWN": "VK_NUMPAD2",
    "VK_NEXT": "VK_NUMPAD3",
    "VK_LEFT": "VK_NUMPAD4",
    "VK_CLEAR": "VK_NUMPAD5",
    "VK_RIGHT": "VK_NUMPAD6",
    "VK_HOME": "VK_NUMPAD7",
    "VK_UP": "VK_NUMPAD8",
    "VK_PRIOR": "VK_NUMPAD9",
    "VK_DELETE": "VK_DECIMAL",
}

# keys possibly missing from WinUser.h
_extra = {
    Vk(0, "VK__end_", reserved=True, mappable=False, comment="end of keyboard table", fake=True),
    Vk(0x16, "VK_IME_ON", mappable=False),
    Vk(0x1A, "VK_IME_OFF", mappable=False),
    Vk(0xC1, "VK_ABNT_C1", comment="next to Right Shift on Brazillian keyboard"),
    Vk(0xC2, "VK_ABNT_C2", comment="next to Numpad Add on Brazillian keyboard"),
    Vk(0xFF, "VK__none_", reserved=True, mappable=False)
}

_translation = {}
_translation_reverse = {}


def translate(vk):
    """
    Translate KBDMULTIVK or KBDNUMPAD Vk or Vk.code.
    """
    is_vk = isinstance(vk, Vk)
    if not is_vk and not isinstance(vk, int):
        raise TypeError
    vk = _translation.get(vk, int(vk))
    if is_vk:
        vk = code_to_vk[vk]
    return vk


def untranslate(vk):
    """
    Reverse of ``translate()``.
    """
    is_vk = isinstance(vk, Vk)
    if not is_vk and not isinstance(vk, int):
        raise TypeError
    vk = _translation_reverse.get(vk, int(vk))
    if is_vk:
        vk = code_to_vk[vk]
    return vk


def _generate(f, winuser):
    # hide local imports from the generated file
    import re
    import string

    vk = {}

    # VK_0 - VK_9 are same as ASCII, comment only
    # VK_A - VK_Z are same as ASCII, comment only
    for c in string.digits + string.ascii_uppercase:
        name = f"VK_{c}"
        vk[name] = Vk(ord(c), name, fake=True)
    
    matcher = re.compile(r"^[ \t]*"
                         r"#[ \t]*(?:define|DEFINE)"
                         r"[ \t]+(VK_[A-Z0-9_]+)"
                         r"[ \t]+0x([0-9A-F]+)"
                         r"[ \t]*(?:/\*([^*]*)\*/|//(.*))?"
                         r"[ \t]*$")

    for line in winuser:
        m = matcher.match(line)
        if m:
            name, value = m.group(1), int(m.group(2), 16)
            comment = (m.group(3) or m.group(4) or "").strip() or None
            reserved = name in _reserved or value in _reserved_codes
            function = name in _function
            extended = name in _extended
            vk[name] = Vk(value, name, reserved, not function, extended, comment)

    for base, conv in _numpad.items():
        name = f"{conv}_{base[3:]}"
        base_vk = vk[base]
        translated = vk[conv]
        vk[name] = Vk(
            base_vk.code | KBDNUMPAD | KBDSPECIAL,
            name,
            mappable=False,
            comment=f"respects NumLock",
            fake=True,
        )
        _translation[vk[name].code] = translated.code
        _translation_reverse[translated.code] = vk[name].code

    for base, comment in _multivk.items():
        name = f"{base}_MULTIVK"
        base_vk = vk[base]
        vk[name] = Vk(
            base_vk.code | KBDMULTIVK,
            name,
            mappable=False,
            comment=comment,
            fake=True
        )
        _translation[vk[name].code] = base_vk.code
        _translation_reverse[base_vk.code] = vk[name].code

    for extra in _extra:
        if extra.name not in vk:
            vk[extra.name] = extra

    vk = {n: v for n, v in sorted(vk.items(), key=lambda x: x[1])}

    for name, value in vk.items():
        print(f"{name} = {repr(value)}", file=f)
    print(file=f)

    print("all = [", file=f)
    for name in vk:
        print(f"    {name},", file=f)
    print("]", file=f)
    print(file=f)

    print("valid = [", file=f)
    for name, value in vk.items():
        if not value.reserved:
            print(f"    {name},", file=f)
    print("]", file=f)
    print(file=f)

    print("mappable = [", file=f)
    for name, value in vk.items():
        if value.mappable:
            print(f"    {name},", file=f)
    print("]", file=f)
    print(file=f)

    print("name_to_vk = {", file=f)
    for name in vk:
        print(f'    "{name}": {name},', file=f)
    print("}", file=f)
    print(file=f)

    codes = {}
    print("code_to_vk = {", file=f)
    for name, value in vk.items():
        if value.code in codes:
            continue
        codes[value.code] = value
        print(f'    {hex(value.code)}: {name},', file=f)
    print("}", file=f)
    print(file=f)

    print(f"_translation = {repr(_translation)}", file=f)
    print(f"_translation_reverse = {repr(_translation_reverse)}", file=f)


if __name__ == '__main__':
    def _main():
        import sys
        dir, sep, file = __file__.rpartition("_gen_")
        if sep != "_gen_":
            raise RuntimeError("This is the generated file. "
                               "Please run the _gen_ version to regenerate it.")

        if len(sys.argv) != 2:
            raise RuntimeError("Please provide exactly one argument, path to WinUser.h.")

        with open(sys.argv[1], "r", encoding="ascii", errors="strict") as f:
            winuser = f.readlines()

        with open(dir + file, "w", encoding="ascii", errors="strict") as f:
            with open(__file__, "r", encoding="ascii", errors="strict") as s:
                f.write(s.read())
            print(file=f)
            _generate(f, winuser)

    _main()

# ----- start generated content -----