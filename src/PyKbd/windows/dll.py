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

import typing
from collections import defaultdict
from dataclasses import dataclass, field, is_dataclass
from operator import itemgetter

from ..layout import Layout
from ..linker_binary import BinaryObject, BinaryObjectReader, Symbol, link
from . import _version, _version_num, compiler
from .types import (
    CHAR_E,
    DWORD,
    DWORD_PTR,
    FIXEDFILEINFO,
    MAKELONG,
    MAKEWORD,
    RVA,
    STR,
    WORD,
    WSTR,
    Resource,
    _Length,
    _LengthExpr,
    _LengthFixed,
    _LengthReferenced,
    _NullTerminated,
    _StrEncoding,
    _WinInt,
    _WinIntPtr,
    _WinPtr,
)

__version__ = _version


@dataclass(frozen=True)
class Offset(Symbol):
    target: typing.Optional[BinaryObject]
    sizeof: int

    def transform(self, offset):
        return offset

    def __call__(self) -> BinaryObject:
        offset = 0
        if self.target is not None:
            offset = self.transform((self.target.find_placement() or (None, 0))[1])
        return Assembler(self.sizeof)._compile(offset, DWORD_PTR)


@dataclass(frozen=True)
class Pointer(Offset):
    target: typing.Optional[BinaryObject]
    sizeof: int
    offset: int

    def transform(self, offset):
        return self.offset + offset


