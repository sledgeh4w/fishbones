import pytest

from fishbones import uint32
from fishbones.decompiler_builtins.ida import (
    byten,
    sbyten,
    rol4,
    ror4,
    ofsub,
    ofadd,
    cfsub,
    cfadd,
    bswap32,
    clz,
)


@pytest.mark.parametrize(
    "x,n,signed,expected",
    [
        (uint32(0x53683477), 3, False, 83),
        (uint32(0xFFFFFFFF), 3, True, -1),
    ],
)
def test_byte_n(x, n, signed, expected):
    result = (sbyten if signed else byten)(x, n)

    assert result == expected


@pytest.mark.parametrize(
    "value,count,expected",
    [
        (uint32(0x53683477), 2, 0x4DA0D1DD),
        (uint32(0x4DA0D1DD), 4, 0xDA0D1DD4),
    ],
)
def test_rol(value, count, expected):
    result = rol4(value, count)

    assert result == expected


@pytest.mark.parametrize(
    "value,count,expected",
    [
        (uint32(0x53683477), 2, 0xD4DA0D1D),
        (uint32(0xD4DA0D1D), 4, 0xDD4DA0D1),
    ],
)
def test_ror(value, count, expected):
    result = ror4(value, count)

    assert result == expected


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (uint32(0x80000000), uint32(0), 0),
        (uint32(0x80000000), uint32(1), 1),
    ],
)
def test_ofsub(x, y, expected):
    result = ofsub(x, y)

    assert result == expected


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (uint32(0x7FFFFFFF), uint32(0), 0),
        (uint32(0x7FFFFFFF), uint32(1), 1),
    ],
)
def test_ofadd(x, y, expected):
    result = ofadd(x, y)

    assert result == expected


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (uint32(0x0), uint32(0), 0),
        (uint32(0x0), uint32(1), 1),
    ],
)
def test_cfsub(x, y, expected):
    result = cfsub(x, y)

    assert result == expected


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (uint32(0xFFFFFFFF), uint32(0), 0),
        (uint32(0xFFFFFFFF), uint32(1), 1),
    ],
)
def test_cfadd(x, y, expected):
    result = cfadd(x, y)

    assert result == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (uint32(0x53683477), 0x77346853),
    ],
)
def test_bswap(value, expected):
    result = bswap32(value)

    assert result == expected


@pytest.mark.parametrize(
    "x,expected",
    [
        (uint32(0x53), 25),
        (uint32(0x683477), 9),
    ],
)
def test_clz(x, expected):
    result = clz(x)

    assert result == expected
