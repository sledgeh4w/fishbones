import ctypes
import re
import sys
from typing import (
    Callable,
    Iterable,
    Optional,
    SupportsBytes,
    SupportsInt,
    Type,
    Union,
    get_type_hints,
)

from .consts import LITTLE_ENDIAN

if sys.version_info >= (3, 8):
    from typing import Literal, SupportsIndex
else:
    from typing_extensions import Literal, SupportsIndex


class _UnaryOp:
    def __call__(self) -> "Integer":
        pass


class _BinaryOp:
    def __call__(self, other: SupportsInt) -> "Integer":
        pass


_ComparisonOp = Callable[[object, object], bool]


class IntMeta(type):
    """Metaclass of integer type."""

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)

        for name, hint_type in get_type_hints(cls).items():
            if hint_type in (_BinaryOp, _UnaryOp):
                setattr(cls, name, cls.build_operator(name))

            elif hint_type == _ComparisonOp:
                setattr(cls, name, cls.build_operator(name, is_comparison=True))

    @staticmethod
    def build_operator(func_name: str, is_comparison: bool = False):
        """Build operation method to integer type."""
        int_func = getattr(int, func_name)

        def decorator(*args):
            self = args[0]
            result_type = type(self)

            # If a binary operation
            if len(args) > 1:
                other = args[1]

                if is_comparison:
                    if isinstance(other, int) or isinstance(other, Integer):
                        return int_func(int(self), int(other))

                    return int_func(int(self), other)

                if isinstance(other, Integer):
                    # If their sizes are equal, the type of result is unsigned.
                    if self.size == other.size:
                        result_type = type(other if self.signed else self)

                    # If their sizes are not equal, the type of result is
                    # larger size type.
                    else:
                        if self.size < other.size:
                            result_type = type(other)
                            self, other = other, self

                        else:
                            result_type = type(self)

                elif not hasattr(other, "__int__"):
                    return NotImplemented

                return result_type(int_func(int(self), int(other)))

            return result_type(int_func(int(self)))

        return decorator


class Integer(metaclass=IntMeta):
    """Base class of integer type."""

    def __init__(self, x: SupportsInt):
        ctypes_cls = getattr(ctypes, "c_%s" % self.__class__.__name__.lower())
        self._value = ctypes_cls(int(x))

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
    __eq__: _ComparisonOp
    __ne__: _ComparisonOp
    __gt__: _ComparisonOp
    __ge__: _ComparisonOp
    __le__: _ComparisonOp
    __lt__: _ComparisonOp

    def __int__(self) -> int:
        return int(self._value.value)

    def __str__(self) -> str:
        return str(self.__int__())

    @property
    def size(self) -> int:
        return get_type_size(self.__class__)

    @property
    def signed(self) -> bool:
        return get_type_signed(self.__class__)

    @classmethod
    def from_bytes(
        cls,
        data: Union[Iterable[SupportsIndex], SupportsBytes],
        byteorder: Literal["big", "little"] = LITTLE_ENDIAN,
    ):
        """Return a value of this type from given bytes"""
        return cls(
            int.from_bytes(data, byteorder=byteorder, signed=get_type_signed(cls))
        )

    def to_bytes(self, byteorder: Literal["big", "little"] = LITTLE_ENDIAN) -> bytes:
        """Covert this value to bytes."""
        return int(self).to_bytes(
            length=self.size,
            byteorder=byteorder,
            signed=self.signed,
        )

    @staticmethod
    def get_type(
        size: Optional[int] = None,
        signed: Optional[bool] = None,
        type_name: Optional[str] = None,
    ) -> Type["Integer"]:
        """Get type integer with specified size and signed.

        Args:
            size: The size of the type.
            signed: Is the type signed.
            type_name: The lowercase name of type to find. If it is None,
                ``size`` and ``signed`` must be given.

        Raises:
            ValueError: If no matched type.
        """
        int_types = [Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32, UInt64]

        if type_name is not None:
            match = re.match(r"(u*)int(\d+)", type_name)

            if match:
                nbits = int(match.group(2))
                if nbits % 8 == 0:
                    signed = not bool(match.group(1))
                    size = nbits // 8

        if size is not None and signed is not None:
            for int_type in int_types:
                if (
                    get_type_size(int_type) == size
                    and get_type_signed(int_type) == signed
                ):
                    return int_type

        raise ValueError("No matched type")


class Int8(Integer):
    """Int8"""


class Int16(Integer):
    """Int16"""


class Int32(Integer):
    """Int32"""


class Int64(Integer):
    """Int64"""


class UInt8(Integer):
    """UInt8"""


class UInt16(Integer):
    """UInt16"""


class UInt32(Integer):
    """UInt32"""


class UInt64(Integer):
    """UInt64"""


def int8(x: SupportsInt) -> Int8:
    """Shorthand for `Int8(x)`."""
    return Int8(x)


def int16(x: SupportsInt) -> Int16:
    """Shorthand for `Int16(x)`."""
    return Int16(x)


def int32(x: SupportsInt) -> Int32:
    """Shorthand for `Int32(x)`."""
    return Int32(x)


def int64(x: SupportsInt) -> Int64:
    """Shorthand for `Int64(x)`."""
    return Int64(x)


def uint8(x: SupportsInt) -> UInt8:
    """Shorthand for `UInt8(x)`."""
    return UInt8(x)


def uint16(x: SupportsInt) -> UInt16:
    """Shorthand for `UInt16(x)`."""
    return UInt16(x)


def uint32(x: SupportsInt) -> UInt32:
    """Shorthand for `UInt32(x)`."""
    return UInt32(x)


def uint64(x: SupportsInt) -> UInt64:
    """Shorthand for `UInt64(x)`."""
    return UInt64(x)


def get_type_size(t: Type[Integer]) -> int:
    """Get size (bytes) of the type."""
    match_obj = re.match(r"(U*)Int(\d+)", t.__name__)
    if not match_obj:
        raise ValueError("Invalid type")

    return int(match_obj.group(2)) // 8


def get_type_signed(t: Type[Integer]) -> bool:
    """Get signed of the type."""
    return bool(re.match(r"Int\d+", t.__name__))