@dataclass()
class Assembler:
    ptr_size: int

    def _alignment(self, tp, *annotations):
        annotations = list(annotations)
        if annotations:
            annotation = annotations.pop()
            if isinstance(annotation, (_WinInt, _StrEncoding)):
                return annotation.sizeof
            elif isinstance(annotation, _WinPtr) and annotation.sizeof != 0:
                return annotation.sizeof
            elif isinstance(annotation, (_WinIntPtr, _WinPtr)):
                return self.ptr_size
            elif isinstance(annotation, _Length):
                return self._alignment(tp, *annotations)
            else:
                raise NotImplementedError(annotation)
        elif typing.get_origin(tp) is tuple:
            return sum(self._alignment(tp) for tp in typing.get_args(tp))
        elif typing.get_origin(tp) is typing.Annotated:
            return self._alignment(*typing.get_args(tp))
        elif typing.get_origin(tp) is list:
            tp, = typing.get_args(tp)
            return self._alignment(tp)
        elif is_dataclass(tp):
            fields = typing.get_type_hints(tp, include_extras=True)
            return max(self._alignment(tp) for tp in fields.values())
        else:
            raise NotImplementedError(tp)

    def _compile(self, obj, tp, *annotations, **ctx):
        annotations = list(annotations)
        if annotations:
            annotation = annotations.pop()
            if isinstance(annotation, (_WinInt, _WinIntPtr)):
                if isinstance(annotation, _WinIntPtr):
                    annotation = _WinInt(self.ptr_size, annotation.signed)
                assert len(annotations) == 0
                assert tp is int
                assert isinstance(obj, int)
                return BinaryObject(obj.to_bytes(
                    annotation.sizeof,
                    byteorder="little",
                    signed=annotation.signed,
                ), alignment=annotation.sizeof)
            elif isinstance(annotation, _WinPtr):
                assert len(annotations) == 0
                assert typing.get_origin(tp) is typing.Union
                tp, none = typing.get_args(tp)
                assert none == type(None)
                if obj is not None:
                    tgt = self._compile(obj, tp, **ctx)
                else:
                    tgt = None
                if annotation.sizeof == 0:
                    return Offset(tgt, self.ptr_size)
                else:
                    return Offset(tgt, annotation.sizeof)
            elif isinstance(annotation, _Length):
                if type(annotation) is _Length:
                    assert len(obj) == ctx["__length"]
                elif isinstance(annotation, _LengthReferenced):
                    l = ctx[annotation.reference] * annotation.mul + annotation.add
                    assert isinstance(l, int) or l.is_integer()
                    assert len(obj) == int(l)
                    ctx["__length"] = int(l)
                elif isinstance(annotation, _LengthExpr):
                    l = eval(annotation.expr, globals(), ctx)
                    assert isinstance(l, int)
                    assert len(obj) == l
                    ctx["__length"] = int(l)
                elif isinstance(annotation, _LengthFixed):
                    ctx["__length"] = annotation.length
                    assert len(obj) == ctx["__length"]
                elif isinstance(annotation, _NullTerminated):
                    assert len(obj) > 0, "zero-length null-terminated objects not supported"
                else:
                    raise NotImplementedError(annotation)
                compiled = self._compile(obj, tp, *annotations, **ctx)
                if isinstance(annotation, _NullTerminated):
                    element_cnt = len(obj)
                    assert isinstance(compiled, BinaryObject)
                    compiled.append_padding(compiled.alignment)
                    element_len = len(compiled.data) // element_cnt
                    assert len(compiled.data) % element_len == 0
                    compiled.append(b"\0" * element_len)
                return compiled
            elif isinstance(annotation, _StrEncoding):
                assert len(annotations) == 0
                assert tp is str
                assert isinstance(obj, str)
                bts = obj.encode(annotation.encoding, errors="strict")
                if len(bts) != len(obj) * annotation.sizeof:
                    raise UnicodeError("unsupported characters in object")
                return BinaryObject(bts, alignment=annotation.sizeof)
            else:
                raise NotImplementedError(annotation)
        elif typing.get_origin(tp) is tuple:
            tps = typing.get_args(tp)
            assert isinstance(obj, tuple)
            assert len(obj) == len(tps)
            out = BinaryObject(alignment=self._alignment(tp))
            for tp, v in zip(tps, obj):
                out.append(self._compile(v, tp))
            return out
        elif typing.get_origin(tp) is typing.Annotated:
            return self._compile(obj, *typing.get_args(tp), **ctx)
        elif tp is bytes:
            assert isinstance(obj, bytes)
            return BinaryObject(obj)
        elif tp is BinaryObject:
            assert isinstance(obj, BinaryObject)
            return obj
        elif typing.get_origin(tp) is list:
            assert isinstance(obj, list)
            tp, = typing.get_args(tp)
            alignment = None
            out = BinaryObject()
            for e in obj:
                v = self._compile(e, tp, **ctx)
                if alignment is None:
                    if isinstance(v, Offset):
                        alignment = v.sizeof
                    else:
                        alignment = v.alignment
                    out.alignment = alignment
                assert (isinstance(v, Offset) and v.sizeof or v.alignment) == alignment
                out.append(v)
            return out
        elif is_dataclass(tp):
            assert isinstance(obj, tp)
            values = []
            fields = typing.get_type_hints(tp, include_extras=True)
            ctx2 = obj.__dict__
            if "__length" in ctx:
                ctx2["__length"] = ctx["__length"]
            for name, type_hint in fields.items():
                values.append(self._compile(getattr(obj, name), type_hint, **ctx2))
            alignment = 0
            for val in values:
                if isinstance(val, Offset):
                    alignment = max(alignment, val.sizeof)
                else:
                    assert isinstance(val, BinaryObject)
                    alignment = max(alignment, val.alignment)
            out = BinaryObject(alignment=alignment)
            for val in values:
                out.append(val)
            return out
        else:
            raise NotImplementedError(tp)

    def compile(self, obj):
        """Compile struct"""
        return self._compile(obj, type(obj))

    def _decompile(self, data: BinaryObjectReader, tp, *annotations, **ctx):
        annotations = list(annotations)
        if annotations:
            annotation = annotations.pop()
            if isinstance(annotation, (_WinInt, _WinIntPtr)):
                if isinstance(annotation, _WinIntPtr):
                    annotation = _WinInt(self.ptr_size, annotation.signed)
                assert len(annotations) == 0
                assert tp is int
                return int.from_bytes(
                    data.read_bytes(annotation.sizeof, annotation.sizeof),
                    byteorder="little",
                    signed=annotation.signed,
                )
            elif isinstance(annotation, _WinPtr):
                assert len(annotations) == 0
                assert typing.get_origin(tp) is typing.Union
                tp, none = typing.get_args(tp)
                assert none == type(None)
                if annotation.sizeof == 0:
                    addr = self._decompile(data, DWORD_PTR)
                else:
                    addr = self._decompile(data, int, _WinInt(annotation.sizeof, False))
                if addr != 0:
                    return self._decompile(BinaryObjectReader(data.target, addr - ctx["__base"]), tp, *annotations, **ctx)
                else:
                    return None
            elif isinstance(annotation, _Length):
                if type(annotation) is _Length:
                    pass
                elif isinstance(annotation, _LengthReferenced):
                    l = ctx[annotation.reference] * annotation.mul + annotation.add
                    assert isinstance(l, int) or l.is_integer()
                    ctx["__length"] = int(l)
                elif isinstance(annotation, _LengthExpr):
                    l = eval(annotation.expr, globals(), ctx)
                    assert isinstance(l, int)
                    ctx["__length"] = int(l)
                elif isinstance(annotation, _LengthFixed):
                    ctx["__length"] = annotation.length
                elif isinstance(annotation, _NullTerminated):
                    ctx["__length"] = _NullTerminated()
                else:
                    raise NotImplementedError(annotation)
                return self._decompile(data, tp, *annotations, **ctx)
            elif isinstance(annotation, _StrEncoding):
                assert len(annotations) == 0
                assert tp is str
                if isinstance(ctx["__length"], _NullTerminated):
                    end = b"\0" * annotation.sizeof
                    bts = bytearray()
                    while True:
                        char = data.read_bytes(annotation.sizeof, annotation.sizeof)
                        if char == end:
                            break
                        bts.extend(char)
                    ctx["__length"] = len(bts) // annotation.sizeof
                else:
                    bts = data.read_bytes(ctx["__length"] * annotation.sizeof, annotation.sizeof)
                s = bts.decode(annotation.encoding, errors="strict")
                if len(bts) != len(s) * annotation.sizeof:
                    raise UnicodeError("read incorrect")
                return s
            else:
                raise NotImplementedError(annotation)
        elif typing.get_origin(tp) is tuple:
            data.read_padding(self._alignment(tp))
            return tuple(self._decompile(data, tp) for tp in typing.get_args(tp))
        elif typing.get_origin(tp) is typing.Annotated:
            return self._decompile(data, *typing.get_args(tp), **ctx)
        elif tp is bytes:
            if isinstance(ctx["__length"], _NullTerminated):
                bts = bytearray()
                while True:
                    b = data.read_bytes(1)
                    if b == b"\0":
                        ctx["__length"] = len(bts)
                        return bts
                    bts.append(b)
            else:
                return data.read_bytes(ctx["__length"])
        elif tp is BinaryObject:
            d = self._decompile(data, bytes, **ctx)
            return BinaryObject(d)
        elif typing.get_origin(tp) is list:
            tp, = typing.get_args(tp)
            if not isinstance(ctx["__length"], _NullTerminated):
                return [self._decompile(data, tp, **ctx) for _ in range(ctx["__length"])]
            else:
                alignment = self._alignment(tp)
                out = []
                data.read_padding(alignment)
                reader = BinaryObjectReader(data.target, data.offset)
                off = data.offset
                v = self._decompile(data, tp, **ctx)
                end = b"\0" * (data.offset - off)
                while reader.read_bytes(len(end), alignment) != end:
                    assert reader.offset == data.offset
                    out.append(v)
                    v = self._decompile(data, tp, **ctx)
                return out
        elif is_dataclass(tp):
            data.read_padding(self._alignment(tp))
            # delay PTRs to allow referenced length to follow the pointer
            delayed = {}
            out = tp()
            fields = typing.get_type_hints(tp, include_extras=True)
            ctx2 = {}
            if "__length" in ctx:
                ctx2["__length"] = ctx["__length"]
            if "__base" in ctx:
                ctx2["__base"] = ctx["__base"]
            for name, type_hint in fields.items():
                if typing.get_origin(type_hint) is typing.Annotated and \
                        isinstance(typing.get_args(type_hint)[-1], _WinPtr):
                    delayed[name] = (BinaryObjectReader(data.target, data.offset), type_hint)
                    if typing.get_args(type_hint)[-1].sizeof == 0:
                        self._decompile(data, DWORD_PTR)
                    else:
                        self._decompile(data, int, _WinInt(typing.get_args(type_hint)[-1].sizeof, False))
                else:
                    value = self._decompile(data, type_hint, **ctx2)
                    setattr(out, name, value)
                    ctx2[name] = value
            for name, (dt, type_hint) in delayed.items():
                value = self._decompile(dt, type_hint, **ctx2)
                setattr(out, name, value)
                ctx2[name] = value
            return out
        else:
            raise NotImplementedError(tp)

    def decompile(self, data, tp, off=0, base=0):
        """Compile struct"""
        if not isinstance(data, BinaryObject):
            data = BinaryObject(data)
        return self._decompile(BinaryObjectReader(data, off), tp, __base=base)


