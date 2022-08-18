import sys
from ctypes import (
    c_int8,
    c_int16,
    c_int32,
    c_int64,
    c_uint8,
    c_uint16,
    c_uint32,
    c_uint64,
)
from typing import ClassVar, Iterable, SupportsBytes, SupportsInt, Type, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

_CtypesInt = Union[
    c_int8, c_int16, c_int32, c_int64, c_uint8, c_uint16, c_uint32, c_uint64
]

ByteOrder = Literal["little", "big"]

class _IntOp:
    def __call__(self, other: SupportsInt) -> Integer: ...

class _ComparisonOp:
    def __call__(self, other: SupportsInt) -> bool: ...

class _UnaryOp:
    def __call__(self) -> Integer: ...

class Integer:

    _base: Type[_CtypesInt]
    _size: ClassVar[int]
    _signed: ClassVar[bool]

    _impl: _CtypesInt

    def __init__(self, val: SupportsInt): ...
    def __int__(self) -> int: ...

    __neg__: _UnaryOp
    __pos__: _UnaryOp
    __abs__: _UnaryOp
    __add__: _IntOp
    __radd__: _IntOp
    __sub__: _IntOp
    __rsub__: _IntOp
    __mul__: _IntOp
    __rmul__: _IntOp
    __truediv__: _IntOp
    __rtruediv__: _IntOp
    __floordiv__: _IntOp
    __rfloordiv__: _IntOp
    __mod__: _IntOp
    __rmod__: _IntOp
    __invert__: _UnaryOp
    __and__: _IntOp
    __rand__: _IntOp
    __or__: _IntOp
    __ror__: _IntOp
    __xor__: _IntOp
    __rxor__: _IntOp
    __lshift__: _IntOp
    __rlshift__: _IntOp
    __rshift__: _IntOp
    __rrshift__: _IntOp
    __gt__: _ComparisonOp
    __ge__: _ComparisonOp
    __le__: _ComparisonOp
    __lt__: _ComparisonOp

    @classmethod
    def get_size(cls) -> int: ...
    @classmethod
    def get_signed(cls) -> bool: ...
    @classmethod
    def from_bytes(
        cls,
        data: Union[Iterable[SupportsInt], SupportsBytes],
        byteorder: ByteOrder = "little",
    ): ...
    def to_bytes(self, byteorder: ByteOrder = "little") -> bytes: ...

class Int8(Integer): ...
class Int16(Integer): ...
class Int32(Integer): ...
class Int64(Integer): ...
class UInt8(Integer): ...
class UInt16(Integer): ...
class UInt32(Integer): ...
class UInt64(Integer): ...

def int8(v: SupportsInt) -> Int8: ...
def int16(v: SupportsInt) -> Int16: ...
def int32(v: SupportsInt) -> Int32: ...
def int64(v: SupportsInt) -> Int64: ...
def uint8(v: SupportsInt) -> UInt8: ...
def uint16(v: SupportsInt) -> UInt16: ...
def uint32(v: SupportsInt) -> UInt32: ...
def uint64(v: SupportsInt) -> UInt64: ...
