"""Implement functions which are used in the code decompiled by IDA."""

from .. import endian
from ..integer import (
    IntType,
    IntVar,
    int8,
    int16,
    int32,
    uint8,
    uint16,
    uint32,
    uint64,
)
from ..utils import get_type, truncate

# Refer to defs.h of IDA.


def last_ind(x: IntVar, part_type: IntType) -> int:
    """Implementation of `LAST_IND`."""
    return x.get_size() // part_type.get_size() - 1


def low_ind(x: IntVar, part_type: IntType) -> int:
    """Implementation of `LOW_IND`."""
    return last_ind(x, part_type) if endian.BYTE_ORDER == endian.BIG_ENDIAN else 0


def high_ind(x: IntVar, part_type: IntType) -> int:
    """Implementation of `HIGH_IND`."""
    return 0 if endian.BYTE_ORDER == endian.BIG_ENDIAN else last_ind(x, part_type)


def byten(x: IntVar, n: int) -> uint8:
    """Implementation of `BYTEn`."""
    return truncate(x, n * 1, uint8)


def wordn(x: IntVar, n: int) -> uint16:
    """Implementation of `WORDn`."""
    return truncate(x, n * 2, uint16)


def dwordn(x: IntVar, n: int) -> uint32:
    """Implementation of `DWORDn`."""
    return truncate(x, n * 4, uint32)


def lobyte(x: IntVar) -> uint8:
    """Implementation of `LOBYTE`."""
    return byten(x, low_ind(x, uint8))


def loword(x: IntVar) -> uint16:
    """Implementation of `LOWORD`."""
    return wordn(x, low_ind(x, uint16))


def lodword(x: IntVar) -> uint32:
    """Implementation of `LODWORD`."""
    return dwordn(x, low_ind(x, uint32))


def hibyte(x: IntVar) -> uint8:
    """Implementation of `HIBYTE`."""
    return byten(x, high_ind(x, uint8))


def hiword(x: IntVar) -> uint16:
    """Implementation of `HIWORD`."""
    return wordn(x, high_ind(x, uint16))


def hidword(x: IntVar) -> uint32:
    """Implementation of `HIDWORD`."""
    return dwordn(x, high_ind(x, uint32))


def byte1(x: IntVar) -> uint8:
    """Implementation of `BYTE1`."""
    return byten(x, 1)


def byte2(x: IntVar) -> uint8:
    """Implementation of `BYTE2`."""
    return byten(x, 2)


def byte3(x: IntVar) -> uint8:
    """Implementation of `BYTE3`."""
    return byten(x, 3)


def byte4(x: IntVar) -> uint8:
    """Implementation of `BYTE4`."""
    return byten(x, 4)


def byte5(x: IntVar) -> uint8:
    """Implementation of `BYTE5`."""
    return byten(x, 5)


def byte6(x: IntVar) -> uint8:
    """Implementation of `BYTE6`."""
    return byten(x, 6)


def byte7(x: IntVar) -> uint8:
    """Implementation of `BYTE7`."""
    return byten(x, 7)


def byte8(x: IntVar) -> uint8:
    """Implementation of `BYTE8`."""
    return byten(x, 8)


def byte9(x: IntVar) -> uint8:
    """Implementation of `BYTE9`."""
    return byten(x, 9)


def byte10(x: IntVar) -> uint8:
    """Implementation of `BYTE10`."""
    return byten(x, 10)


def byte11(x: IntVar) -> uint8:
    """Implementation of `BYTE11`."""
    return byten(x, 11)


def byte12(x: IntVar) -> uint8:
    """Implementation of `BYTE12`."""
    return byten(x, 12)


def byte13(x: IntVar) -> uint8:
    """Implementation of `BYTE13`."""
    return byten(x, 13)


def byte14(x: IntVar) -> uint8:
    """Implementation of `BYTE14`."""
    return byten(x, 14)


def byte15(x: IntVar) -> uint8:
    """Implementation of `BYTE15`."""
    return byten(x, 15)


def word1(x: IntVar) -> uint16:
    """Implementation of `WORD1`."""
    return wordn(x, 1)


def word2(x: IntVar) -> uint16:
    """Implementation of `WORD2`."""
    return wordn(x, 2)


def word3(x: IntVar) -> uint16:
    """Implementation of `WORD3`."""
    return wordn(x, 3)


def word4(x: IntVar) -> uint16:
    """Implementation of `WORD4`."""
    return wordn(x, 4)


def word5(x: IntVar) -> uint16:
    """Implementation of `WORD5`."""
    return wordn(x, 5)


