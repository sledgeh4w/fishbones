"""Implement functions which are used in the code decompiled by IDA."""

import sys
from typing import Type, TypeVar

from ..consts import BIG_ENDIAN, LITTLE_ENDIAN
from ..integer import (
    Integer,
    Int8,
    Int16,
    Int32,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
    get_type_size,
)


if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


_T = TypeVar("_T", bound=Integer)


# Refer to defs.h of IDA.


def truncate(x: Integer, c: int, to_type: Type[_T]) -> _T:
    """Truncate."""
    data = x.to_bytes()
    to_size = get_type_size(to_type)
    return to_type.from_bytes(data[c : c + to_size])


def zero_extend(x: Integer, to_type: Type[_T]) -> _T:
    """Zero extend."""
    return to_type.from_bytes(x.to_bytes())


def sign_extend(x: Integer, to_type: Type[_T]) -> _T:
    """Sign extend."""
    t1 = Integer.get_type(size=x.size, signed=True)
    t2 = Integer.get_type(size=get_type_size(to_type), signed=True)
    return to_type.from_bytes(t2.from_bytes(t1(x).to_bytes()).to_bytes())


def last_ind(x: Integer, part_type: Type[Integer]) -> int:
    """Implementation of `LAST_IND`."""
    return x.size // get_type_size(part_type) - 1


def low_ind(
    x: Integer,
    part_type: Type[Integer],
    byteorder: Literal["big", "little"] = LITTLE_ENDIAN,
) -> int:
    """Implementation of `LOW_IND`."""
    return last_ind(x, part_type) if byteorder == BIG_ENDIAN else 0


def high_ind(
    x: Integer,
    part_type: Type[Integer],
    byteorder: Literal["big", "little"] = LITTLE_ENDIAN,
) -> int:
    """Implementation of `HIGH_IND`."""
    return 0 if byteorder == BIG_ENDIAN else last_ind(x, part_type)


def byten(x: Integer, n: int) -> UInt8:
    """Implementation of `BYTEn`."""
    return truncate(x, n * 1, UInt8)


def wordn(x: Integer, n: int) -> UInt16:
    """Implementation of `WORDn`."""
    return truncate(x, n * 2, UInt16)


def dwordn(x: Integer, n: int) -> UInt32:
    """Implementation of `DWORDn`."""
    return truncate(x, n * 4, UInt32)


def lobyte(x: Integer) -> UInt8:
    """Implementation of `LOBYTE`."""
    return byten(x, low_ind(x, UInt8))


def loword(x: Integer) -> UInt16:
    """Implementation of `LOWORD`."""
    return wordn(x, low_ind(x, UInt16))


def lodword(x: Integer) -> UInt32:
    """Implementation of `LODWORD`."""
    return dwordn(x, low_ind(x, UInt32))


def hibyte(x: Integer) -> UInt8:
    """Implementation of `HIBYTE`."""
    return byten(x, high_ind(x, UInt8))


def hiword(x: Integer) -> UInt16:
    """Implementation of `HIWORD`."""
    return wordn(x, high_ind(x, UInt16))


def hidword(x: Integer) -> UInt32:
    """Implementation of `HIDWORD`."""
    return dwordn(x, high_ind(x, UInt32))


def byte1(x: Integer) -> UInt8:
    """Implementation of `BYTE1`."""
    return byten(x, 1)


def byte2(x: Integer) -> UInt8:
    """Implementation of `BYTE2`."""
    return byten(x, 2)


def byte3(x: Integer) -> UInt8:
    """Implementation of `BYTE3`."""
    return byten(x, 3)


def byte4(x: Integer) -> UInt8:
    """Implementation of `BYTE4`."""
    return byten(x, 4)


def byte5(x: Integer) -> UInt8:
    """Implementation of `BYTE5`."""
    return byten(x, 5)


def byte6(x: Integer) -> UInt8:
    """Implementation of `BYTE6`."""
    return byten(x, 6)


def byte7(x: Integer) -> UInt8:
    """Implementation of `BYTE7`."""
    return byten(x, 7)


def byte8(x: Integer) -> UInt8:
    """Implementation of `BYTE8`."""
    return byten(x, 8)


def byte9(x: Integer) -> UInt8:
    """Implementation of `BYTE9`."""
    return byten(x, 9)


def byte10(x: Integer) -> UInt8:
    """Implementation of `BYTE10`."""
    return byten(x, 10)


def byte11(x: Integer) -> UInt8:
    """Implementation of `BYTE11`."""
    return byten(x, 11)


def byte12(x: Integer) -> UInt8:
    """Implementation of `BYTE12`."""
    return byten(x, 12)


def byte13(x: Integer) -> UInt8:
    """Implementation of `BYTE13`."""
    return byten(x, 13)


def byte14(x: Integer) -> UInt8:
    """Implementation of `BYTE14`."""
    return byten(x, 14)


