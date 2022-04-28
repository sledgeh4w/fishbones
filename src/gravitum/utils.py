from typing import Union

from .types import (
    Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32, UInt64, IntType)
from .virtualpointer import VirtualPointer


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


def uint8(v) -> Int8:
    """Short-hand for `UInt8(v)`."""
    return UInt8(v)


def uint16(v) -> Int16:
    """Short-hand for `UInt16(v)`."""
    return UInt16(v)


def uint32(v) -> Int32:
    """Short-hand for `UInt32(v)`."""
    return UInt32(v)


def uint64(v) -> Int64:
    """Short-hand for `UInt64(v)`."""
    return UInt64(v)


def vptr(
        source: bytearray,
        data_type: Union[IntType, str] = UInt8
) -> VirtualPointer:
    """Short-hand for `VirtualPointer(source, data_type)`."""
    return VirtualPointer(source=source, data_type=data_type)
