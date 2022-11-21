import ctypes
import re
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

from . import endian

if sys.version_info >= (3, 8):
    from typing import SupportsIndex
else:
    from typing_extensions import SupportsIndex

_CtypesInt = Union[
    c_int8, c_int16, c_int32, c_int64, c_uint8, c_uint16, c_uint32, c_uint64
]


class _UnaryOp:
    def __call__(self) -> "IntVar":
        ...


class _BinaryOp:
    def __call__(self, other: SupportsInt) -> "IntVar":
        ...


class _ComparisonOp:
    def __call__(self, other: SupportsInt) -> bool:
        ...


# Operation and comparison methods of integer types.

_INT_OP = [
    "__neg__",
    "__pos__",
    "__abs__",
    "__add__",
    "__sub__",
    "__mul__",
    "__truediv__",
    "__floordiv__",
    "__mod__",
    "__invert__",
    "__and__",
    "__or__",
    "__xor__",
    "__lshift__",
    "__rshift__",
]

_INT_CMP = ["__gt__", "__ge__", "__eq__", "__le__", "__lt__", "__ne__"]


class IntMeta(type):
    """Metaclass of integer type."""

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)

        base = getattr(ctypes, "c_%s" % cls.__name__.lower())
        setattr(cls, "_base", base)

        size = int(re.match(r"(U*)Int(\d+)", cls.__name__).group(2)) // 8
        setattr(cls, "_size", size)

        signed = bool(re.match(r"Int\d+", cls.__name__))
        setattr(cls, "_signed", signed)

        for op in _INT_OP:
            setattr(cls, op, cls._build_operation(op))

        for cmp in _INT_CMP:
            setattr(cls, cmp, cls._build_comparison(cmp))

    @staticmethod
    def _build_operation(func_name):
        """Build operation method.

        If it is a unary operation, the result is still the own type.
        If the type of another operand is ``Integer`` and is inconsistent with
        the own type, they result will be converted to larger size or unsigned type.
        If another operand is ``int`` or can be converted to ``int``, the result
        will be converted to the own type.
        """

        def decorator(self, *args):
            data_type = type(self)

            try:
                operator = getattr(int, func_name)
            except AttributeError:
                return NotImplemented

            # If a binary operation
            if args:
                other = args[0]

                if isinstance(other, Integer):
                    # If their sizes are equal, the type of result is unsigned.
                    if self.get_size() == other.get_size():
                        data_type = type(other if self.get_signed() else self)

                    # If their sizes are not equal, the type of result is
                    # larger size type.
                    else:
                        if self.get_size() < other.get_size():
                            data_type = type(other)
                            self, other = other, self

                        else:
                            data_type = type(self)

                elif not hasattr(other, "__int__"):
                    return NotImplemented

                return data_type(operator(self._impl.value, int(other)))

            return data_type(operator(self._impl.value))

        return decorator

    @staticmethod
    def _build_comparison(func_name):
        """Build comparison method."""

        def decorator(self, other):
            if not hasattr(other, "__int__"):
                return False

            func = getattr(int, func_name)
            return func(self._impl.value, int(other))

        return decorator


class Integer:
    """Base class of integer type."""

    _base: Type[_CtypesInt]
    _size: ClassVar[int]
    _signed: ClassVar[bool]
    _impl: _CtypesInt

    def __init__(self, x: SupportsInt):
        self._impl = self._base(int(x))

    def __int__(self) -> int:
        return int(self._impl.value)

    def __str__(self) -> str:
        return str(self.__int__())

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
    def get_size(cls) -> int:
        """Get size (bytes) of this type."""
        return cls._size

    @classmethod
    def get_signed(cls) -> bool:
        """Get signed of this type."""
        return cls._signed

    @classmethod
    def from_bytes(cls, data: Union[Iterable[SupportsIndex], SupportsBytes]):
        """Return a value of this type from given bytes"""
        return cls(
            int.from_bytes(data, byteorder=endian.BYTE_ORDER, signed=cls.get_signed())
        )

    def to_bytes(self) -> bytes:
        """Covert this value to bytes."""
        return int(self).to_bytes(
            length=self.get_size(),
            byteorder=endian.BYTE_ORDER,
            signed=self.get_signed(),
        )


class Int8(Integer, metaclass=IntMeta):
    """Int8"""


class Int16(Integer, metaclass=IntMeta):
    """Int16"""


class Int32(Integer, metaclass=IntMeta):
    """Int32"""


class Int64(Integer, metaclass=IntMeta):
    """Int64"""


class UInt8(Integer, metaclass=IntMeta):
    """UInt8"""


class UInt16(Integer, metaclass=IntMeta):
    """UInt16"""


class UInt32(Integer, metaclass=IntMeta):
    """UInt32"""


class UInt64(Integer, metaclass=IntMeta):
    """UInt64"""


int8 = Int8
int16 = Int16
int32 = Int32
int64 = Int64
uint8 = UInt8
uint16 = UInt16
uint32 = UInt32
uint64 = UInt64

# Used as typing
IntVar = Integer
IntType = Type[IntVar]
