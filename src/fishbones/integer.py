import ctypes
import re
import sys
from typing import (
    Iterable,
    Optional,
    SupportsBytes,
    SupportsInt,
    Type,
    Union,
)

from .consts import LITTLE_ENDIAN

if sys.version_info >= (3, 8):
    from typing import Literal, SupportsIndex
else:
    from typing_extensions import Literal, SupportsIndex


def _unary_op(func):
    op = getattr(int, func.__name__)

    def decorator(self):
        data_type = type(self)
        return data_type(op(self._impl.value))

    return decorator


def _binary_op(func):
    op = getattr(int, func.__name__)

    def decorator(self, *args):
        data_type = type(self)

        other = args[0]

        if isinstance(other, Integer):
            # If their sizes are equal, the type of result is unsigned.
            if self.size == other.size:
                data_type = type(other if self.signed else self)

            # If their sizes are not equal, the type of result is
            # larger size type.
            else:
                if self.size < other.size:
                    data_type = type(other)
                    self, other = other, self

                else:
                    data_type = type(self)

        elif not hasattr(other, "__int__"):
            return NotImplemented

        return data_type(op(self._impl.value, int(other)))

    return decorator


def _comparison(func):
    cmp = getattr(int, func.__name__)

    def decorator(self, other):
        if not hasattr(other, "__int__"):
            return False

        return cmp(self._impl.value, int(other))

    return decorator


class Integer:
    """Base class of integer type."""

    def __init__(self, x: SupportsInt):
        ctypes_cls = getattr(ctypes, "c_%s" % self.__class__.__name__.lower())
        self._impl = ctypes_cls(int(x))

    @_unary_op
    def __neg__(self):
        pass

    @_unary_op
    def __pos__(self):
        pass

    @_unary_op
    def __abs__(self):
        pass

    @_binary_op
    def __add__(self, other):
        pass

    @_binary_op
    def __radd__(self, other):
        pass

    @_binary_op
    def __sub__(self, other):
        pass

    @_binary_op
    def __rsub__(self, other):
        pass

    @_binary_op
    def __mul__(self, other):
        pass

    @_binary_op
    def __rmul__(self, other):
        pass

    @_binary_op
    def __truediv__(self, other):
        pass

    @_binary_op
    def __rtruediv__(self, other):
        pass

    @_binary_op
    def __floordiv__(self, other):
        pass

    @_binary_op
    def __rfloordiv__(self, other):
        pass

    @_binary_op
    def __mod__(self, other):
        pass

    @_binary_op
    def __rmod__(self, other):
        pass

    @_unary_op
    def __invert__(self):
        pass

    @_binary_op
    def __and__(self, other):
        pass

    @_binary_op
    def __rand__(self, other):
        pass

    @_binary_op
    def __or__(self, other):
        pass

    @_binary_op
    def __ror__(self, other):
        pass

    @_binary_op
    def __xor__(self, other):
        pass

    @_binary_op
    def __rxor__(self, other):
        pass

    @_binary_op
    def __lshift__(self, other):
        pass

    @_binary_op
    def __rlshift__(self, other):
        pass

    @_binary_op
    def __rshift__(self, other):
        pass

    @_binary_op
    def __rrshift__(self, other):
        pass

    @_comparison
    def __eq__(self, other):
        pass

    @_comparison
    def __ne__(self, other):
        pass

    @_comparison
    def __gt__(self, other):
        pass

    @_comparison
    def __ge__(self, other):
        pass

    @_comparison
    def __lt__(self, other):
        pass

    @_comparison
    def __le__(self, other):
        pass

    def __int__(self) -> int:
        return int(self._impl.value)

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
