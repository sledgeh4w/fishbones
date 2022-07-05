"""Implement functions which are used in the code decompiled by Ghidra."""

from typing import Type, TypeVar

from .ida import cfadd, ofsub, ofadd
from ..types import Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32, UInt64
from ..utils import get_type

# Refer to https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra
# /Features/Decompiler/src/main/help/help/topics/DecompilePlugin
# /DecompilerConcepts.html

InVar = TypeVar('InVar', Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32,
                UInt64)
OutVar = TypeVar('OutVar', Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32,
                 UInt64)


def truncate(x: InVar, c: int, to_type: Type[OutVar]) -> OutVar:
    """Truncation operation."""
    return to_type.from_bytes(x.to_bytes()[c:c + to_type.get_size()])


def sub21(x: UInt16, c: int) -> UInt8:
    """Implementation of `SUB21`."""
    return truncate(x, c, UInt8)


def sub41(x: UInt32, c: int) -> UInt8:
    """Implementation of `SUB41`."""
    return truncate(x, c, UInt8)


def sub42(x: UInt32, c: int) -> UInt16:
    """Implementation of `SUB42`."""
    return truncate(x, c, UInt16)


def sub81(x: UInt64, c: int) -> UInt8:
    """Implementation of `SUB81`."""
    return truncate(x, c, UInt8)


def sub82(x: UInt64, c: int) -> UInt16:
    """Implementation of `SUB82`."""
    return truncate(x, c, UInt16)


def sub84(x: UInt64, c: int) -> UInt32:
    """Implementation of `SUB84`."""
    return truncate(x, c, UInt32)


def zero_extend(x: InVar, from_type: Type[InVar],
                to_type: Type[OutVar]) -> OutVar:
    """Zero-extension operator."""
    return to_type.from_bytes(from_type(x).to_bytes())


def zext12(x: UInt8) -> UInt16:
    """Implementation of `ZEXT12`."""
    return zero_extend(x, UInt8, UInt16)


def zext14(x: UInt8) -> UInt32:
    """Implementation of `ZEXT14`."""
    return zero_extend(x, UInt8, UInt32)


def zext18(x: UInt8) -> UInt64:
    """Implementation of `ZEXT18`."""
    return zero_extend(x, UInt8, UInt64)


def zext24(x: UInt16) -> UInt32:
    """Implementation of `ZEXT14`."""
    return zero_extend(x, UInt16, UInt32)


def zext28(x: UInt16) -> UInt64:
    """Implementation of `ZEXT18`."""
    return zero_extend(x, UInt16, UInt64)


def zext48(x: UInt32) -> UInt64:
    """Implementation of `ZEXT48`."""
    return zero_extend(x, UInt32, UInt64)


def sign_extend(x: InVar, from_type: Type[InVar],
                to_type: Type[OutVar]) -> OutVar:
    """Sign-extension operator."""
    t1 = get_type(size=from_type.get_size(), signed=True)
    t2 = get_type(size=to_type.get_size(), signed=True)
    return to_type.from_bytes(t2.from_bytes(t1(x).to_bytes()).to_bytes())


def sext12(x: UInt8) -> UInt16:
    """Implementation of `SEXT12`."""
    return sign_extend(x, UInt8, UInt16)


def sext14(x: UInt8) -> UInt32:
    """Implementation of `SEXT14`."""
    return sign_extend(x, UInt8, UInt32)


def sext18(x: UInt8) -> UInt64:
    """Implementation of `SEXT18`."""
    return sign_extend(x, UInt8, UInt64)


def sext24(x: UInt16) -> UInt32:
    """Implementation of `SEXT14`."""
    return sign_extend(x, UInt16, UInt32)


def sext28(x: UInt16) -> UInt64:
    """Implementation of `SEXT18`."""
    return sign_extend(x, UInt16, UInt64)


def sext48(x: UInt32) -> UInt64:
    """Implementation of `SEXT48`."""
    return sign_extend(x, UInt32, UInt64)


def sborrow1(x: UInt8, y: UInt8) -> Int8:
    """Implementation of `SBORROW1`."""
    return ofsub(x, y)


def sborrow2(x: UInt16, y: UInt16) -> Int8:
    """Implementation of `SBORROW2`."""
    return ofsub(x, y)


def sborrow4(x: UInt32, y: UInt32) -> Int8:
    """Implementation of `SBORROW4`."""
    return ofsub(x, y)


def sborrow8(x: UInt64, y: UInt64) -> Int8:
    """Implementation of `SBORROW8`."""
    return ofsub(x, y)


def carry1(x: UInt8, y: UInt8) -> Int8:
    """Implementation of `CARRY1`."""
    return cfadd(x, y)


def carry2(x: UInt16, y: UInt16) -> Int8:
    """Implementation of `CARRY2`."""
    return cfadd(x, y)


def carry4(x: UInt32, y: UInt32) -> Int8:
    """Implementation of `CARRY4`."""
    return cfadd(x, y)


def carry8(x: UInt64, y: UInt64) -> Int8:
    """Implementation of `CARRY8`."""
    return cfadd(x, y)


def scarry1(x: Int8, y: Int8) -> Int8:
    """Implementation of `SCARRY1`."""
    return ofadd(x, y)


def scarry2(x: Int16, y: Int16) -> Int8:
    """Implementation of `SCARRY2`."""
    return ofadd(x, y)


def scarry4(x: Int32, y: Int32) -> Int8:
    """Implementation of `SCARRY4`."""
    return ofadd(x, y)


def scarry8(x: Int64, y: Int64) -> Int8:
    """Implementation of `SCARRY8`."""
    return ofadd(x, y)