def _aligned_next(addr, align):
    return addr + (-addr) % align


@dataclass()
class ResourceNode:
    wLength: WORD = 0
    wValueLength: WORD = 0
    wType: WORD = 1
    szKey: WSTR = "\0"
    Value: typing.Annotated[BinaryObject, _LengthExpr("wValueLength << wType")] = field(default_factory=BinaryObject)
    Children: typing.Annotated[
        BinaryObject, _LengthExpr(
            "wLength - 8"
            " - ((2 * len(szKey) + 3) & 0x1FFFC)"
            " - (((wValueLength << wType) + 3) & 0x1FFFC)"
        )
    ] = field(default_factory=BinaryObject)


@dataclass()
class ResourceEntry:
    Data: RVA[typing.Annotated[BinaryObject, _LengthReferenced("Size")]] = None
    Size: DWORD = 0
    Codepage: DWORD = 0
    Reserved: DWORD = 0


@dataclass()
class ResourceTableRow:
    ID: DWORD
    Entry: DWORD


@dataclass()
class ResourceTable:
    Characteristicts: DWORD = 0
    TimeDateStamp: DWORD = 0
    Version: MAKELONG = (0, 0)
    NumberOfNameEntries: WORD = 0
    NumberOfIDEntries: WORD = 0
    NameEntries: typing.Annotated[list[ResourceTableRow], _LengthReferenced("NumberOfNameEntries")] = field(default_factory=list)
    IDEntries: typing.Annotated[list[ResourceTableRow], _LengthReferenced("NumberOfIDEntries")] = field(default_factory=list)


