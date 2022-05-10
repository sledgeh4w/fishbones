"""Implement functions which are used in the code decompiled by IDA."""

from .types import (
    Int8, Int16, Int32, UInt8, UInt16, UInt32, UInt64, IntVar, IntType,
    get_type)

BIG_ENDIAN = 'big'
LITTLE_ENDIAN = 'little'

# Default use little endian.
BYTE_ORDER = LITTLE_ENDIAN


# Refer to defs.h of IDA.


def last_ind(x: IntVar, part_type: IntType) -> int:
    """Implementation for `LAST_IND`."""
    return x.get_size() // part_type.get_size() - 1


def low_ind(x: IntVar, part_type: IntType) -> int:
    """Implementation for `LOW_IND`."""
    return last_ind(x, part_type) if BYTE_ORDER == BIG_ENDIAN else 0


def high_ind(x: IntVar, part_type: IntType) -> int:
    """Implementation for `HIGH_IND`."""
    return 0 if BYTE_ORDER == BIG_ENDIAN else last_ind(x, part_type)


def offset_n(x: IntVar, n: int, t: IntType) -> IntVar:
    """Get the nth member of the data."""
    size = t.get_size()
    data = x.to_bytes(byteorder=BYTE_ORDER)
    return t.from_bytes(data[n * size: (n + 1) * size], byteorder=BYTE_ORDER)


def byte_n(x: IntVar, n: int) -> UInt8:
    """Implementation for `BYTEn`."""
    return offset_n(x, n, UInt8)


def word_n(x: IntVar, n: int) -> UInt16:
    """Implementation for `WORDn`."""
    return offset_n(x, n, UInt16)


def dword_n(x: IntVar, n: int) -> UInt32:
    """Implementation for `DWORDn`."""
    return offset_n(x, n, UInt32)


def low_byte(x: IntVar) -> UInt8:
    """Implementation for `LOBYTE`."""
    return byte_n(x, low_ind(x, UInt8))


def low_word(x: IntVar) -> UInt16:
    """Implementation for `LOWORD`."""
    return word_n(x, low_ind(x, UInt16))


def low_dword(x: IntVar) -> UInt32:
    """Implementation for `LODWORD`."""
    return dword_n(x, low_ind(x, UInt32))


def high_byte(x: IntVar) -> UInt8:
    """Implementation for `HIBYTE`."""
    return byte_n(x, high_ind(x, UInt8))


def high_word(x: IntVar) -> UInt16:
    """Implementation for `HIWORD`."""
    return word_n(x, high_ind(x, UInt16))


def high_dword(x: IntVar) -> UInt32:
    """Implementation for `HIDWORD`."""
    return dword_n(x, high_ind(x, UInt32))


def byte1(x: IntVar) -> UInt8:
    """Implementation for `BYTE1`."""
    return byte_n(x, 1)


def byte2(x: IntVar) -> UInt8:
    """Implementation for `BYTE2`."""
    return byte_n(x, 2)


def byte3(x: IntVar) -> UInt8:
    """Implementation for `BYTE3`."""
    return byte_n(x, 3)


def byte4(x: IntVar) -> UInt8:
    """Implementation for `BYTE4`."""
    return byte_n(x, 4)


def byte5(x: IntVar) -> UInt8:
    """Implementation for `BYTE5`."""
    return byte_n(x, 5)


def byte6(x: IntVar) -> UInt8:
    """Implementation for `BYTE6`."""
    return byte_n(x, 6)


def byte7(x: IntVar) -> UInt8:
    """Implementation for `BYTE7`."""
    return byte_n(x, 7)


def byte8(x: IntVar) -> UInt8:
    """Implementation for `BYTE8`."""
    return byte_n(x, 8)


def byte9(x: IntVar) -> UInt8:
    """Implementation for `BYTE9`."""
    return byte_n(x, 9)


def byte10(x: IntVar) -> UInt8:
    """Implementation for `BYTE10`."""
    return byte_n(x, 10)


def byte11(x: IntVar) -> UInt8:
    """Implementation for `BYTE11`."""
    return byte_n(x, 11)


def byte12(x: IntVar) -> UInt8:
    """Implementation for `BYTE12`."""
    return byte_n(x, 12)


def byte13(x: IntVar) -> UInt8:
    """Implementation for `BYTE13`."""
    return byte_n(x, 13)


def byte14(x: IntVar) -> UInt8:
    """Implementation for `BYTE14`."""
    return byte_n(x, 14)


def byte15(x: IntVar) -> UInt8:
    """Implementation for `BYTE15`."""
    return byte_n(x, 15)


def word1(x: IntVar) -> UInt8:
    """Implementation for `WORD1`."""
    return word_n(x, 1)


