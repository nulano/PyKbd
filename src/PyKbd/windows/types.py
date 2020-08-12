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

from dataclasses import dataclass, field
from typing import Annotated, TypeVar, Tuple, Optional

from . import _version


__version__ = _version


# ---------- Windows Integer Types ----------


@dataclass(frozen=True)
class _WinInt:
    sizeof: int
    signed: bool


BYTE = Annotated[int, _WinInt(1, signed=False)]
WORD = Annotated[int, _WinInt(2, signed=False)]
DWORD = Annotated[int, _WinInt(4, signed=False)]
QWORD = Annotated[int, _WinInt(8, signed=False)]

# CHAR = Annotated[int, _WinInt(1, signed=True)]
SHORT = Annotated[int, _WinInt(2, signed=True)]
INT = Annotated[int, _WinInt(4, signed=True)]
LONG = Annotated[int, _WinInt(4, signed=True)]
LONGLONG = Annotated[int, _WinInt(8, signed=True)]

UCHAR = Annotated[int, _WinInt(1, signed=False)]
USHORT = Annotated[int, _WinInt(2, signed=False)]
UINT = Annotated[int, _WinInt(4, signed=False)]
ULONG = Annotated[int, _WinInt(4, signed=False)]
ULONGLONG = Annotated[int, _WinInt(8, signed=False)]

MAKELONG = Tuple[WORD, WORD]


@dataclass(frozen=True)
class _WinIntPtr:
    signed: bool


DWORD_PTR = Annotated[int, _WinIntPtr(signed=False)]
UINT_PTR = Annotated[int, _WinIntPtr(signed=False)]
ULONG_PTR = Annotated[int, _WinIntPtr(signed=False)]

INT_PTR = Annotated[int, _WinIntPtr(signed=True)]
LONG_PTR = Annotated[int, _WinIntPtr(signed=True)]


# ---------- Windows Pointers ----------


@dataclass(frozen=True)
class _WinPtr:
    long: bool = False


PTR = Annotated[Optional[TypeVar("T")], _WinPtr(long=False)]
LPTR = Annotated[Optional[TypeVar("T")], _WinPtr(long=True)]


# ---------- Windows Arrays ----------


@dataclass(frozen=True)
class _Length:
    pass


@dataclass(frozen=True)
class _NullTerminated(_Length):
    pass


@dataclass(frozen=True)
class _LengthFixed(_Length):
    length: int


@dataclass(frozen=True)
class _LengthReferenced(_Length):
    reference: str
    add: int = 0
    mul: int = 1


P = LPTR[Annotated[list[TypeVar("T")], _NullTerminated()]]
"""Long Pointer to Null-Terminated Array."""


# ---------- Windows Strings ----------


@dataclass(frozen=True)
class _StrEncoding:
    encoding: str
    sizeof: int


CHAR_E = _StrEncoding("ascii", 1)
WCHAR_E = _StrEncoding("utf-16le", 2)

CHAR = Annotated[str, CHAR_E, _LengthFixed(1)]
WCHAR = Annotated[str, WCHAR_E, _LengthFixed(1)]

STR = Annotated[str, CHAR_E, _NullTerminated()]
WSTR = Annotated[str, WCHAR_E, _NullTerminated()]

LPSTR = LPTR[STR]
LPWSTR = LPTR[WSTR]

MAKELONG_WCHAR = Tuple[WCHAR, WCHAR]


# ---------- Keyboard Structs ----------


@dataclass()
class VK_TO_BIT:
    """
    VK_TO_BIT - associate a Virtual Key with a Modifier bitmask.

    Vk        - the Virtual key (eg: VK_SHIFT, VK_RMENU, VK_CONTROL etc.)
                Special Values:
                   0        null terminator
    ModBits   - a combination of KBDALT, KBDCTRL, KBDSHIFT and kbd-specific bits
                Any kbd-specific shift bits must be the lowest-order bits other
                than KBDSHIFT, KBDCTRL and KBDALT (0, 1 & 2)

    Those languages that use AltGr (VK_RMENU) to shift keys convert it to
    CTRL+ALT with the KBDSPECIAL bit in the ausVK[] entry for VK_RMENU
    and by having an entry in aVkToPfnOem[] to simulate the right Vk sequence.
    """
    Vk: BYTE = 0
    ModBits: BYTE = 0


@dataclass()
class MODIFIERS:
    """
    pModNumber  - a table to map shift bits to enumerated shift states

    Table attributes: Ordered table

    Maps all possible shifter key combinations to an enumerated shift state.
    The size of the table depends on the value of the highest order bit used
    in aCharModifiers[*].ModBits

    Special values for aModification[*]
      SHFT_INVALID - no characters produced with this shift state.
    LATER: (ianja) no SHFT_CTRL - control characters encoded in tables like others
      SHFT_CTRL    - standard control character production (all keyboards must
                     be able to produce CTRL-C == 0x0003 etc.)
      Other        - enumerated shift state (not less than 0)

    This table is indexed by the Modifier Bits to obtain an Modification Number.

                           CONTROL MENU SHIFT

       aModification[] = {
           0,            //   0     0     0     = 000  <none>
           1,            //   0     0     1     = 001  SHIFT
           SHFT_INVALID, //   0     1     0     = 010  ALT
           2,            //   0     1     1     = 011  SHIFT ALT
           3,            //   1     0     0     = 100  CTRL
           4,            //   1     0     1     = 101  SHIFT CTRL
           5,            //   1     1     0     = 110  CTRL ALT
           SHFT_INVALID  //   1     1     1     = 111  SHIFT CTRL ALT
       };
    """
    pVkToBit: P[VK_TO_BIT] = None
    wMaxModBits: WORD = 0
    ModNumber: Annotated[list[BYTE], _LengthReferenced("wMaxModBits", add=1)] = field(default_factory=list)


