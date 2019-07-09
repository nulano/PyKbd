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

from typing import Optional

from .wintypes import *
from .linker_binary import BinaryObject, link


@dataclass()
class WinDll:
    layout: object
    architecture: Architecture

    timestamp: int
    filename: str

    kbdtables: Optional[BinaryObject] = None

    dir_export: Optional[BinaryObject] = None
    dir_resource: Optional[BinaryObject] = None
    dir_reloc: Optional[BinaryObject] = None

    sec_HEADER: Optional[BinaryObject] = None
    sec_data: Optional[BinaryObject] = None
    sec_rsrc: Optional[BinaryObject] = None
    sec_reloc: Optional[BinaryObject] = None

    data: Optional[bytes] = None

    def __init__(self, layout, architecture: Architecture):
        self.layout = layout
        self.architecture = architecture

        self.timestamp = 0  # TODO
        self.filename = 'kbdtst.dll'  # TODO

    def compile(self):
        self.compile_layout()
        self.compile_export_dir()
        self.compile_resource_dir()
        self.compile_reloc_dir()
        self.link()
        self.compile_header()
        self.assemble()

        return self.data

    def compile_layout(self):
        kbdtables = BinaryObject(alignment=self.architecture.pointer)

        # TODO

        self.kbdtables = kbdtables

    def compile_export_dir(self):
        func = BinaryObject(alignment=16)                           # -- KBDTABLES* KbdLayerDescriptor() --
        if self.architecture.pointer == 8:                          #
            func.append(BYTE(0x48))                                 # (if AMD64) REX ...
        func.append(BYTE(0xB8))                                     # MOV EAX, ...
        func.append(PTR(self.kbdtables, self.architecture, False))  # ... offset KbdLayerDescriptorTable
        if self.architecture == WOW64:                              #
            func.append(BYTE(0x99))                                 # (if WOW64) CDQ
        func.append(BYTE(0xC3))                                     # RET

        addresses = BinaryObject(alignment=4)
        addresses.append(RVA(func))

        names = BinaryObject(alignment=4)
        names.append(RVA(STR("KbdLayerDescriptor")))

        ordinals = BinaryObject(alignment=4)
        ordinals.append(WORD(0))

        export = BinaryObject(alignment=16)     # -- Export Directory --
        export.append(DWORD(0))                 # Export Flags (reserved)
        export.append(DWORD(self.timestamp))    # Timestamp
        export.append(WORD(0))                  # Major Version (unused)
        export.append(WORD(0))                  # Minor Version (unused)
        export.append(RVA(STR(self.filename)))  # Name RVA
        export.append(DWORD(1))                 # Ordinal Base
        export.append(DWORD(1))                 # Address Table Entries
        export.append(DWORD(1))                 # Number of Name Pointers
        export.append(RVA(addresses))           # Export Address Table RVA
        export.append(RVA(names))               # Name Pointer Table RVA
        export.append(RVA(ordinals))            # Ordinal Table RVA

        self.dir_export = export

    def compile_resource_dir(self):
        resource = BinaryObject(alignment=16)

        # TODO

        self.dir_resource = resource

    def compile_reloc_dir(self):
        reloc = BinaryObject()

        # TODO

        self.dir_reloc = reloc

    def link(self):
        # TODO

        pass

    def compile_header(self):
        header = BinaryObject(alignment=16)

        # TODO

        self.sec_HEADER = header

    def assemble(self):
        assembly = BinaryObject(self.sec_HEADER.data)
        assembly.append(self.sec_data)
        assembly.append(self.sec_rsrc)
        assembly.append(self.sec_reloc)
        assembly.append_padding(0x200)
        self.data = assembly.data