def word6(x: IntVar) -> uint16:
    """Implementation of `WORD6`."""
    return wordn(x, 6)


def word7(x: IntVar) -> uint16:
    """Implementation of `WORD7`."""
    return wordn(x, 7)


def dword1(x: IntVar) -> uint32:
    """Implementation of `DWORD1`."""
    return dwordn(x, 1)


def dword2(x: IntVar) -> uint32:
    """Implementation of `DWORD2`."""
    return dwordn(x, 2)


def dword3(x: IntVar) -> uint32:
    """Implementation of `DWORD3`."""
    return dwordn(x, 3)


def sbyten(x: IntVar, n: int) -> int8:
    """Implementation of `SBYTEn`."""
    return truncate(x, n * 1, int8)


def swordn(x: IntVar, n: int) -> int16:
    """Implementation of `SWORDn`."""
    return truncate(x, n * 2, int16)


def sdwordn(x: IntVar, n: int) -> int32:
    """Implementation of `SDWORDn`."""
    return truncate(x, n * 4, int32)


def slobyte(x: IntVar) -> int8:
    """Implementation of `SLOBYTE`."""
    return sbyten(x, low_ind(x, int8))


def sloword(x: IntVar) -> int16:
    """Implementation of `SLOWORD`."""
    return swordn(x, low_ind(x, int16))


def slodword(x: IntVar) -> int32:
    """Implementation of `SLODWORD`."""
    return sdwordn(x, low_ind(x, int32))


def shibyte(x: IntVar) -> int8:
    """Implementation of `SHIBYTE`."""
    return sbyten(x, high_ind(x, int8))


def shiword(x: IntVar) -> int16:
    """Implementation of `SHIWORD`."""
    return swordn(x, high_ind(x, int16))


def shidword(x: IntVar) -> int32:
    """Implementation of `SHIDWORD`."""
    return sdwordn(x, high_ind(x, int32))


def sbyte1(x: IntVar) -> int8:
    """Implementation of `SBYTE1`."""
    return sbyten(x, 1)


def sbyte2(x: IntVar) -> int8:
    """Implementation of `SBYTE2`."""
    return sbyten(x, 2)


def sbyte3(x: IntVar) -> int8:
    """Implementation of `SBYTE3`."""
    return sbyten(x, 3)


def sbyte4(x: IntVar) -> int8:
    """Implementation of `SBYTE4`."""
    return sbyten(x, 4)


def sbyte5(x: IntVar) -> int8:
    """Implementation of `SBYTE5`."""
    return sbyten(x, 5)


def sbyte6(x: IntVar) -> int8:
    """Implementation of `SBYTE6`."""
    return sbyten(x, 6)


def sbyte7(x: IntVar) -> int8:
    """Implementation of `SBYTE7`."""
    return sbyten(x, 7)


def sbyte8(x: IntVar) -> int8:
    """Implementation of `SBYTE8`."""
    return sbyten(x, 8)


def sbyte9(x: IntVar) -> int8:
    """Implementation of `SBYTE9`."""
    return sbyten(x, 9)


def sbyte10(x: IntVar) -> int8:
    """Implementation of `SBYTE10`."""
    return sbyten(x, 10)


def sbyte11(x: IntVar) -> int8:
    """Implementation of `SBYTE11`."""
    return sbyten(x, 11)


def sbyte12(x: IntVar) -> int8:
    """Implementation of `SBYTE12`."""
    return sbyten(x, 12)


def sbyte13(x: IntVar) -> int8:
    """Implementation of `SBYTE13`."""
    return sbyten(x, 13)


def sbyte14(x: IntVar) -> int8:
    """Implementation of `SBYTE14`."""
    return sbyten(x, 14)


def sbyte15(x: IntVar) -> int8:
    """Implementation of `SBYTE15`."""
    return sbyten(x, 15)


def sword1(x: IntVar) -> int16:
    """Implementation of `SWORD1`."""
    return swordn(x, 1)


def sword2(x: IntVar) -> int16:
    """Implementation of `SWORD2`."""
    return swordn(x, 2)


def sword3(x: IntVar) -> int16:
    """Implementation of `SWORD3`."""
    return swordn(x, 3)


def sword4(x: IntVar) -> int16:
    """Implementation of `SWORD4`."""
    return swordn(x, 4)


def sword5(x: IntVar) -> int16:
    """Implementation of `SWORD5`."""
    return swordn(x, 5)


def sword6(x: IntVar) -> int16:
    """Implementation of `SWORD6`."""
    return swordn(x, 6)


def sword7(x: IntVar) -> int16:
    """Implementation of `SWORD7`."""
    return swordn(x, 7)


