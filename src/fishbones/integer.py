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
from typing import (
    ClassVar,
    Iterable,
    Optional,
    SupportsBytes,
    SupportsInt,
    Type,
    Union,
    get_type_hints,
)

from . import endian

if sys.version_info >= (3, 8):
    from typing import SupportsIndex
else:
    from typing_extensions import SupportsIndex

_CtypesInt = Union[
    c_int8, c_int16, c_int32, c_int64, c_uint8, c_uint16, c_uint32, c_uint64
]


class _UnaryOp:
    def __call__(self) -> "Int":
        pass


class _BinaryOp:
    def __call__(self, other: SupportsInt) -> "Int":
        pass


class _ComparisonOp:
    def __call__(self, other: SupportsInt) -> bool:
        pass


class IntMeta(type):
    """Metaclass of integer type."""

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)

        cls_name = cls.__name__

        setattr(cls, "_cls", getattr(ctypes, "c_%s" % cls_name.lower()))
        setattr(cls, "_size", int(re.match(r"(U*)Int(\d+)", cls_name).group(2)) // 8)
        setattr(cls, "_signed", bool(re.match(r"Int\d+", cls_name)))

        for name, t_hint in get_type_hints(_Int).items():
            if t_hint in (_BinaryOp, _UnaryOp):
                setattr(cls, name, cls._build_operation(name))

            elif t_hint == _ComparisonOp:
                setattr(cls, name, cls._build_comparison(name))

        for name in ("__eq__", "__ne__"):
            setattr(cls, name, cls._build_comparison(name))

    @staticmethod
    def _build_operation(func_name):
        """Build operation method.

        If it is a unary operation, the result is still the own type.
        If the type of another operand is ``Int`` and is inconsistent with the
        own type, they result will be converted to larger size or unsigned type.
        If another operand is ``int`` or can be converted to ``int``, the result
        will be converted to the own type.
        """

        try:
            operator = getattr(int, func_name)
        except AttributeError:
            return None

        def decorator(self, *args):
            data_type = type(self)

            # If a binary operation
            if args:
                other = args[0]

                if isinstance(other, Int):
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


class _Int:
    """Type hint for integer type."""

    _size: ClassVar[int]
    _signed: ClassVar[bool]

    _cls: Type[_CtypesInt]
    _impl: _CtypesInt

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


class Int(_Int):
    """Base class of integer type."""

    def __init__(self, x: SupportsInt):
        if not getattr(self, "_cls"):
            raise TypeError(
                "This class is only used for inheritance, don't instantiate it"
            )

        self._impl = self._cls(int(x))

    def __int__(self) -> int:
        return int(self._impl.value)

    def __str__(self) -> str:
        return str(self.__int__())

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

    @staticmethod
    def get_type(
        size: Optional[int] = None,
        signed: Optional[bool] = None,
        type_name: Optional[str] = None,
    ) -> Type["Int"]:
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
                if int_type.get_size() == size and int_type.get_signed() == signed:
                    return int_type

        raise ValueError("No matched type")


class Int8(Int, metaclass=IntMeta):
    """Int8"""


class Int16(Int, metaclass=IntMeta):
    """Int16"""


class Int32(Int, metaclass=IntMeta):
    """Int32"""


class Int64(Int, metaclass=IntMeta):
    """Int64"""


class UInt8(Int, metaclass=IntMeta):
    """UInt8"""


class UInt16(Int, metaclass=IntMeta):
    """UInt16"""


class UInt32(Int, metaclass=IntMeta):
    """UInt32"""


class UInt64(Int, metaclass=IntMeta):
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