def byte15(x: Integer) -> UInt8:
    """Implementation of `BYTE15`."""
    return byten(x, 15)


def word1(x: Integer) -> UInt16:
    """Implementation of `WORD1`."""
    return wordn(x, 1)


def word2(x: Integer) -> UInt16:
    """Implementation of `WORD2`."""
    return wordn(x, 2)


def word3(x: Integer) -> UInt16:
    """Implementation of `WORD3`."""
    return wordn(x, 3)


def word4(x: Integer) -> UInt16:
    """Implementation of `WORD4`."""
    return wordn(x, 4)


def word5(x: Integer) -> UInt16:
    """Implementation of `WORD5`."""
    return wordn(x, 5)


def word6(x: Integer) -> UInt16:
    """Implementation of `WORD6`."""
    return wordn(x, 6)


def word7(x: Integer) -> UInt16:
    """Implementation of `WORD7`."""
    return wordn(x, 7)


def dword1(x: Integer) -> UInt32:
    """Implementation of `DWORD1`."""
    return dwordn(x, 1)


def dword2(x: Integer) -> UInt32:
    """Implementation of `DWORD2`."""
    return dwordn(x, 2)


def dword3(x: Integer) -> UInt32:
    """Implementation of `DWORD3`."""
    return dwordn(x, 3)


def sbyten(x: Integer, n: int) -> Int8:
    """Implementation of `SBYTEn`."""
    return truncate(x, n * 1, Int8)


def swordn(x: Integer, n: int) -> Int16:
    """Implementation of `SWORDn`."""
    return truncate(x, n * 2, Int16)


def sdwordn(x: Integer, n: int) -> Int32:
    """Implementation of `SDWORDn`."""
    return truncate(x, n * 4, Int32)


def slobyte(x: Integer) -> Int8:
    """Implementation of `SLOBYTE`."""
    return sbyten(x, low_ind(x, Int8))


def sloword(x: Integer) -> Int16:
    """Implementation of `SLOWORD`."""
    return swordn(x, low_ind(x, Int16))


def slodword(x: Integer) -> Int32:
    """Implementation of `SLODWORD`."""
    return sdwordn(x, low_ind(x, Int32))


def shibyte(x: Integer) -> Int8:
    """Implementation of `SHIBYTE`."""
    return sbyten(x, high_ind(x, Int8))


def shiword(x: Integer) -> Int16:
    """Implementation of `SHIWORD`."""
    return swordn(x, high_ind(x, Int16))


def shidword(x: Integer) -> Int32:
    """Implementation of `SHIDWORD`."""
    return sdwordn(x, high_ind(x, Int32))


def sbyte1(x: Integer) -> Int8:
    """Implementation of `SBYTE1`."""
    return sbyten(x, 1)


def sbyte2(x: Integer) -> Int8:
    """Implementation of `SBYTE2`."""
    return sbyten(x, 2)


def sbyte3(x: Integer) -> Int8:
    """Implementation of `SBYTE3`."""
    return sbyten(x, 3)


def sbyte4(x: Integer) -> Int8:
    """Implementation of `SBYTE4`."""
    return sbyten(x, 4)


def sbyte5(x: Integer) -> Int8:
    """Implementation of `SBYTE5`."""
    return sbyten(x, 5)


def sbyte6(x: Integer) -> Int8:
    """Implementation of `SBYTE6`."""
    return sbyten(x, 6)


def sbyte7(x: Integer) -> Int8:
    """Implementation of `SBYTE7`."""
    return sbyten(x, 7)


def sbyte8(x: Integer) -> Int8:
    """Implementation of `SBYTE8`."""
    return sbyten(x, 8)


def sbyte9(x: Integer) -> Int8:
    """Implementation of `SBYTE9`."""
    return sbyten(x, 9)


def sbyte10(x: Integer) -> Int8:
    """Implementation of `SBYTE10`."""
    return sbyten(x, 10)


def sbyte11(x: Integer) -> Int8:
    """Implementation of `SBYTE11`."""
    return sbyten(x, 11)


def sbyte12(x: Integer) -> Int8:
    """Implementation of `SBYTE12`."""
    return sbyten(x, 12)


def sbyte13(x: Integer) -> Int8:
    """Implementation of `SBYTE13`."""
    return sbyten(x, 13)


def sbyte14(x: Integer) -> Int8:
    """Implementation of `SBYTE14`."""
    return sbyten(x, 14)


def sbyte15(x: Integer) -> Int8:
    """Implementation of `SBYTE15`."""
    return sbyten(x, 15)


def sword1(x: Integer) -> Int16:
    """Implementation of `SWORD1`."""
    return swordn(x, 1)


def sword2(x: Integer) -> Int16:
    """Implementation of `SWORD2`."""
    return swordn(x, 2)


def sword3(x: Integer) -> Int16:
    """Implementation of `SWORD3`."""
    return swordn(x, 3)


