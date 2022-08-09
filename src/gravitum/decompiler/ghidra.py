"""Implement functions which are used in the code decompiled by Ghidra."""

from typing import Type, TypeVar

from .ida import cfadd, ofsub, ofadd
from ..types import Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32, UInt64
from ..utils import get_type

# Refer to https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/Features/Decompiler/src/main/help/help/topics/DecompilePlugin/DecompilerConcepts.html    # noqa: E501

_T1 = TypeVar("_T1", Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32, UInt64)
_T2 = TypeVar("_T2", Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32, UInt64)


def _truncate(x: _T1, c: int, to_type: Type[_T2]) -> _T2:
    """Truncation operation."""
    return to_type.from_bytes(x.to_bytes()[c : c + to_type.get_size()])


def _zero_extend(x: _T1, from_type: Type[_T1], to_type: Type[_T2]) -> _T2:
    """Zero-extension operator."""
    return to_type.from_bytes(from_type(x).to_bytes())


def _sign_extend(x: _T1, from_type: Type[_T1], to_type: Type[_T2]) -> _T2:
    """Sign-extension operator."""
    t1 = get_type(size=from_type.get_size(), signed=True)
    t2 = get_type(size=to_type.get_size(), signed=True)
    return to_type.from_bytes(t2.from_bytes(t1(x).to_bytes()).to_bytes())


def sub21(x: UInt16, c: int) -> UInt8:
    """Implementation of `SUB21`."""
    return _truncate(x, c, UInt8)


def sub41(x: UInt32, c: int) -> UInt8:
    """Implementation of `SUB41`."""
    return _truncate(x, c, UInt8)


def sub42(x: UInt32, c: int) -> UInt16:
    """Implementation of `SUB42`."""
    return _truncate(x, c, UInt16)


def sub81(x: UInt64, c: int) -> UInt8:
    """Implementation of `SUB81`."""
    return _truncate(x, c, UInt8)


def sub82(x: UInt64, c: int) -> UInt16:
    """Implementation of `SUB82`."""
    return _truncate(x, c, UInt16)


def sub84(x: UInt64, c: int) -> UInt32:
    """Implementation of `SUB84`."""
    return _truncate(x, c, UInt32)


def zext12(x: UInt8) -> UInt16:
    """Implementation of `ZEXT12`."""
    return _zero_extend(x, UInt8, UInt16)


def zext14(x: UInt8) -> UInt32:
    """Implementation of `ZEXT14`."""
    return _zero_extend(x, UInt8, UInt32)


def zext18(x: UInt8) -> UInt64:
    """Implementation of `ZEXT18`."""
    return _zero_extend(x, UInt8, UInt64)


def zext24(x: UInt16) -> UInt32:
    """Implementation of `ZEXT14`."""
    return _zero_extend(x, UInt16, UInt32)


def zext28(x: UInt16) -> UInt64:
    """Implementation of `ZEXT18`."""
    return _zero_extend(x, UInt16, UInt64)


def zext48(x: UInt32) -> UInt64:
    """Implementation of `ZEXT48`."""
    return _zero_extend(x, UInt32, UInt64)


def sext12(x: UInt8) -> UInt16:
    """Implementation of `SEXT12`."""
    return _sign_extend(x, UInt8, UInt16)


def sext14(x: UInt8) -> UInt32:
    """Implementation of `SEXT14`."""
    return _sign_extend(x, UInt8, UInt32)


def sext18(x: UInt8) -> UInt64:
    """Implementation of `SEXT18`."""
    return _sign_extend(x, UInt8, UInt64)


def sext24(x: UInt16) -> UInt32:
    """Implementation of `SEXT14`."""
    return _sign_extend(x, UInt16, UInt32)


def sext28(x: UInt16) -> UInt64:
    """Implementation of `SEXT18`."""
    return _sign_extend(x, UInt16, UInt64)


def sext48(x: UInt32) -> UInt64:
    """Implementation of `SEXT48`."""
    return _sign_extend(x, UInt32, UInt64)


def sborrow1(x: UInt8, y: UInt8) -> int:
    """Implementation of `SBORROW1`."""
    return ofsub(x, y)


def sborrow2(x: UInt16, y: UInt16) -> int:
    """Implementation of `SBORROW2`."""
    return ofsub(x, y)


def sborrow4(x: UInt32, y: UInt32) -> int:
    """Implementation of `SBORROW4`."""
    return ofsub(x, y)


def sborrow8(x: UInt64, y: UInt64) -> int:
    """Implementation of `SBORROW8`."""
    return ofsub(x, y)


def carry1(x: UInt8, y: UInt8) -> int:
    """Implementation of `CARRY1`."""
    return cfadd(x, y)


def carry2(x: UInt16, y: UInt16) -> int:
    """Implementation of `CARRY2`."""
    return cfadd(x, y)


def carry4(x: UInt32, y: UInt32) -> int:
    """Implementation of `CARRY4`."""
    return cfadd(x, y)


def carry8(x: UInt64, y: UInt64) -> int:
    """Implementation of `CARRY8`."""
    return cfadd(x, y)


def scarry1(x: Int8, y: Int8) -> int:
    """Implementation of `SCARRY1`."""
    return ofadd(x, y)


def scarry2(x: Int16, y: Int16) -> int:
    """Implementation of `SCARRY2`."""
    return ofadd(x, y)


def scarry4(x: Int32, y: Int32) -> int:
    """Implementation of `SCARRY4`."""
    return ofadd(x, y)


def scarry8(x: Int64, y: Int64) -> int:
    """Implementation of `SCARRY8`."""
    return ofadd(x, y)
