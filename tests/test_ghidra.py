import pytest

from gravitum import uint16, uint32, uint64
from gravitum.utils import disable_numpy_overflow_warnings
from gravitum.platform.ghidra import sub42, zext24, sext48

disable_numpy_overflow_warnings()


@pytest.mark.parametrize('x,c,expected', [
    (uint32(0xaabbccdd), 1, uint16(0xbbcc)),
])
def test_sub(x, c, expected):
    result = sub42(x, c)

    assert result == expected


@pytest.mark.parametrize('x,expected', [
    (uint16(0xaabb), uint32(0x0000aabb)),
])
def test_zext(x, expected):
    result = zext24(x)

    assert result == expected


@pytest.mark.parametrize('x,expected', [
    (uint32(0xaabbccdd), uint64(0xffffffffaabbccdd)),
])
def test_sext(x, expected):
    result = sext48(x)

    assert result == expected
