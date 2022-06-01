"""Implement functions which are used in the code decompiled by Ghidra."""

from .ida import cfadd, ofadd
from .types import Int8, Int32, Int64, UInt32, UInt64

# Refer to https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra
# /Features/Decompiler/src/main/help/help/topics/DecompilePlugin
# /DecompilerConcepts.html


def carry4(x: UInt32, y: UInt32) -> Int8:
    """Implementation of `CARRY4`."""
    return cfadd(x, y)


def carry8(x: UInt64, y: UInt64) -> Int8:
    """Implementation of `CARRY8`."""
    return cfadd(x, y)


def scarry4(x: Int32, y: Int32) -> Int8:
    """Implementation of `SCARRY4`."""
    return ofadd(x, y)


def scarry8(x: Int64, y: Int64) -> Int8:
    """Implementation of `SCARRY8`."""
    return ofadd(x, y)