def sdword1(x: IntVar) -> int32:
    """Implementation of `SDWORD1`."""
    return sdwordn(x, 1)


def sdword2(x: IntVar) -> int32:
    """Implementation of `SDWORD2`."""
    return sdwordn(x, 2)


def sdword3(x: IntVar) -> int32:
    """Implementation of `SDWORD3`."""
    return sdwordn(x, 3)


def pair(high: IntVar, low: IntVar) -> IntVar:
    """Implementation of `__PAIR__`."""
    size = high.get_size()
    signed = high.get_signed()
    int_type = get_type(size=size * 2, signed=signed)
    return int_type(high) << size * 8 | type(high)(low)


def rol(value: IntVar, count: int) -> IntVar:
    """Implementation of `__ROL__`."""
    data_type = type(value)
    nbits = value.get_size() * 8

    if count > 0:
        count %= nbits
        high = value >> (nbits - count)
        if value.get_signed():
            high &= ~(data_type(-1) << count)
        value <<= count
        value |= high

    else:
        count = -count % nbits
        low = value << (nbits - count)
        value >>= count
        value |= low

    return value


def rol1(value: uint8, count: int) -> uint8:
    """Implementation of `__ROL1__`."""
    return uint8(rol(value, count))


def rol2(value: uint16, count: int) -> uint16:
    """Implementation of `__ROL2__`."""
    return uint16(rol(value, count))


def rol4(value: uint32, count: int) -> uint32:
    """Implementation of `__ROL4__`."""
    return uint32(rol(value, count))


def rol8(value: uint64, count: int) -> uint64:
    """Implementation of `__ROL8__`."""
    return uint64(rol(value, count))


def ror1(value: uint8, count: int) -> uint8:
    """Implementation of `__ROR1__`."""
    return uint8(rol(value, -count))


def ror2(value: uint16, count: int) -> uint16:
    """Implementation of `__ROR2__`."""
    return uint16(rol(value, -count))


def ror4(value: uint32, count: int) -> uint32:
    """Implementation of `__ROR4__`."""
    return uint32(rol(value, -count))


def ror8(value: uint64, count: int) -> uint64:
    """Implementation of `__ROR8__`."""
    return uint64(rol(value, -count))


def mkcshl(value: IntVar, count: int) -> int:
    """Implementation of `__MKCSHL__`."""
    nbits = value.get_size() * 8
    count %= nbits
    return int((value >> (nbits - count)) & 1)


def mkcshr(value: IntVar, count: int) -> int:
    """Implementation of `__MKCSHR__`."""
    return int((value >> (count - 1)) & 1)


def sets(x: IntVar) -> int:
    """Implementation of `__SETS__`."""
    data_type = get_type(size=x.get_size(), signed=True)
    return int(data_type(x) < 0)


def ofsub(x: IntVar, y: IntVar) -> int:
    """Implementation of `__OFSUB__`."""
    if x.get_size() < y.get_size():
        x2 = x
        sx = sets(x2)
        return int((sx ^ sets(y)) & (sx ^ sets(x2 - y)))
    else:
        y2 = y
        sx = sets(x)
        return int((sx ^ sets(y2)) & (sx ^ sets(x - y2)))


def ofadd(x: IntVar, y: IntVar) -> int:
    """Implementation of `__OFADD__`."""
    if x.get_size() < y.get_size():
        x2 = x
        sx = sets(x2)
        return int(((1 ^ sx) ^ sets(y)) & (sx ^ sets(x2 + y)))
    else:
        y2 = y
        sx = sets(x)
        return int(((1 ^ sx) ^ sets(y2)) & (sx ^ sets(x + y2)))


def cfsub(x: IntVar, y: IntVar) -> int:
    """Implementation of `__CFSUB__`."""
    size = max(x.get_size(), y.get_size())
    data_type = get_type(size=size, signed=False)
    return int(data_type(x) < data_type(y))


def cfadd(x: IntVar, y: IntVar) -> int:
    """Implementation of `__CFADD__`."""
    size = max(x.get_size(), y.get_size())
    data_type = get_type(size=size, signed=False)
    return int(data_type(x) > data_type(x + y))


# Refer to https://gcc.gnu.org/onlinedocs/gcc/Other-Builtins.html.


def bswap32(value: uint32) -> uint32:
    """Implementation of `bswap32`."""
    return value.from_bytes(value.to_bytes()[::-1])


def clz(x: IntVar) -> int:
    """Implementation of `__clz`."""
    return x.get_size() * 8 - len(bin(int(x))[2:])
