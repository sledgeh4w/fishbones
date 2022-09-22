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
from typing import ClassVar, Iterable, Optional, SupportsBytes, SupportsInt, Type, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

_CtypesInt = Union[
    c_int8, c_int16, c_int32, c_int64, c_uint8, c_uint16, c_uint32, c_uint64
]

_ByteOrder = Literal["little", "big"]

class _UnaryOp:
    def __call__(self) -> IntVar: ...

class _BinaryOp:
    def __call__(self, other: SupportsInt) -> IntVar: ...

class _ComparisonOp:
    def __call__(self, other: SupportsInt) -> bool: ...

class IntBase:
    _base: Type[_CtypesInt]
    _size: ClassVar[int]
    _signed: ClassVar[bool]
    _impl: _CtypesInt

    def __init__(self, x: SupportsInt): ...
    def __int__(self) -> int: ...

    __neg__: _UnaryOp
    __pos__: _UnaryOp
    __abs__: _UnaryOp
    __add__: _BinaryOp
    __radd__: _BinaryOp
    __sub__: _BinaryOp
    __rsub__: _BinaryOp
    __mul__: _BinaryOp
    __rmul__: _BinaryOp
    __truediv__: _BinaryOp
    __rtruediv__: _BinaryOp
    __floordiv__: _BinaryOp
    __rfloordiv__: _BinaryOp
    __mod__: _BinaryOp
    __rmod__: _BinaryOp
    __invert__: _UnaryOp
    __and__: _BinaryOp
    __rand__: _BinaryOp
    __or__: _BinaryOp
    __ror__: _BinaryOp
    __xor__: _BinaryOp
    __rxor__: _BinaryOp
    __lshift__: _BinaryOp
    __rlshift__: _BinaryOp
    __rshift__: _BinaryOp
    __rrshift__: _BinaryOp
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
        byteorder: Optional[_ByteOrder] = None,
    ): ...
    def to_bytes(self, byteorder: Optional[_ByteOrder] = None) -> bytes: ...

class Int8(IntBase): ...
class Int16(IntBase): ...
class Int32(IntBase): ...
class Int64(IntBase): ...
class UInt8(IntBase): ...
class UInt16(IntBase): ...
class UInt32(IntBase): ...
class UInt64(IntBase): ...

int8 = Int8
int16 = Int16
int32 = Int32
int64 = Int64
uint8 = UInt8
uint16 = UInt16
uint32 = UInt32
uint64 = UInt64

IntVar = IntBase
IntType = Type[IntVar]
