import pytest

from gravitum import vptr, int8, int16, int32, int64, uint8, uint16, uint32, uint64


@pytest.mark.parametrize(
    "source_data,read_offset,read_type,expected",
    [
        (bytearray([71, 114, 97, 118, 105, 116, 117, 109]), 4, uint8, 105),
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


@pytest.mark.parametrize(
    "source_data,read_offset,read_size,expected",
    [
        (
            bytearray([71, 114, 97, 118, 105, 116, 117, 109]),
            4,
            4,
            bytes([105, 116, 117, 109]),
        ),
    ],
)
def test_read_bytes(source_data, read_offset, read_size, expected):
    p = vptr(source_data)
    result = p.add(read_offset).read_bytes(read_size)

    assert result == expected


@pytest.mark.parametrize(
    "source_data,write_offset,write_data,expected",
    [
        (
            bytearray([71, 114, 97, 118, 105, 116, 117, 109]),
            2,
            bytes([119, 52, 104, 83]),
            bytearray([71, 114, 119, 52, 104, 83, 117, 109]),
        ),
        (
            bytearray([71, 114, 97, 118, 105, 116, 117, 109]),
            2,
            bytearray([119, 52, 104, 83]),
            bytearray([71, 114, 119, 52, 104, 83, 117, 109]),
        ),
        (
            bytearray([71, 114, 97, 118, 105, 116, 117, 109]),
            2,
            [119, 52, 104, 83],
            bytearray([71, 114, 119, 52, 104, 83, 117, 109]),
        ),
    ],
)
def test_write_bytes(source_data, write_offset, write_data, expected):
    p = vptr(source_data)
    p.add(write_offset).write_bytes(write_data)

    assert source_data == expected


@pytest.mark.parametrize(
    "type_or_name",
    [
        int8,
        int16,
        int32,
        int64,
        uint8,
        uint16,
        uint32,
        uint64,
        "int8",
        "int16",
        "int32",
        "int64",
        "uint8",
        "uint16",
        "uint32",
        "uint64",
    ],
)
def test_cast(type_or_name):
    data = bytearray([])
    p = vptr(data)
    p.cast(type_or_name)
