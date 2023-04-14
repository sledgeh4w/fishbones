import operator

import pytest

from fishbones import int8, uint8, uint32
from fishbones.integer import UInt8, UInt32


@pytest.mark.parametrize(
    "x,op,expected",
    [
        (1, operator.neg, -1),
        (-1, operator.pos, -1),
        (-1, operator.abs, 1),
        (1, operator.invert, -2),
    ],
)
def test_unary_operation(x, op, expected):
    result = op(int8(x))

    assert result == expected


@pytest.mark.parametrize(
    "x,y,op,expected",
    [
        (1, 1, operator.add, 2),
        (2, 1, operator.sub, 1),
        (2, 2, operator.mul, 4),
        (4, 2, operator.truediv, 2),
        (4, 2, operator.floordiv, 2),
        (3, 2, operator.mod, 1),
        (1, 2, operator.and_, 0),
        (1, 2, operator.or_, 3),
        (1, 2, operator.xor, 3),
        (1, 1, operator.lshift, 2),
        (1, 1, operator.rshift, 0),
    ],
)
def test_binary_operation(x, y, op, expected):
    results = [op(int8(x), int8(y)), op(int8(x), y), op(x, int8(y))]

    assert all([result == expected for result in results])


@pytest.mark.parametrize(
    "x,y,op,expected",
    [
        (1, 0, operator.gt, True),
        (1, 1, operator.gt, False),
        (1, 1, operator.ge, True),
        (0, 1, operator.ge, False),
        (1, 1, operator.eq, True),
        (1, 0, operator.eq, False),
        (1, 1, operator.le, True),
        (1, 0, operator.le, False),
        (0, 1, operator.lt, True),
        (1, 1, operator.lt, False),
        (1, 0, operator.ne, True),
        (1, 1, operator.ne, False),
    ],
)
def test_comparison(x, y, op, expected):
    results = [op(int8(x), int8(y)), op(int8(x), y), op(x, int8(y))]

    assert all([result == expected for result in results])


@pytest.mark.parametrize(
    "x,y,op,expected",
    [
        (int8(1), 1.1, operator.gt, False),
        (int8(1), 0.9, operator.gt, True),
        (1.1, int8(1), operator.gt, True),
        (0.9, int8(1), operator.gt, False),
        (int8(1), 1.1, operator.eq, False),
        (int8(1), 1.1, operator.ne, True),
    ],
)
def test_comparison_with_float(x, y, op, expected):
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
