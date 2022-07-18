import pytest

from gravitum import uint16, uint32, uint64
from gravitum.decompiler.ghidra import sub42, zext24, sext48


@pytest.mark.parametrize(
    "x,c,expected",
    [
        (uint32(0xAABBCCDD), 1, uint16(0xBBCC)),
    ],
)
def test_sub(x, c, expected):
    result = sub42(x, c)

    assert result == expected


@pytest.mark.parametrize(
    "x,expected",
    [
        (uint16(0xAABB), uint32(0x0000AABB)),
    ],
)
def test_zext(x, expected):
    result = zext24(x)

    assert result == expected


@pytest.mark.parametrize(
    "x,expected",
    [
        (uint32(0xAABBCCDD), uint64(0xFFFFFFFFAABBCCDD)),
    ],
)
def test_sext(x, expected):
    result = sext48(x)

    assert result == expected