def sword4(x: Integer) -> Int16:
    """Implementation of `SWORD4`."""
    return swordn(x, 4)


def sword5(x: Integer) -> Int16:
    """Implementation of `SWORD5`."""
    return swordn(x, 5)


def sword6(x: Integer) -> Int16:
    """Implementation of `SWORD6`."""
    return swordn(x, 6)


def sword7(x: Integer) -> Int16:
    """Implementation of `SWORD7`."""
    return swordn(x, 7)


def sdword1(x: Integer) -> Int32:
    """Implementation of `SDWORD1`."""
    return sdwordn(x, 1)


def sdword2(x: Integer) -> Int32:
    """Implementation of `SDWORD2`."""
    return sdwordn(x, 2)


def sdword3(x: Integer) -> Int32:
    """Implementation of `SDWORD3`."""
    return sdwordn(x, 3)


def pair(high: Integer, low: Integer) -> Integer:
    """Implementation of `__PAIR__`."""
    int_type = Integer.get_type(size=high.size * 2, signed=high.signed)
    return int_type(high) << high.size * 8 | type(high)(low)


def rol(value: Integer, count: int) -> Integer:
    """Implementation of `__ROL__`."""
    data_type = type(value)
    nbits = value.size * 8

    if count > 0:
        count %= nbits
        high = value >> (nbits - count)
        if value.signed:
            high &= ~(data_type(-1) << count)
        value <<= count
        value |= high

    else:
        count = -count % nbits
        low = value << (nbits - count)
        value >>= count
        value |= low

    return value


def rol1(value: UInt8, count: int) -> UInt8:
    """Implementation of `__ROL1__`."""
    return UInt8(rol(value, count))


def rol2(value: UInt16, count: int) -> UInt16:
    """Implementation of `__ROL2__`."""
    return UInt16(rol(value, count))


def rol4(value: UInt32, count: int) -> UInt32:
    """Implementation of `__ROL4__`."""
    return UInt32(rol(value, count))


def rol8(value: UInt64, count: int) -> UInt64:
    """Implementation of `__ROL8__`."""
    return UInt64(rol(value, count))


def ror1(value: UInt8, count: int) -> UInt8:
    """Implementation of `__ROR1__`."""
    return UInt8(rol(value, -count))


def ror2(value: UInt16, count: int) -> UInt16:
    """Implementation of `__ROR2__`."""
    return UInt16(rol(value, -count))


def ror4(value: UInt32, count: int) -> UInt32:
    """Implementation of `__ROR4__`."""
    return UInt32(rol(value, -count))


def ror8(value: UInt64, count: int) -> UInt64:
    """Implementation of `__ROR8__`."""
    return UInt64(rol(value, -count))


def mkcshl(value: Integer, count: int) -> int:
    """Implementation of `__MKCSHL__`."""
    nbits = value.size * 8
    count %= nbits
    return int((value >> (nbits - count)) & 1)


def mkcshr(value: Integer, count: int) -> int:
    """Implementation of `__MKCSHR__`."""
    return int((value >> (count - 1)) & 1)


def sets(x: Integer) -> int:
    """Implementation of `__SETS__`."""
    data_type = Integer.get_type(size=x.size, signed=True)
    return int(data_type(x) < 0)


def ofsub(x: Integer, y: Integer) -> int:
    """Implementation of `__OFSUB__`."""
    if x.size < y.size:
        x2 = x
        sx = sets(x2)
        return int((sx ^ sets(y)) & (sx ^ sets(x2 - y)))
    else:
        y2 = y
        sx = sets(x)
        return int((sx ^ sets(y2)) & (sx ^ sets(x - y2)))


def ofadd(x: Integer, y: Integer) -> int:
    """Implementation of `__OFADD__`."""
    if x.size < y.size:
        x2 = x
        sx = sets(x2)
        return int(((1 ^ sx) ^ sets(y)) & (sx ^ sets(x2 + y)))
    else:
        y2 = y
        sx = sets(x)
        return int(((1 ^ sx) ^ sets(y2)) & (sx ^ sets(x + y2)))


def cfsub(x: Integer, y: Integer) -> int:
    """Implementation of `__CFSUB__`."""
    size = max(x.size, y.size)
    data_type = Integer.get_type(size=size, signed=False)
    return int(data_type(x) < data_type(y))


def cfadd(x: Integer, y: Integer) -> int:
    """Implementation of `__CFADD__`."""
    size = max(x.size, y.size)
    data_type = Integer.get_type(size=size, signed=False)
    return int(data_type(x) > data_type(x + y))


# Refer to https://gcc.gnu.org/onlinedocs/gcc/Other-Builtins.html.


def bswap32(value: UInt32) -> UInt32:
    """Implementation of `bswap32`."""
    return value.from_bytes(value.to_bytes()[::-1])


def clz(x: Integer) -> int:
    """Implementation of `__clz`."""
    return x.size * 8 - len(bin(int(x))[2:])
