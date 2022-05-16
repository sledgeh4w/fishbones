from functools import wraps
from typing import Union, Type, SupportsBytes, Iterable

import numpy as np

# Operation methods to be overrode.
_OVERRIDE_OPERATIONS = [
    '__neg__', '__pos__', '__invert__',
    '__add__', '__radd__', '__iadd__',
    '__sub__', '__rsub__', '__isub__',
    '__mul__', '__rmul__', '__imul__',
    '__truediv__', '__rtruediv__', '__itruediv__',
    '__floordiv__', '__rfloordiv__', '__ifloordiv__',
    '__mod__', '__rmod__', '__imod__',
    '__and__', '__rand__', '__iand__',
    '__or__', '__ror__', '__ior__',
    '__xor__', '__rxor__', '__ixor__',
    '__lshift__', '__rlshift__', '__ilshift__',
    '__rshift__', '__rrshift__', '__irshift__'
]


class IntMeta(type):
    """Meta class of type int."""

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)

        for op in _OVERRIDE_OPERATIONS:
            if not hasattr(cls, op):
                continue
            setattr(cls, op, cls.operation_wrapper(getattr(cls, op)))

    @staticmethod
    def operation_wrapper(f):
        """Wrap operation method for overriding type conversion.

        If it is a unary operation, the result is still its own type.
        If the other operand is int, it will be converted to its own type.
        If the type of another operand is inconsistent with its own type,
        they are converted to larger size or unsigned type.
        """

        @wraps(f)
        def decorator(self, *args):
            data_type = type(self)

            if args:
                other = args[0]

                if isinstance(other, int):
                    other = data_type(other)

                elif isinstance(self, np.integer):
                    if self.itemsize == other.itemsize:
                        data_type = type(other) \
                            if isinstance(self, np.signedinteger) \
                            else type(self)

                    else:
                        data_type = type(other) \
                            if self.itemsize < other.itemsize \
                            else type(self)

                return data_type(f(self, other))

            return data_type(f(self))

        return decorator


class IntMixin(np.integer):
    """Mixin class of type int."""

    @classmethod
    def get_size(cls) -> int:
        """Get size (bytes) of this type."""
        return cls._SIZE

    @classmethod
    def get_signed(cls) -> bool:
        """Get signed of this type."""
        return issubclass(cls, np.signedinteger)

    @classmethod
    def from_bytes(
            cls,
            data: Union[Iterable[int], SupportsBytes],
            byteorder: str = 'little'
    ):
        """Return a value of this type from given bytes"""
        return cls(int.from_bytes(
            data,
            byteorder=byteorder,
            signed=cls.get_signed()
        ))

    def to_bytes(self, byteorder: str = 'little') -> bytes:
        """Covert this value to bytes."""
        return int(self).to_bytes(
            length=self.get_size(),
            byteorder=byteorder,
            signed=self.get_signed()
        )


class Int8(np.int8, IntMixin, metaclass=IntMeta):
    """Int8"""
    _SIZE = 1


class Int16(np.int16, IntMixin, metaclass=IntMeta):
    """Int16"""
    _SIZE = 2


class Int32(np.int32, IntMixin, metaclass=IntMeta):
    """Int32"""
    _SIZE = 4


class Int64(np.int64, IntMixin, metaclass=IntMeta):
    """Int64"""
    _SIZE = 8


class UInt8(np.uint8, IntMixin, metaclass=IntMeta):
    """UInt8"""
    _SIZE = 1


class UInt16(np.uint16, IntMixin, metaclass=IntMeta):
    """UInt16"""
    _SIZE = 2


class UInt32(np.uint32, IntMixin, metaclass=IntMeta):
    """UInt32"""
    _SIZE = 4


class UInt64(np.uint64, IntMixin, metaclass=IntMeta):
    """UInt64"""
    _SIZE = 8


IntVar = Union[
    Int8, Int16, Int32, Int64,
    UInt8, UInt16, UInt32, UInt64
]

IntType = Type[Union[
    Int8, Int16, Int32, Int64,
    UInt8, UInt16, UInt32, UInt64
]]


def int8(v) -> Int8:
    """Short-hand for `Int8(v)`."""
    return Int8(v)


def int16(v) -> Int16:
    """Short-hand for `Int16(v)`."""
    return Int16(v)


def int32(v) -> Int32:
    """Short-hand for `Int32(v)`."""
    return Int32(v)


def int64(v) -> Int64:
    """Short-hand for `Int64(v)`."""
    return Int64(v)


def uint8(v) -> UInt8:
    """Short-hand for `UInt8(v)`."""
    return UInt8(v)


def uint16(v) -> UInt16:
    """Short-hand for `UInt16(v)`."""
    return UInt16(v)


def uint32(v) -> UInt32:
    """Short-hand for `UInt32(v)`."""
    return UInt32(v)


def uint64(v) -> UInt64:
    """Short-hand for `UInt64(v)`."""
    return UInt64(v)
