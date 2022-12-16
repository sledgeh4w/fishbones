import operator

import pytest

from fishbones import int8, uint8, uint32
from fishbones.integer import UInt8, UInt32


@pytest.mark.parametrize(
    "x,op,expected",
    [
        (int8(1), operator.neg, -1),
        (int8(-1), operator.pos, -1),
        (int8(-1), operator.abs, 1),
        (int8(1), operator.invert, -2),
    ],
)
def test_unary_operation(x, op, expected):
    result = op(x)

    assert result == expected


@pytest.mark.parametrize(
    "x,y,op,expected",
    [
        (int8(1), int8(1), operator.add, 2),
        (int8(2), int8(1), operator.sub, 1),
        (int8(2), int8(2), operator.mul, 4),
        (int8(4), int8(2), operator.truediv, 2),
        (int8(4), int8(2), operator.floordiv, 2),
        (int8(3), int8(2), operator.mod, 1),
        (int8(1), int8(2), operator.and_, 0),
        (int8(1), int8(2), operator.or_, 3),
        (int8(1), int8(2), operator.xor, 3),
        (int8(1), int8(1), operator.lshift, 2),
        (int8(1), int8(1), operator.rshift, 0),
    ],
)
def test_binary_operation(x, y, op, expected):
    result = op(x, y)

    assert result == expected


@pytest.mark.parametrize(
    "x,y,op,expected",
    [
        (int8(1), int8(0), operator.gt, True),
        (int8(1), int8(1), operator.gt, False),
        (int8(1), int8(1), operator.ge, True),
        (int8(0), int8(1), operator.ge, False),
        (int8(1), int8(1), operator.eq, True),
        (int8(1), int8(0), operator.eq, False),
        (int8(1), int8(1), operator.le, True),
        (int8(1), int8(0), operator.le, False),
        (int8(0), int8(1), operator.lt, True),
        (int8(1), int8(1), operator.lt, False),
        (int8(1), int8(0), operator.ne, True),
        (int8(1), int8(1), operator.ne, False),
    ],
)
def test_comparison(x, y, op, expected):
    result = op(x, y)

    assert result == expected


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (int8(1), uint8(1), UInt8),
        (uint8(1), 1, UInt8),
        (uint8(1), uint32(1), UInt32),
    ],
)
def test_type_conversion(x, y, expected):
    result = x + y

    assert type(result) == expected


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (uint32(0x53683477), uint32(0x53683477), 0xD5708F51),
    ],
)
def test_overflow(x, y, expected):
    result = x * y

    assert result == expected