@dataclass()
class VS_FIXEDFILEINFO:
    dwSignature: DWORD = 0xFEEF04BD
    dwStrucVersion: MAKELONG = (0, 1)
    dwFileVersionMS: MAKELONG = (0, 1)
    dwFileVersionLS: MAKELONG = (0, 0)
    dwProductVersionMS: MAKELONG = (0, 1)
    dwProductVersionLS: MAKELONG = (0, 0)
    dwFileFlagsMask: DWORD = 0
    dwFileFlags: DWORD = 0
    dwFileOS: DWORD = 0
    dwFileType: DWORD = 0
    dwFileSubtype: DWORD = 0
    dwFileDateMS: DWORD = 0
    dwFileDateLS: DWORD = 0


@dataclass()
class ResourceCompiler:
    base: int

    assembler: Assembler = field(default_factory=lambda: Assembler(4))

    def compile_value(self, val):
        if isinstance(val, FIXEDFILEINFO):
            v = VS_FIXEDFILEINFO()
            v.dwFileVersionMS = val.FILEVERSION[1::-1]
            v.dwFileVersionLS = val.FILEVERSION[:1:-1]
            v.dwProductVersionMS = val.PRODUCTVERSION[1::-1]
            v.dwProductVersionLS = val.PRODUCTVERSION[:1:-1]
            v.dwFileFlagsMask = val.FILEFLAGSMASK
            v.dwFileFlags = val.FILEFLAGS
            v.dwFileOS = val.FILEOS
            v.dwFileType = val.FILETYPE
            v.dwFileSubtype = val.FILESUBTYPE
            typ, val, tp = 0, v, VS_FIXEDFILEINFO
        elif isinstance(val, str):
            typ, tp = 1, WSTR
        else:
            assert is_dataclass(val)
            typ, tp = 0, type(val)
        return typ, self.assembler._compile(val, tp)

    def compile_node(self, key: str, res: typing.Union[Resource, str, dict, typing.Any]):
        if not isinstance(res, Resource):
            if isinstance(res, dict):
                res = Resource(None, res)
            else:
                res = Resource(res, {})
        node = ResourceNode()
        node.szKey = key
        if res.Value is not None:
            node.wType, node.Value = self.compile_value(res.Value)
            node.Value.alignment = 4
            node.wValueLength = len(node.Value.data)
            if node.wType:
                node.wValueLength //= 2
        node.Children.alignment = 4
        for name, child in res.Children.items():
            node.Children.append(self.compile_node(name, child))
        node.wLength = _aligned_next(8 + 2*len(node.szKey), 4)
        node.wLength += _aligned_next(len(node.Value), 4)
        node.wLength += len(node.Children)
        out = self.assembler.compile(node)
        out.alignment = 4
        out.append_padding(4)
        return out

    def compile_tables(self, table: dict):
        tables = ResourceTable()

        name_entries = {key: value for key, value in table.items() if isinstance(key, str)}
        id_entries = {key: value for key, value in table.items() if isinstance(key, int)}

        assert len(name_entries) == 0, "not implemented"

        entries_data = {}
        entries_subdir = {}
        tables.NumberOfIDEntries = len(id_entries)
        for key, value in sorted(id_entries.items(), key=itemgetter(0)):
            next = len(entries_data) + len(entries_subdir) + 0xFEED1273
            if not isinstance(value, BinaryObject):
                entries_subdir[next] = self.compile_tables(value)
            else:
                entries_data[next] = ResourceEntry(value, len(value))
            tables.IDEntries.append(ResourceTableRow(key, next))

        tables = self.assembler.compile(tables)
        for key, entry in entries_data.items():
            entry = self.assembler.compile(entry)
            tables.symbols[tables.data.index(self.assembler._compile(key, DWORD).data)] = Pointer(entry, 4, -self.base)
        for key, entry in entries_subdir.items():
            entry = self.assembler.compile(entry)
            tables.symbols[tables.data.index(self.assembler._compile(key, DWORD).data)] = Pointer(entry, 4, 0x80000000-self.base)

        return tables


