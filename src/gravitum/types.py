import re
import sys
from functools import wraps
from typing import Union, Type, SupportsBytes, Iterable

import numpy as np

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = [
    'IntVar', 'IntType', 'IntMeta', 'IntBase', 'Int8', 'Int16', 'Int32',
    'Int64', 'UInt8', 'UInt16', 'UInt32', 'UInt64', 'int8', 'int16', 'int32',
    'int64', 'uint8', 'uint16', 'uint32', 'uint64'
]

ByteOrder = Literal['little', 'big']

IntVar = Union['Int8', 'Int16', 'Int32', 'Int64', 'UInt8', 'UInt16', 'UInt32',
               'UInt64']

IntType = Type[Union['Int8', 'Int16', 'Int32', 'Int64', 'UInt8', 'UInt16',
                     'UInt32', 'UInt64']]


class IntMeta(type):
    """Meta class of integer type."""

    _OVERRIDE_OPERATIONS = [
        '__neg__', '__pos__', '__invert__', '__add__', '__radd__', '__iadd__',
        '__sub__', '__rsub__', '__isub__', '__mul__', '__rmul__', '__imul__',
        '__truediv__', '__rtruediv__', '__itruediv__', '__floordiv__',
        '__rfloordiv__', '__ifloordiv__', '__mod__', '__rmod__', '__imod__',
        '__and__', '__rand__', '__iand__', '__or__', '__ror__', '__ior__',
        '__xor__', '__rxor__', '__ixor__', '__lshift__', '__rlshift__',
        '__ilshift__', '__rshift__', '__rrshift__', '__irshift__'
    ]

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)

        size = int(re.match(r'(U*)Int(\d+)', cls.__name__).group(2)) // 8
        setattr(cls, '_DATA_SIZE', size)

        for op in cls._OVERRIDE_OPERATIONS:
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
                        value = (other if isinstance(self, np.signedinteger)
                                 else self)
                    else:
                        value = (other
                                 if self.itemsize < other.itemsize else self)

                    data_type = type(value)

                return data_type(f(self, other))

            return data_type(f(self))

        return decorator


class IntBase(np.integer):
    """Base class of integer type."""

    def __add__(self, other) -> IntVar:
        pass

    def __radd__(self, other) -> IntVar:
        pass

    def __sub__(self, other) -> IntVar:
        pass

    def __rsub__(self, other) -> IntVar:
        pass

    def __mul__(self, other) -> IntVar:
        pass

    def __rmul__(self, other) -> IntVar:
        pass

    def __truediv__(self, other) -> IntVar:
        pass

    def __rtruediv__(self, other) -> IntVar:
        pass

    def __floordiv__(self, other) -> IntVar:
        pass

    def __rfloordiv__(self, other) -> IntVar:
        pass

    def __mod__(self, other) -> IntVar:
        pass

    def __rmod__(self, other) -> IntVar:
        pass

    def __and__(self, other) -> IntVar:
        pass

    def __rand__(self, other) -> IntVar:
        pass

    def __or__(self, other) -> IntVar:
        pass

    def __ror__(self, other) -> IntVar:
        pass

    def __xor__(self, other) -> IntVar:
        pass

    def __rxor__(self, other) -> IntVar:
        pass

    def __lshift__(self, other) -> IntVar:
        pass

    def __rlshift__(self, other) -> IntVar:
        pass

    def __rshift__(self, other) -> IntVar:
        pass

    def __rrshift__(self, other) -> IntVar:
        pass

    @classmethod
    def get_size(cls) -> int:
        """Get size (bytes) of this type."""
        return cls._DATA_SIZE

    @classmethod
    def get_signed(cls) -> bool:
        """Get signed of this type."""
        return issubclass(cls, np.signedinteger)

    @classmethod
    def from_bytes(cls,
                   data: Union[Iterable[int], SupportsBytes],
                   byteorder: ByteOrder = 'little'):
        """Return a value of this type from given bytes"""
        return cls(
            int.from_bytes(data, byteorder=byteorder, signed=cls.get_signed()))

    def to_bytes(self, byteorder: ByteOrder = 'little') -> bytes:
        """Covert this value to bytes."""
        return int(self).to_bytes(length=self.get_size(),
                                  byteorder=byteorder,
                                  signed=self.get_signed())


class Int8(np.int8, IntBase, metaclass=IntMeta):
    """Int8"""


class Int16(np.int16, IntBase, metaclass=IntMeta):
    """Int16"""


class Int32(np.int32, IntBase, metaclass=IntMeta):
    """Int32"""


class Int64(np.int64, IntBase, metaclass=IntMeta):
    """Int64"""


class UInt8(np.uint8, IntBase, metaclass=IntMeta):
    """UInt8"""


class UInt16(np.uint16, IntBase, metaclass=IntMeta):
    """UInt16"""


class UInt32(np.uint32, IntBase, metaclass=IntMeta):
    """UInt32"""


class UInt64(np.uint64, IntBase, metaclass=IntMeta):
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
