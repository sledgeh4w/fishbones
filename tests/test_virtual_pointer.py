import pytest

from gravitum import vptr, uint32, UInt8


@pytest.mark.parametrize(
    "source_data,read_offset,read_type,expected",
    [
        (bytearray([71, 114, 97, 118, 105, 116, 117, 109]), 4, UInt8, 105),
    ],
)
def test_read(source_data, read_offset, read_type, expected):
    p = vptr(source_data)
    result = p.add(read_offset).cast(read_type).read()

    assert result == expected


@pytest.mark.parametrize(
    "source_data,write_offset,write_value,expected",
    [
        (
            bytearray([71, 114, 97, 118, 105, 116, 117, 109]),
            2,
            uint32(0x53683477),
            bytearray([71, 114, 119, 52, 104, 83, 117, 109]),
        ),
    ],
)
def test_write(source_data, write_offset, write_value, expected):
    p = vptr(source_data)
    p.add(write_offset).cast(type(write_value)).write(write_value)

    assert source_data == expected