@dataclass()
class Directory:
    VirtualAddress: DWORD = 0
    Size: DWORD = 0


@dataclass()
class Section:
    Name: typing.Annotated[str, CHAR_E, _LengthFixed(8)] = "\0\0\0\0\0\0\0\0"
    VirtualSize: DWORD = 0
    VirtualAddress: DWORD = 0
    SizeOfRawData: DWORD = 0
    PointerToRawData: RVA[typing.Annotated[BinaryObject, _LengthReferenced("SizeOfRawData")]] = None
    PointerToRelocations: DWORD = 0
    PointerToLinenumber: DWORD = 0
    NumberOfRelocations: WORD = 0
    NumberOfLinenumbers: WORD = 0
    Characteristics: DWORD = 0


@dataclass()
class HeaderOpt:
    Magic: WORD = 0x10B
    LinkerVersion: MAKEWORD = _version_num[:2]
    SizeOfCode: DWORD = 0
    SizeOfInitializedData: DWORD = 0
    SizeOfUninitializedData: DWORD = 0
    AddressOfEntryPoint: DWORD = 0
    BaseOfCode: DWORD = 0
    BaseOfData: DWORD = 0  # Low DWORD of ImageBase on PE32+
    ImageBase: DWORD = 0
    SectionAlignment: DWORD = 0
    FileAlignment: DWORD = 0
    OperatingSystemVersion: MAKELONG = (5, 1)
    ImageVersion: MAKELONG = (0, 0)
    SubsystemVersion: MAKELONG = (5, 1)
    Win32VersionValue: DWORD = 0
    SizeOfImage: DWORD = 0
    SizeOfHeaders: DWORD = 0
    CheckSum: DWORD = 0
    Subsystem: WORD = 1
    DllCharacteristics: WORD = 0x540
    SizeOfStackReserve: DWORD_PTR = 0x40000
    SizeOfStackCommit: DWORD_PTR = 0x1000
    SizeOfHeapReserve: DWORD_PTR = 0x100000
    SizeOfHeapCommit: DWORD_PTR = 0x1000
    LoaderFlags: DWORD = 0
    NumberOfRvaAndSizes: DWORD = 0
    Directories: typing.Annotated[list[Directory], _LengthReferenced("NumberOfRvaAndSizes")] = field(default_factory=list)

    def __len__(self):
        if self.Magic == 0x10B:
            return 28 + 68 + 8 * self.NumberOfRvaAndSizes
        elif self.Magic == 0x20B:
            return 24 + 88 + 8 * self.NumberOfRvaAndSizes
        else:
            assert False, "unknown Magic constant for Optional Header"


