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
from dataclasses import dataclass, is_dataclass

from ..linker_binary import BinaryObject, Symbol, BinaryObjectReader
from .types import _WinInt, _WinIntPtr, _StrEncoding, _WinPtr, _Length, _LengthFixed, _LengthReferenced, \
    _NullTerminated, \
    DWORD_PTR, MAKELONG, LONG, MAKELONG_WCHAR

from . import _version


__version__ = _version



@dataclass(frozen=True)
class Pointer(Symbol):
    target: typing.Optional[BinaryObject]
    conf: "Configuration"

    def __call__(self) -> BinaryObject:
        offset = 0
        if self.target is not None:
            offset = self.conf.base + (self.target.find_placement() or (None, 0))[1]
        return BinaryObject(
            offset.to_bytes(self.conf.ptr_size, byteorder="little", signed=False),
            alignment=self.conf.ptr_size,
        )



@dataclass()
class Configuration:
    base: int
    ptr_size: int

    def _alignment(self, tp, *annotations):
        annotations = list(annotations)
        if annotations:
            annotation = annotations.pop()
            if isinstance(annotation, (_WinInt, _StrEncoding)):
                return annotation.sizeof
            elif isinstance(annotation, (_WinIntPtr, _WinPtr)):
                return self.ptr_size
            elif isinstance(annotation, _Length):
                return self._alignment(tp, *annotations)
            else:
                raise NotImplementedError(annotation)
        elif tp in (MAKELONG, MAKELONG_WCHAR):
            return self._alignment(LONG)
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
                print(obj, tp, annotations, ctx)
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
                return Pointer(tgt, self)
            elif isinstance(annotation, _Length):
                if type(annotation) is _Length:
                    assert len(obj) == ctx["__length"]
                elif isinstance(annotation, _LengthReferenced):
                    ctx["__length"] = ctx[annotation.reference] * annotation.mul + annotation.add
                    print(obj, ctx)
                    assert len(obj) == ctx["__length"]
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
        elif tp in (MAKELONG, MAKELONG_WCHAR):
            tps = typing.get_args(tp)
            assert isinstance(obj, tuple)
            assert len(obj) == 2
            out = BinaryObject(alignment=self._alignment(tp))
            for tp, v in zip(tps, obj):
                out.append(self._compile(v, tp))
            return out
        elif typing.get_origin(tp) is typing.Annotated:
            print(obj, tp)
            return self._compile(obj, *typing.get_args(tp), **ctx)
        elif typing.get_origin(tp) is list:
            assert isinstance(obj, list)
            tp, = typing.get_args(tp)
            alignment = None
            out = BinaryObject()
            for e in obj:
                v = self._compile(e, tp, **ctx)
                if alignment is None:
                    if isinstance(v, Pointer):
                        assert v.conf is self
                        alignment = self.ptr_size
                    else:
                        alignment = v.alignment
                    out.alignment = alignment
                assert isinstance(v, Pointer) or v.alignment == alignment
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
                if isinstance(val, Pointer):
                    assert val.conf is self
                    alignment = max(alignment, self.ptr_size)
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
                addr = self._decompile(data, DWORD_PTR)
                if addr != 0:
                    return self._decompile(BinaryObjectReader(data.target, addr - self.base), tp, *annotations, **ctx)
                else:
                    return None
            elif isinstance(annotation, _Length):
                if type(annotation) is _Length:
                    pass
                elif isinstance(annotation, _LengthReferenced):
                    ctx["__length"] = ctx[annotation.reference] * annotation.mul + annotation.add
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
        elif tp in (MAKELONG, MAKELONG_WCHAR):
            data.read_padding(self._alignment(tp))
            return tuple(self._decompile(data, tp) for tp in typing.get_args(tp))
        elif typing.get_origin(tp) is typing.Annotated:
            return self._decompile(data, *typing.get_args(tp), **ctx)
        elif typing.get_origin(tp) is list:
            tp, = typing.get_args(tp)
            print(tp)
            print(ctx)
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
            for name, type_hint in fields.items():
                if typing.get_origin(type_hint) is typing.Annotated and \
                        isinstance(typing.get_args(type_hint)[-1], _WinPtr):
                    delayed[name] = (BinaryObjectReader(data.target, data.offset), type_hint)
                    self._decompile(data, DWORD_PTR)
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

    def decompile(self, data, tp, off=0):
        """Compile struct"""
        if not isinstance(data, BinaryObject):
            data = BinaryObject(data)
        return self._decompile(BinaryObjectReader(data, off), tp)
