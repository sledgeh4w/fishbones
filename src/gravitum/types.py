import ctypes
import re
import sys
from typing import Iterable, SupportsBytes, Type, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

ByteOrder = Literal["little", "big"]

IntVar = Union["Int8", "Int16", "Int32", "Int64", "UInt8", "UInt16", "UInt32", "UInt64"]

IntType = Type[
    Union[
        "Int8",
        "Int16",
        "Int32",
        "Int64",
        "UInt8",
        "UInt16",
        "UInt32",
        "UInt64",
    ]
]


class IntMeta(type):
    """Meta class of integer type."""

    _SUPPORT_OPERATIONS = [
        "__neg__",
        "__pos__",
        "__abs__",
        "__add__",
        "__radd__",
        "__iadd__",
        "__sub__",
        "__rsub__",
        "__isub__",
        "__mul__",
        "__rmul__",
        "__imul__",
        "__truediv__",
        "__rtruediv__",
        "__itruediv__",
        "__floordiv__",
        "__rfloordiv__",
        "__ifloordiv__",
        "__mod__",
        "__rmod__",
        "__imod__",
        "__invert__",
        "__and__",
        "__rand__",
        "__iand__",
        "__or__",
        "__ror__",
        "__ior__",
        "__xor__",
        "__rxor__",
        "__ixor__",
        "__lshift__",
        "__rlshift__",
        "__ilshift__",
        "__rshift__",
        "__rrshift__",
        "__irshift__",
    ]

    _SUPPORT_COMPARISONS = [
        "__gt__",
        "__ge__",
        "__eq__",
        "__le__",
        "__lt__",
        "__ne__",
    ]

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)

        base = getattr(ctypes, "c_%s" % cls.__name__.lower())
        setattr(cls, "_base", base)

        size = int(re.match(r"(U*)Int(\d+)", cls.__name__).group(2)) // 8
        setattr(cls, "_size", size)

        signed = bool(re.match(r"Int\d+", cls.__name__))
        setattr(cls, "_signed", signed)

        for func in cls._SUPPORT_OPERATIONS:
            setattr(cls, func, cls.build_operation(func))

        for func in cls._SUPPORT_COMPARISONS:
            setattr(cls, func, cls.build_comparison(func))

    @staticmethod
    def build_operation(func):
        """Build operation method.

        If it is a unary operation, the result is still its own type.
        If the other operand is int, it will be converted to its own type.
        If the type of another operand is inconsistent with its own type,
        they are converted to larger size or unsigned type.
        """

        def decorator(self, *args):
            data_type = type(self)

            try:
                operator = getattr(int, func)
            except AttributeError:
                return NotImplemented

            if args:
                other = args[0]

                if not isinstance(other, int):
                    if self.get_size() == other.get_size():
                        data_type = type(other if self.get_signed() else self)

                    else:
                        if self.get_size() < other.get_size():
                            data_type = type(other)
                            self, other = other, self

                        else:
                            data_type = type(self)

                return data_type(operator(self._impl.value, int(other)))

            return data_type(operator(self._impl.value))

        return decorator

    @staticmethod
    def build_comparison(func):
        """Build comparison method."""

        def decorator(self, other):
            cmp = getattr(int, func)
            return cmp(int(self), int(other))

        return decorator


class IntBase:
    """Base class of integer type."""

    def __init__(self, val):
        if isinstance(val, IntBase):
            val = val.__int__()

        self._impl = self._base(val)

    def __int__(self) -> int:
        return int(self._impl.value)

    @classmethod
    def get_size(cls) -> int:
        """Get size (bytes) of this type."""
        return cls._size

    @classmethod
    def get_signed(cls) -> bool:
        """Get signed of this type."""
        return cls._signed

    @classmethod
    def from_bytes(
        cls,
        data: Union[Iterable[int], SupportsBytes],
        byteorder: ByteOrder = "little",
    ):
        """Return a value of this type from given bytes"""
        return cls(int.from_bytes(data, byteorder=byteorder, signed=cls.get_signed()))

    def to_bytes(self, byteorder: ByteOrder = "little") -> bytes:
        """Covert this value to bytes."""
        return int(self).to_bytes(
            length=self.get_size(),
            byteorder=byteorder,
            signed=self.get_signed(),
        )


class Int8(IntBase, metaclass=IntMeta):
    """Int8"""


class Int16(IntBase, metaclass=IntMeta):
    """Int16"""


class Int32(IntBase, metaclass=IntMeta):
    """Int32"""


class Int64(IntBase, metaclass=IntMeta):
    """Int64"""


class UInt8(IntBase, metaclass=IntMeta):
    """UInt8"""


class UInt16(IntBase, metaclass=IntMeta):
    """UInt16"""


class UInt32(IntBase, metaclass=IntMeta):
    """UInt32"""


class UInt64(IntBase, metaclass=IntMeta):
    """UInt64"""


def int8(v) -> Int8:
    """Shorthand of `Int8(v)`."""
    return Int8(v)


def int16(v) -> Int16:
    """Shorthand of `Int16(v)`."""
    return Int16(v)


def int32(v) -> Int32:
    """Shorthand of `Int32(v)`."""
    return Int32(v)


def int64(v) -> Int64:
    """Shorthand of `Int64(v)`."""
    return Int64(v)


def uint8(v) -> UInt8:
    """Shorthand of `UInt8(v)`."""
    return UInt8(v)


def uint16(v) -> UInt16:
    """Shorthand of `UInt16(v)`."""
    return UInt16(v)


def uint32(v) -> UInt32:
    """Shorthand of `UInt32(v)`."""
    return UInt32(v)


def uint64(v) -> UInt64:
    """Shorthand of `UInt64(v)`."""
    return UInt64(v)
