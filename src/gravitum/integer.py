import ctypes
import re
from typing import Type

# Operation and comparison methods of integer types to be defined.

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

                if isinstance(other, IntBase):
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
            func = getattr(int, func_name)
            return func(self._impl.value, int(other))

        return decorator


class IntBase:
    """Base class of integer type."""

    def __init__(self, v):
        self._impl = self._base(int(v))

    def __int__(self):
        return int(self._impl.value)

    @classmethod
    def get_size(cls):
        """Get size (bytes) of this type."""
        return cls._size

    @classmethod
    def get_signed(cls):
        """Get signed of this type."""
        return cls._signed

    @classmethod
    def from_bytes(cls, data, byteorder="little"):
        """Return a value of this type from given bytes"""
        return cls(int.from_bytes(data, byteorder=byteorder, signed=cls.get_signed()))

    def to_bytes(self, byteorder="little"):
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


int8 = Int8
int16 = Int16
int32 = Int32
int64 = Int64
uint8 = UInt8
uint16 = UInt16
uint32 = UInt32
uint64 = UInt64

# Used as typing
IntVar = IntBase
IntType = Type[IntVar]
