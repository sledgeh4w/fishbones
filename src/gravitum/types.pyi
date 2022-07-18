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
from typing import (
    ClassVar,
    Iterable,
    SupportsBytes,
    SupportsInt,
    Type,
    TypeVar,
    Union,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = [
    "ByteOrder",
    "IntVar",
    "IntType",
    "IntBase",
    "Int8",
    "Int16",
    "Int32",
    "Int64",
    "UInt8",
    "UInt16",
    "UInt32",
    "UInt64",
    "int8",
    "int16",
    "int32",
    "int64",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
]

_CtypesIntVar = Union[
    c_int8, c_int16, c_int32, c_int64, c_uint8, c_uint16, c_uint32, c_uint64
]
_CtypesIntType = Type[_CtypesIntVar]

ByteOrder = Literal["little", "big"]

IntVar = Union["Int8", "Int16", "Int32", "Int64", "UInt8", "UInt16", "UInt32", "UInt64"]
IntType = Type[IntVar]

_T = TypeVar(
    "_T",
    "Int8",
    "Int16",
    "Int32",
    "Int64",
    "UInt8",
    "UInt16",
    "UInt32",
    "UInt64",
)

class _IntOp:
    def __call__(self, other: SupportsInt) -> IntVar: ...

class _ComparisonOp:
    def __call__(self, other: SupportsInt) -> bool: ...

class IntMeta(type): ...

class IntBase:
    _base: _CtypesIntType
    _size: ClassVar[int]
    _signed: ClassVar[bool]
    _impl: _CtypesIntVar
    def __init__(self, val: SupportsInt): ...
    def __int__(self) -> int: ...
    def __neg__(self) -> IntVar: ...
    def __pos__(self) -> IntVar: ...
    def __abs__(self) -> IntVar: ...
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
    def __invert__(self) -> IntVar: ...
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
        data: Union[Iterable[int], SupportsBytes],
        byteorder: ByteOrder = "little",
    ): ...
    def to_bytes(self, byteorder: ByteOrder = "little") -> bytes: ...

class Int8(IntBase, metaclass=IntMeta): ...
class Int16(IntBase, metaclass=IntMeta): ...
class Int32(IntBase, metaclass=IntMeta): ...
class Int64(IntBase, metaclass=IntMeta): ...
class UInt8(IntBase, metaclass=IntMeta): ...
class UInt16(IntBase, metaclass=IntMeta): ...
class UInt32(IntBase, metaclass=IntMeta): ...
class UInt64(IntBase, metaclass=IntMeta): ...

def int8(v: SupportsInt) -> Int8: ...
def int16(v: SupportsInt) -> Int16: ...
def int32(v: SupportsInt) -> Int32: ...
def int64(v: SupportsInt) -> Int64: ...
def uint8(v: SupportsInt) -> UInt8: ...
def uint16(v: SupportsInt) -> UInt16: ...
def uint32(v: SupportsInt) -> UInt32: ...
def uint64(v: SupportsInt) -> UInt64: ...
