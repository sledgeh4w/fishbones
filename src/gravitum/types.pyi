import sys
from ctypes import (c_int8, c_int16, c_int32, c_int64, c_uint8, c_uint16,
                    c_uint32, c_uint64)
from typing import ClassVar, Iterable, SupportsBytes, Type, TypeVar, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = [
    'ByteOrder', 'IntVar', 'IntType', 'IntMeta', 'IntBase', 'Int8', 'Int16',
    'Int32', 'Int64', 'UInt8', 'UInt16', 'UInt32', 'UInt64', 'int8', 'int16',
    'int32', 'int64', 'uint8', 'uint16', 'uint32', 'uint64'
]

_BaseInt = Union[c_int8, c_int16, c_int32, c_int64, c_uint8, c_uint16, c_uint32,
                 c_uint64]

_BaseType = Type[_BaseInt]

ByteOrder = Literal['little', 'big']

IntVar = Union['Int8', 'Int16', 'Int32', 'Int64', 'UInt8', 'UInt16', 'UInt32',
               'UInt64']

IntType = Type[Union['Int8', 'Int16', 'Int32', 'Int64', 'UInt8', 'UInt16',
                     'UInt32', 'UInt64']]

T = TypeVar('T', 'Int8', 'Int16', 'Int32', 'Int64', 'UInt8', 'UInt16', 'UInt32',
            'UInt64')


class IntMeta(type):
    ...


class IntBase:

    _base: _BaseType
    _size: ClassVar[int]
    _signed: ClassVar[bool]

    _impl: _BaseInt

    def __init__(self, val):
        ...

    def __int__(self) -> int:
        ...

    def __gt__(self, other) -> bool:
        ...

    def __ge__(self, other) -> bool:
        ...

    def __eq__(self, other) -> bool:
        ...

    def __le__(self, other) -> bool:
        ...

    def __lt__(self, other) -> bool:
        ...

    def __ne__(self, other) -> bool:
        ...

    def __neg__(self):
        ...

    def __pos__(self):
        ...

    def __abs__(self):
        ...

    def __add__(self, other):
        ...

    def __radd__(self, other):
        ...

    def __sub__(self, other):
        ...

    def __rsub__(self, other):
        ...

    def __mul__(self, other):
        ...

    def __rmul__(self, other):
        ...

    def __truediv__(self, other):
        ...

    def __rtruediv__(self, other):
        ...

    def __floordiv__(self, other):
        ...

    def __rfloordiv__(self, other):
        ...

    def __mod__(self, other):
        ...

    def __rmod__(self, other):
        ...

    def __invert__(self):
        ...

    def __and__(self, other):
        ...

    def __rand__(self, other):
        ...

    def __or__(self, other):
        ...

    def __ror__(self, other):
        ...

    def __xor__(self, other):
        ...

    def __rxor__(self, other):
        ...

    def __lshift__(self, other):
        ...

    def __rlshift__(self, other):
        ...

    def __rshift__(self, other):
        ...

    def __rrshift__(self, other):
        ...

    @classmethod
    def get_size(cls) -> int:
        ...

    @classmethod
    def get_signed(cls) -> bool:
        ...

    @classmethod
    def from_bytes(cls,
                   data: Union[Iterable[int], SupportsBytes],
                   byteorder: ByteOrder = 'little'):
        ...

    def to_bytes(self, byteorder: ByteOrder = 'little') -> bytes:
        ...


class Int8(IntBase, metaclass=IntMeta):
    ...


class Int16(IntBase, metaclass=IntMeta):
    ...


class Int32(IntBase, metaclass=IntMeta):
    ...


class Int64(IntBase, metaclass=IntMeta):
    ...


class UInt8(IntBase, metaclass=IntMeta):
    ...


class UInt16(IntBase, metaclass=IntMeta):
    ...


class UInt32(IntBase, metaclass=IntMeta):
    ...


class UInt64(IntBase, metaclass=IntMeta):
    ...


def int8(v) -> Int8:
    ...


def int16(v) -> Int16:
    ...


def int32(v) -> Int32:
    ...


def int64(v) -> Int64:
    ...


def uint8(v) -> UInt8:
    ...


def uint16(v) -> UInt16:
    ...


def uint32(v) -> UInt32:
    ...


def uint64(v) -> UInt64:
    ...