def word2(x: IntVar) -> UInt8:
    """Implementation for `WORD2`."""
    return word_n(x, 2)


def word3(x: IntVar) -> UInt8:
    """Implementation for `WORD3`."""
    return word_n(x, 3)


def word4(x: IntVar) -> UInt8:
    """Implementation for `WORD4`."""
    return word_n(x, 4)


def word5(x: IntVar) -> UInt8:
    """Implementation for `WORD5`."""
    return word_n(x, 5)


def word6(x: IntVar) -> UInt8:
    """Implementation for `WORD6`."""
    return word_n(x, 6)


def word7(x: IntVar) -> UInt8:
    """Implementation for `WORD7`."""
    return word_n(x, 7)


def signed_byte_n(x: IntVar, n: int) -> Int8:
    """Implementation for `SBYTEn`."""
    return offset_n(x, n, Int8)


def signed_word_n(x: IntVar, n: int) -> Int16:
    """Implementation for `SWORDn`."""
    return offset_n(x, n, Int16)


def signed_dword_n(x: IntVar, n: int) -> Int32:
    """Implementation for `SDWORDn`."""
    return offset_n(x, n, Int32)


def signed_low_byte(x: IntVar) -> Int8:
    """Implementation for `SLOBYTE`."""
    return signed_byte_n(x, low_ind(x, Int8))


def signed_low_word(x: IntVar) -> Int16:
    """Implementation for `SLOWORD`."""
    return signed_word_n(x, low_ind(x, Int16))


def signed_low_dword(x: IntVar) -> Int32:
    """Implementation for `SLODWORD`."""
    return signed_dword_n(x, low_ind(x, Int32))


def signed_high_byte(x: IntVar) -> Int8:
    """Implementation for `SHIBYTE`."""
    return signed_byte_n(x, high_ind(x, Int8))


def signed_high_word(x: IntVar) -> Int16:
    """Implementation for `SHIWORD`."""
    return signed_word_n(x, high_ind(x, Int16))


def signed_high_dword(x: IntVar) -> Int32:
    """Implementation for `SHIDWORD`."""
    return signed_dword_n(x, high_ind(x, Int32))


def signed_byte1(x: IntVar) -> Int8:
    """Implementation for `SBYTE1`."""
    return signed_byte_n(x, 1)


def signed_byte2(x: IntVar) -> Int8:
    """Implementation for `SBYTE2`."""
    return signed_byte_n(x, 2)


def signed_byte3(x: IntVar) -> Int8:
    """Implementation for `SBYTE3`."""
    return signed_byte_n(x, 3)


def signed_byte4(x: IntVar) -> Int8:
    """Implementation for `SBYTE4`."""
    return signed_byte_n(x, 4)


def signed_byte5(x: IntVar) -> Int8:
    """Implementation for `SBYTE5`."""
    return signed_byte_n(x, 5)


def signed_byte6(x: IntVar) -> Int8:
    """Implementation for `SBYTE6`."""
    return signed_byte_n(x, 6)


def signed_byte7(x: IntVar) -> Int8:
    """Implementation for `SBYTE7`."""
    return signed_byte_n(x, 7)


def signed_byte8(x: IntVar) -> Int8:
    """Implementation for `SBYTE8`."""
    return signed_byte_n(x, 8)


def signed_byte9(x: IntVar) -> Int8:
    """Implementation for `SBYTE9`."""
    return signed_byte_n(x, 9)


def signed_byte10(x: IntVar) -> Int8:
    """Implementation for `SBYTE10`."""
    return signed_byte_n(x, 10)


def signed_byte11(x: IntVar) -> Int8:
    """Implementation for `SBYTE11`."""
    return signed_byte_n(x, 11)


def signed_byte12(x: IntVar) -> Int8:
    """Implementation for `SBYTE12`."""
    return signed_byte_n(x, 12)


def signed_byte13(x: IntVar) -> Int8:
    """Implementation for `SBYTE13`."""
    return signed_byte_n(x, 13)


def signed_byte14(x: IntVar) -> Int8:
    """Implementation for `SBYTE14`."""
    return signed_byte_n(x, 14)


def signed_byte15(x: IntVar) -> Int8:
    """Implementation for `SBYTE15`."""
    return signed_byte_n(x, 15)


def signed_word1(x: IntVar) -> Int8:
    """Implementation for `SWORD1`."""
    return signed_word_n(x, 1)


def signed_word2(x: IntVar) -> Int8:
    """Implementation for `SWORD2`."""
    return signed_word_n(x, 2)


def signed_word3(x: IntVar) -> Int8:
    """Implementation for `SWORD3`."""
    return signed_word_n(x, 3)


def signed_word4(x: IntVar) -> Int8:
    """Implementation for `SWORD4`."""
    return signed_word_n(x, 4)