@dataclass()
class HeaderCOFF:
    # technically not part of COFF header, but it immediately precedes it
    signature: typing.Annotated[bytes, _LengthFixed(4)] = b"PE\0\0"

    # start of COFF header
    Machine: WORD = 0
    NumberOfSections: WORD = 0
    TimeDateStamp: DWORD = 0
    PointerToSymbolTable: DWORD = 0
    NumberOfSymbols: DWORD = 0
    SizeOfOptionalHeader: WORD = 0
    Characteristics: WORD = 0

    opt: typing.Annotated[HeaderOpt, _LengthReferenced("SizeOfOptionalHeader")] = field(default_factory=HeaderOpt)

    # technically not part of the COFF header, but it immediately follows it
    sections: typing.Annotated[list[Section], _LengthReferenced("NumberOfSections")] = field(default_factory=list)


@dataclass()
class HeaderDOS:
    signature: typing.Annotated[bytes, _LengthFixed(2)] = b"MZ"
    bytes_in_last_block: WORD = 0x90
    blocks_in_file: WORD = 3
    """size of file // 512"""
    num_relocs: WORD = 0
    header_paragraphs: WORD = 4
    """size of header // 16 (start of code)"""
    min_extra_paragraphs: WORD = 0
    max_extra_paragraphs: WORD = 0xFFFF
    ss: WORD = 0
    sp: WORD = 0xB8
    checksum: WORD = 0
    ip: WORD = 0
    cs: WORD = 0
    reloc_table_offset: WORD = 0
    overlay_number: WORD = 0
    padding: typing.Annotated[bytes, _LengthFixed(32)] = b"\0" * 32
    pe: RVA[HeaderCOFF] = field(default_factory=HeaderCOFF)


dos_stub = (
    b"\x0E"             # PUSH CS
    b"\x1F"             # PUSH DS
    b"\xBA\x0E\x00"     # MOV DX, offset 0xE
    b"\xB4\x09"         # MOV AH, 0x09
    b"\xCD\x21"         # INT 0x21
    b"\xB8\x01\x4C"     # MOV AX, 0x4C01
    b"\xCD\x21"         # INT 0x21
    b"This program cannot be run in DOS mode.\n\n\r$"
    b"\0\0\0\0\0\0\0"   # align 0x16
)


@dataclass()
class DirExport:
    flags: DWORD = 0  # reserved
    timestamp: DWORD = 0
    version_major: WORD = 0  # unused
    version_minor: WORD = 0  # unused
    name: RVA[STR] = "\0"
    ordinal_base: DWORD = 1
    address_count: DWORD = 0
    name_count: DWORD = 0
    addresses: RVA[typing.Annotated[list[DWORD], _LengthReferenced("address_count")]] = None
    names: RVA[typing.Annotated[list[RVA[STR]], _LengthReferenced("name_count")]] = None
    ordinals: RVA[typing.Annotated[list[WORD], _LengthReferenced("name_count")]] = None


@dataclass()
class DirRelocBlock:
    page: DWORD = 0
    size: DWORD = 0
    entries: typing.Annotated[
        list[WORD], _LengthReferenced("size", mul=0.5, add=-4)
    ] = field(default_factory=list)


@dataclass()
class DirReloc:
    blocks: list[DirRelocBlock]


