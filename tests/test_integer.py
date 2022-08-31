from operator import (
    neg,
    pos,
    abs,
    invert,
    add,
    sub,
    mul,
    truediv,
    floordiv,
    mod,
    and_,
    or_,
    xor,
    lshift,
    rshift,
)

import pytest

from gravitum import int8, uint8, uint32


@pytest.mark.parametrize(
    "x,op,expected",
    [
        (int8(1), neg, -1),
        (int8(-1), pos, -1),
        (int8(-1), abs, 1),
        (int8(1), invert, -2),
    ],
)
def test_unary_operation(x, op, expected):
    result = op(x)

    assert result == expected


@pytest.mark.parametrize(
    "x,y,op,expected",
    [
        (int8(1), int8(1), add, 2),
        (int8(2), int8(1), sub, 1),
        (int8(2), int8(2), mul, 4),
        (int8(4), int8(2), truediv, 2),
        (int8(4), int8(2), floordiv, 2),
        (int8(3), int8(2), mod, 1),
        (int8(1), int8(2), and_, 0),
        (int8(1), int8(2), or_, 3),
        (int8(1), int8(2), xor, 3),
        (int8(1), int8(1), lshift, 2),
        (int8(1), int8(1), rshift, 0),
    ],
)
def test_binary_operation(x, y, op, expected):
    result = op(x, y)

    assert result == expected


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (int8(1), uint8(1), uint8),
        (uint8(1), 1, uint8),
        (uint8(1), uint32(1), uint32),
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