def signed_word5(x: IntVar) -> Int8:
    """Implementation for `SWORD5`."""
    return signed_word_n(x, 5)


def signed_word6(x: IntVar) -> Int8:
    """Implementation for `SWORD6`."""
    return signed_word_n(x, 6)


def signed_word7(x: IntVar) -> Int8:
    """Implementation for `SWORD7`."""
    return signed_word_n(x, 7)


def pair(high: IntVar, low: IntVar) -> IntVar:
    """Implementation for `__PAIR__`."""
    size = high.get_size()
    signed = high.get_signed()
    int_type = get_type(size=size * 2, signed=signed)
    return int_type(high) << size * 8 | type(high)(low)


def rol(value: IntVar, count: int) -> IntVar:
    """Implementation for `__ROL__`."""
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


def rol1(value: UInt8, count: int) -> UInt8:
    """Implementation for `__ROL1__`."""
    return rol(value, count)


def rol2(value: UInt16, count: int) -> UInt16:
    """Implementation for `__ROL2__`."""
    return rol(value, count)


def rol4(value: UInt32, count: int) -> UInt32:
    """Implementation for `__ROL4__`."""
    return rol(value, count)


def rol8(value: UInt64, count: int) -> UInt64:
    """Implementation for `__ROL8__`."""
    return rol(value, count)


def ror1(value: UInt8, count: int) -> UInt8:
    """Implementation for `__ROR1__`."""
    return rol(value, -count)


def ror2(value: UInt16, count: int) -> UInt16:
    """Implementation for `__ROR2__`."""
    return rol(value, -count)


def ror4(value: UInt32, count: int) -> UInt32:
    """Implementation for `__ROR4__`."""
    return rol(value, -count)


def ror8(value: UInt64, count: int) -> UInt64:
    """Implementation for `__ROR8__`."""
    return rol(value, -count)


def mkcshl(value: IntVar, count: int) -> Int8:
    """Implementation for `__MKCSHL__`."""
    nbits = value.get_size() * 8
    count %= nbits
    return (value >> (nbits - count)) & 1


def mkcshr(value: IntVar, count: int) -> Int8:
    """Implementation for `__MKCSHR__`."""
    return (value >> (count - 1)) & 1


def sets(x: IntVar) -> Int8:
    """Implementation for `__SETS__`."""
    data_type = get_type(size=x.get_size(), signed=True)
    return Int8(data_type(x) < 0)


def ofsub(x: IntVar, y: IntVar) -> IntVar:
    """Implementation for `__OFSUB__`."""
    if x.get_size() < y.get_size():
        x2 = x
        sx = sets(x2)
        return (sx ^ sets(y)) & (sx ^ sets(x2 - y))
    else:
        y2 = y
        sx = sets(x)
        return (sx ^ sets(y2)) & (sx ^ sets(x - y2))


def ofadd(x: IntVar, y: IntVar) -> IntVar:
    """Implementation for `__OFADD__`."""
    if x.get_size() < y.get_size():
        x2 = x
        sx = sets(x2)
        return ((1 ^ sx) ^ sets(y)) & (sx ^ sets(x2 + y))
    else:
        y2 = y
        sx = sets(x)
        return ((1 ^ sx) ^ sets(y2)) & (sx ^ sets(x + y2))


def cfsub(x: IntVar, y: IntVar) -> Int8:
    """Implementation for `__CFSUB__`."""
    size = max(x.get_size(), y.get_size())
    data_type = get_type(size=size, signed=False)
    return Int8(data_type(x) < data_type(y))


def cfadd(x: IntVar, y: IntVar) -> Int8:
    """Implementation for `__CFADD__`."""
    size = max(x.get_size(), y.get_size())
    data_type = get_type(size=size, signed=False)
    return Int8(data_type(x) > data_type(x + y))


# Refer to https://gcc.gnu.org/onlinedocs/gcc/Other-Builtins.html.


def swap_bytes(value: IntVar) -> IntVar:
    """Reverse bytes of the value with the order."""
    data = value.to_bytes(byteorder=BYTE_ORDER)
    return value.from_bytes(data[::-1], byteorder=BYTE_ORDER)


def bswap16(value: UInt16) -> UInt16:
    """Implementation for `bswap16`."""
    return swap_bytes(value)


def bswap32(value: UInt32) -> UInt32:
    """Implementation for `bswap32`."""
    return swap_bytes(value)


def bswap64(value: UInt64) -> UInt64:
    """Implementation for `bswap64`."""
    return swap_bytes(value)


def clz(x: IntVar) -> int:
    """Implementation for `__clz`."""
    return x.get_size() * 8 - len(bin(x)[2:])
