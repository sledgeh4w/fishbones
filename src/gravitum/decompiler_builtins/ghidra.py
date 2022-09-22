"""Implement functions which are used in the code decompiled by Ghidra."""

from ..integer import uint8, uint16, uint32, uint64
from .ida import cfadd, ofadd, ofsub
from .utils import sign_extend, truncate, zero_extend

# Refer to https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/Features/Decompiler/src/main/help/help/topics/DecompilePlugin/DecompilerConcepts.html    # noqa: E501


def sub21(x, c):
    """Implementation of `SUB21`."""
    return truncate(x, c, uint8)


def sub41(x, c):
    """Implementation of `SUB41`."""
    return truncate(x, c, uint8)


def sub42(x, c):
    """Implementation of `SUB42`."""
    return truncate(x, c, uint16)


def sub81(x, c):
    """Implementation of `SUB81`."""
    return truncate(x, c, uint8)


def sub82(x, c):
    """Implementation of `SUB82`."""
    return truncate(x, c, uint16)


def sub84(x, c):
    """Implementation of `SUB84`."""
    return truncate(x, c, uint32)


def zext12(x):
    """Implementation of `ZEXT12`."""
    return zero_extend(x, uint16)


def zext14(x):
    """Implementation of `ZEXT14`."""
    return zero_extend(x, uint32)


def zext18(x):
    """Implementation of `ZEXT18`."""
    return zero_extend(x, uint64)


def zext24(x):
    """Implementation of `ZEXT24`."""
    return zero_extend(x, uint32)


def zext28(x):
    """Implementation of `ZEXT28`."""
    return zero_extend(x, uint64)


def zext48(x):
    """Implementation of `ZEXT48`."""
    return zero_extend(x, uint64)


def sext12(x):
    """Implementation of `SEXT12`."""
    return sign_extend(x, uint16)


def sext14(x):
    """Implementation of `SEXT14`."""
    return sign_extend(x, uint32)


def sext18(x):
    """Implementation of `SEXT18`."""
    return sign_extend(x, uint64)


def sext24(x):
    """Implementation of `SEXT24`."""
    return sign_extend(x, uint32)


def sext28(x):
    """Implementation of `SEXT28`."""
    return sign_extend(x, uint64)


def sext48(x):
    """Implementation of `SEXT48`."""
    return sign_extend(x, uint64)


def sborrow1(x, y):
    """Implementation of `SBORROW1`."""
    return ofsub(x, y)


def sborrow2(x, y):
    """Implementation of `SBORROW2`."""
    return ofsub(x, y)


def sborrow4(x, y):
    """Implementation of `SBORROW4`."""
    return ofsub(x, y)


def sborrow8(x, y):
    """Implementation of `SBORROW8`."""
    return ofsub(x, y)


def carry1(x, y):
    """Implementation of `CARRY1`."""
    return cfadd(x, y)


def carry2(x, y):
    """Implementation of `CARRY2`."""
    return cfadd(x, y)


def carry4(x, y):
    """Implementation of `CARRY4`."""
    return cfadd(x, y)


def carry8(x, y):
    """Implementation of `CARRY8`."""
    return cfadd(x, y)


def scarry1(x, y):
    """Implementation of `SCARRY1`."""
    return ofadd(x, y)


def scarry2(x, y):
    """Implementation of `SCARRY2`."""
    return ofadd(x, y)


def scarry4(x, y):
    """Implementation of `SCARRY4`."""
    return ofadd(x, y)


def scarry8(x, y):
    """Implementation of `SCARRY8`."""
    return ofadd(x, y)