@dataclass()
class VSC_VK:
    """
    VSC_VK     - Associate a Virtual Scancode with a Virtual Key
     Vsc - Virtual Scancode
     Vk  - Virtual Key | flags
    Used by VKFromVSC() for scancodes prefixed 0xE0 or 0xE1
    """
    Vsc: BYTE = 0
    Vk: USHORT = 0


@dataclass()
class VK_TO_WCHARS:
    """
    VK_TO_WCHARS<n> - Associate a Virtual Key with <n> UNICODE characters

    VirtualKey  - The Virtual Key.
    wch[]       - An array of characters, one for each shift state that
                  applies to the specified Virtual Key.

    Special values for VirtualKey:
       -1        - This entry contains dead chars for the previous entry
       0         - Terminates a VK_TO_WCHARS[] table

    Special values for Attributes:
       CAPLOK    - The CAPS-LOCK key affects this key like SHIFT
       SGCAPS    - CapsLock uppercases the unshifted char (Swiss-German)

    Special values for wch[*]:
       WCH_NONE  - No character is generated by pressing this key with the
                   current shift state.
       WCH_DEAD  - The character is a dead-key: the next VK_TO_WCHARS[] entry
                   will contain the values of the dead characters (diaresis)
                   that can be produced by the Virtual Key.
       WCH_LGTR  - The character is a ligature.  The characters generated by
                   this keystroke are found in the ligature table.
    """
    VirtualKey: BYTE = 0
    Attributes: BYTE = 0
    wch: Annotated[list[WCHAR], _Length()] = field(default_factory=list)

    def __len__(self):
        return len(self.wch)


@dataclass()
class VK_TO_WCHAR_TABLE:
    """
    VK_TO_WCHAR_TABLE - Describe a table of VK_TO_WCHARS1

    pVkToWchars     - points to the table.
    nModifications  - the number of shift-states supported by this table.
                      (this is the number of elements in pVkToWchars[*].wch[])

    A keyboard may have several such tables: all keys with the same number of
       shift-states are grouped together in one table.

    Special values for pVktoWchars:
        NULL     - Terminates a VK_TO_WCHAR_TABLE[] list.
    """
    pVkToWchars: P[Annotated[VK_TO_WCHARS, _LengthReferenced("nModifications")]] = None
    nModifications: BYTE = 0
    cbSize: BYTE = 0


@dataclass()
class DEADKEY:
    dwBoth: MAKELONG_WCHAR = 0
    wchComposed: WCHAR = "\0"
    uFlags: USHORT = 0


@dataclass()
class LIGATURE:
    VirtualKey: BYTE = 0
    ModificationNumber: WORD = 0
    wch: Annotated[list[WCHAR], _Length()] = field(default_factory=list)

    def __len__(self):
        return len(self.wch)


@dataclass()
class VSC_LPWSTR:
    vsc: BYTE = 0
    pwsz: LPWSTR = " "


@dataclass()
class DEADKEY_LPWSTR:
    """*Defined as WSTR in kbd.h*"""
    deadkey: WCHAR = "\0"
    name: WSTR = " "


@dataclass()
class KBDTABLES:
    # Modifier keys
    pCharModifiers: LPTR[MODIFIERS] = None

    # Characters
    pVkToWcharTable: P[VK_TO_WCHAR_TABLE] = None

    # Diacritics
    pDeadKey: P[DEADKEY] = None

    # Names of Keys
    pKeyNames: P[VSC_LPWSTR] = None
    pKeyNamesExt: P[VSC_LPWSTR] = None
    pKeyNamesDead: P[LPTR[DEADKEY_LPWSTR]] = None

    # Scan codes to Virtual Keys
    pusVSCtoVK: LPTR[Annotated[list[USHORT], _LengthReferenced("bMaxVSCtoVK")]] = None
    bMaxVSCtoVK: BYTE = 0
    pVSCtoVK_E0: P[VSC_VK] = None
    pVSCtoVK_E1: P[VSC_VK] = None

    # Locale-specific special processing
    # High word is version number
    fLocaleFlags: MAKELONG = 0

    # Ligatures
    nLgMax: BYTE = 0
    cbLgEntry: BYTE = 0
    pLigature: LPTR[Annotated[
        list[LPTR[Annotated[LIGATURE, _LengthReferenced("cbLgEntry")]]],
        _LengthReferenced("nLgMax"),
    ]] = None

    # Type and subtype. These are optional.
    dwType: DWORD = 0
    dwSubType: DWORD = 0