@dataclass(frozen=True)
class Architecture:
    pointer: int  # sizeof KBD_LONG_POINTER
    pointer_func: int  # sizeof pointer

    machine: int  # coff.Machine
    characteristics: int  # coff.Characteristics

    magic: int  # opt.Magic
    base: int  # opt.ImageBase

    func: bytes  # data of function KbdLayerDescriptor
    suffix: str  # filename suffix
    name: str  # str(self)

    def __str__(self):
        return self.name


X86   = Architecture(4, 4, 0x14C,  0x2102, 0x10b, 0x00005FFF0000, b"\xB8%b\xC3",     '32', 'Windows-x86')
WOW64 = Architecture(8, 4, 0x14C,  0x2102, 0x10b, 0x00005FFE0000, b"\xB8%b\x99\xC3", 'WW', 'Windows-WoW64')
AMD64 = Architecture(8, 8, 0x8664, 0x2022, 0x20b, 0x001800000000, b"\x48\xB8%b\xC3", '64', 'Windows-amd64')


@dataclass()
class Compiler:
    layout: Layout
    arch: Architecture

    timestamp: int

    align_file: int = 0x200
    align_section: int = 0x1000

    assembler: typing.Optional[Assembler] = None

    dir_export: typing.Optional[BinaryObject] = None
    dir_rsrc: typing.Optional[BinaryObject] = None
    dir_reloc: typing.Optional[BinaryObject] = None

    sec_data: typing.Optional[BinaryObject] = None
    sec_rsrc: typing.Optional[BinaryObject] = None
    sec_reloc: typing.Optional[BinaryObject] = None

    file: typing.Optional[BinaryObject] = None

    def compile(self):
        self.assembler = Assembler(self.arch.pointer_func)

        # skip header "section"
        next_section = self.align_section

        self.compile_sec_data(next_section)
        assert self.sec_data.placement == (None, next_section)
        next_section += _aligned_next(len(self.sec_data.data), self.align_section)

        self.compile_sec_rsrc(next_section)
        assert self.sec_rsrc.placement == (None, next_section)
        next_section += _aligned_next(len(self.sec_rsrc.data), self.align_section)

        self.compile_sec_reloc(next_section)
        assert self.sec_reloc.placement == (None, next_section)
        next_section += _aligned_next(len(self.sec_reloc.data), self.align_section)

        self.compile_header()
        return bytes(self.file.data)

    def compile_sec_data(self, base):
        """Keyboard data and functions"""
        func_ptr = lambda obj: Offset(obj, self.arch.pointer_func)

        kbdtables = Assembler(self.arch.pointer).compile(compiler.compile_kbd_tables(self.layout))

        KbdLayerDescriptor = BinaryObject(self.arch.func % func_ptr(None)().data)
        KbdLayerDescriptor.symbols[self.arch.func.index(b"%b")] = func_ptr(kbdtables)

        export = DirExport()
        export.timestamp = self.timestamp
        export.name = self.layout.dll_name
        export.ordinal_base = 1
        export.address_count = 1
        export.name_count = 1
        export.addresses = [0xA5A5A5A5]
        export.names = ["KbdLayerDescriptor"]
        export.ordinals = [0]

        # export directory must be self-contained
        # abuse link to make sure it is packed, will link for real later
        dir_export = link([self.assembler.compile(export)], base)
        dir_export.placement = None

        # add function pointers
        dir_export.symbols |= {
            dir_export.data.index(b"\xA5\xA5\xA5\xA5"): Offset(KbdLayerDescriptor, 4)
        }

        # abuse link to bring all symbols into one object, and convert pointers
        code = link([KbdLayerDescriptor])
        code.placement = None
        code.symbols |= {
            o: Pointer(p.target, p.sizeof, self.arch.base)
            for o, p in code.symbols.items()
            if isinstance(p, Offset)
        }

        self.dir_export = dir_export
        self.sec_data = link([dir_export, code], base=base)
        self.sec_data.alignment = self.align_file

    def compile_sec_rsrc(self, base):
        rc = ResourceCompiler(base)

        version_info = compiler.compile_resources(self.layout)
        version_info = rc.compile_node("VS_VERSION_INFO", version_info)

        rsrc = rc.compile_tables({0x10: {1: {0x409: version_info}}})
        self.sec_rsrc = self.dir_rsrc = link([rsrc], base=base)
        self.sec_rsrc.alignment = self.align_file

    def compile_sec_reloc(self, base):
        blocks = defaultdict(set)
        for offset, symbol in self.sec_data.symbols.items():
            if symbol.target is not None and isinstance(symbol, Pointer):
                offset += self.sec_data.placement[1]
                blocks[offset // 0x1000].add((offset % 0x1000, symbol))

        reloc = DirReloc([])
        for block_base, symbols in sorted(blocks.items(), key=itemgetter(0)):
            block = DirRelocBlock(block_base * 0x1000, 8 + 2 * len(symbols), [
                offset + (0x3000 if len(symbol().data) == 4 else 0xA000)
                for offset, symbol in sorted(symbols, key=itemgetter(0))
            ])
            if len(symbols) % 2 == 1:
                block.size += 2
                block.entries.append(0)
            reloc.blocks.append(block)

        self.dir_reloc = self.assembler.compile(reloc)
        self.sec_reloc = link([self.dir_reloc], base=base)
        self.sec_reloc.alignment = self.align_file

    def compile_header(self):
        headers = HeaderDOS()

        assert isinstance(headers.pe, HeaderCOFF)
        headers.pe.Machine = self.arch.machine
        headers.pe.NumberOfSections = 3
        headers.pe.TimeDateStamp = self.timestamp
        headers.pe.Characteristics = self.arch.characteristics

        assert isinstance(headers.pe.opt, HeaderOpt)
        headers.pe.opt.Magic = self.arch.magic
        headers.pe.opt.SizeOfInitializedData = sum(
            _aligned_next(len(sec.data), self.align_file)
            for sec in (self.sec_data, self.sec_reloc)
        )
        headers.pe.opt.BaseOfCode = self.sec_data.placement[1]
        if self.arch.pointer_func == 8:
            headers.pe.opt.BaseOfData = self.arch.base & 0xFFFFFFFF
            headers.pe.opt.ImageBase = self.arch.base >> 32
        else:
            headers.pe.opt.BaseOfData = headers.pe.opt.BaseOfCode
            headers.pe.opt.ImageBase = self.arch.base
        headers.pe.opt.SectionAlignment = self.align_section
        headers.pe.opt.FileAlignment = self.align_file
        headers.pe.opt.ImageVersion = self.layout.version
        headers.pe.opt.SizeOfImage = _aligned_next(
            self.sec_reloc.placement[1] + len(self.sec_reloc.data), self.align_section
        )
        headers.pe.opt.SizeOfHeaders = 3*self.align_file  # FIXME
        headers.pe.opt.CheckSum = 0x83D6DB17  # FIXME
        headers.pe.opt.NumberOfRvaAndSizes = 16
        headers.pe.opt.Directories = [Directory()] * 16
        for i, d in (
                (0, self.dir_export),
                (2, self.dir_rsrc),
                (5, self.dir_reloc)
        ):
            headers.pe.opt.Directories[i] = Directory(d.find_placement()[1], len(d.data))
        headers.pe.SizeOfOptionalHeader = len(headers.pe.opt)

        for name, section, characteristics in (
                (".data\0\0\0", self.sec_data, 0x60000040),  # char: init data, read, execute
                (".rsrc\0\0\0", self.sec_rsrc, 0x42000040),  # char: init data, read, discard
                (".reloc\0\0", self.sec_reloc, 0x42000040),  # char: init data, read, discard
        ):
            s = Section(name)
            s.VirtualSize = len(section.data)
            s.VirtualAddress = section.placement[1]
            section = BinaryObject(section.data, self.align_file)
            section.append_padding(self.align_file)
            s.SizeOfRawData = len(section.data)
            s.PointerToRawData = section
            s.Characteristics = characteristics
            headers.pe.sections.append(s)
        headers.pe.NumberOfSections = len(headers.pe.sections)

        mz = self.assembler.compile(headers)
        mz.append(dos_stub)
        mz.append(b"Generated with PyKbd %a for %a" % (__version__, self.arch.name))
        self.file = link([mz])
