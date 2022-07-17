import pytest

from gravitum import uint32, Int8, UInt8
from gravitum.decompiler.ida import (offset_n, rol4, ror4, ofsub, ofadd, cfsub,
                                     cfadd, bswap32, clz)


@pytest.mark.parametrize('x,n,t,expected', [
    (uint32(0x53683477), 3, UInt8, 83),
    (uint32(0xffffffff), 3, Int8, -1),
])
def test_offset_n(x, n, t, expected):
    result = offset_n(x, n, t)

    assert result == expected


@pytest.mark.parametrize('value,count,expected', [
    (uint32(0x53683477), 2, 0x4da0d1dd),
    (uint32(0x4da0d1dd), 4, 0xda0d1dd4),
])
def test_rol(value, count, expected):
    result = rol4(value, count)

    assert result == expected


@pytest.mark.parametrize('value,count,expected', [
    (uint32(0x53683477), 2, 0xd4da0d1d),
    (uint32(0xd4da0d1d), 4, 0xdd4da0d1),
])
def test_ror(value, count, expected):
    result = ror4(value, count)

    assert result == expected


@pytest.mark.parametrize('x,y,expected', [
    (uint32(0x80000000), uint32(0), 0),
    (uint32(0x80000000), uint32(1), 1),
])
def test_ofsub(x, y, expected):
    result = ofsub(x, y)

    assert result == expected


@pytest.mark.parametrize('x,y,expected', [
    (uint32(0x7fffffff), uint32(0), 0),
    (uint32(0x7fffffff), uint32(1), 1),
])
def test_ofadd(x, y, expected):
    result = ofadd(x, y)

    assert result == expected


@pytest.mark.parametrize('x,y,expected', [
    (uint32(0x0), uint32(0), 0),
    (uint32(0x0), uint32(1), 1),
])
def test_cfsub(x, y, expected):
    result = cfsub(x, y)

    assert result == expected


@pytest.mark.parametrize('x,y,expected', [
    (uint32(0xffffffff), uint32(0), 0),
    (uint32(0xffffffff), uint32(1), 1),
])
def test_cfadd(x, y, expected):
    result = cfadd(x, y)

    assert result == expected


@pytest.mark.parametrize('value,expected', [
    (uint32(0x53683477), 0x77346853),
])
def test_bswap(value, expected):
    result = bswap32(value)

    assert result == expected


@pytest.mark.parametrize('x,expected', [
    (uint32(0x53), 25),
    (uint32(0x683477), 9),
])
def test_clz(x, expected):
    result = clz(x)

    assert result == expected
