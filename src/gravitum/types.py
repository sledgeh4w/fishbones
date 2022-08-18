import ctypes
import re

__all__ = [
    "Integer",
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

_INT_OPERATIONS = [
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

_INT_COMPARISONS = [
    "__gt__",
    "__ge__",
    "__eq__",
    "__le__",
    "__lt__",
    "__ne__",
]


class IntMeta(type):
    """Meta class of integer type."""

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)

        base = getattr(ctypes, "c_%s" % cls.__name__.lower())
        setattr(cls, "_base", base)

        size = int(re.match(r"(U*)Int(\d+)", cls.__name__).group(2)) // 8
        setattr(cls, "_size", size)

        signed = bool(re.match(r"Int\d+", cls.__name__))
        setattr(cls, "_signed", signed)

        for f in _INT_OPERATIONS:
            setattr(cls, f, cls.build_operation(f))

        for f in _INT_COMPARISONS:
            setattr(cls, f, cls.build_comparison(f))

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

                if isinstance(other, Integer):
                    if self.get_size() == other.get_size():
                        data_type = type(other if self.get_signed() else self)

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
    def build_comparison(func):
        """Build comparison method."""

        def decorator(self, other):
            cmp = getattr(int, func)
            return cmp(self._impl.value, int(other))

        return decorator


class Integer:
    """Base class of integer type."""

    def __init__(self, val):
        self._impl = self._base(int(val))

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


def int8(v):
    """Shorthand of `Int8(v)`."""
    return Int8(v)


def int16(v):
    """Shorthand of `Int16(v)`."""
    return Int16(v)


def int32(v):
    """Shorthand of `Int32(v)`."""
    return Int32(v)


def int64(v):
    """Shorthand of `Int64(v)`."""
    return Int64(v)


def uint8(v):
    """Shorthand of `UInt8(v)`."""
    return UInt8(v)


def uint16(v):
    """Shorthand of `UInt16(v)`."""
    return UInt16(v)


def uint32(v):
    """Shorthand of `UInt32(v)`."""
    return UInt32(v)


def uint64(v):
    """Shorthand of `UInt64(v)`."""
    return UInt64(v)
