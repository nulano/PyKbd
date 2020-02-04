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

from dataclasses import dataclass
from io import BytesIO

_FIELDS = '__struct_fields__'


class _USE_DEFAULT_CLASS:
    def __repr__(self):
        return '<factory>'


_USE_DEFAULT = _USE_DEFAULT_CLASS()


class _MISSING_CLASS:
    def __repr__(self):
        return '<missing>'


_MISSING = _MISSING_CLASS()


def is_struct(obj):
    return obj is not None and hasattr(obj, _FIELDS)


def _create_fn(name, params, return_type, lines, globals=None):
    lines = [f'def {name}({",".join(params)}) -> {return_type!r}:', *[f' {line}' for line in lines]]

    locals = {}
    globals = globals or {}
    exec('\n'.join(lines), globals, locals)
    return locals[name]


def _init_fn(cls):
    self_name = 'self'
    init_params = [self_name]
    init_lines = []
    globals = {'_USE_DEFAULT': _USE_DEFAULT}

    seen_default = False
    for field in getattr(cls, _FIELDS):
        globals[f'_type_{field.name}'] = field.type
        if field.default is not _MISSING:
            seen_default = True
            init_params.append(f'{field.name}:_type_{field.name}=_USE_DEFAULT')
            init_lines.append(f'{self_name}.{field.name}=({field.name} if {field.name} is not _USE_DEFAULT else _factory_{field.name}())')
            globals[f'_factory_{field.name}'] = field.default.copy if is_struct(field.default) else lambda: field.default
        else:
            if seen_default:
                raise TypeError(f'non-default argument {field.name!r} follows default argument')
            init_params.append(f'{field.name}:_type_{field.name}')
            init_lines.append(f'{self_name}.{field.name}={field.name}')
    init_lines = init_lines or ['pass']

    return _create_fn('__init__', init_params, 'None', init_lines, globals)


def _repr_fn(cls):
    def repr_impl(obj) -> str:
        return f'{cls.__name__}({", ".join([f"{field.name}={getattr(obj, field.name)!r}" for field in getattr(cls, _FIELDS)])})'
    return repr_impl


def _write_fn(cls):
    def write_impl(obj, stream: BytesIO, **kwargs) -> None:
        for field in getattr(cls, _FIELDS):
            getattr(obj, field.name).write(stream, **kwargs)
    return write_impl


def _read_fn(cls):
    def read_impl(stream: BytesIO, **kwargs) -> cls:
        return cls(*[fld.type.read(stream, **kwargs) for fld in getattr(cls, _FIELDS)])
    return staticmethod(read_impl)


def _copy_fn(cls):
    def copy_impl(obj) -> cls:
        values = []
        for field in getattr(cls, _FIELDS):
            value = getattr(obj, field.name)
            if value is not None and is_struct(value):
                value = value.copy()
            values.append(value)
        return cls(*values)
    return copy_impl


@dataclass
class _Field:
    name: str
    type: type
    default: object


@dataclass
class _AutoField:
    type: type
    name: str = '<error>'

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value if isinstance(value, self.type) \
            else self.type(*value) if isinstance(value, tuple) \
            else self.type(value)


def struct(cls): 
    fields = []

    for name, field_type in cls.__dict__.get('__annotations__', {}).items():
        field = _Field(name, field_type, cls.__dict__.get(name))
        fields.append(field)
        if is_struct(field.type):
            setattr(cls, field.name, _AutoField(field.type, field.name))

    setattr(cls, _FIELDS, fields)

    if '__init__' not in cls.__dict__:
        setattr(cls, '__init__', _init_fn(cls))

    if '__repr__' not in cls.__dict__:
        setattr(cls, '__repr__', _repr_fn(cls))

    if 'write' not in cls.__dict__:
        setattr(cls, 'write', _write_fn(cls))

    if 'read' not in cls.__dict__:
        setattr(cls, 'read', _read_fn(cls))

    if 'copy' not in cls.__dict__:
        setattr(cls, 'copy', _copy_fn(cls))

    return cls
