from typing import List, SupportsInt, Union, NoReturn

from .exceptions import InvalidOperationError
from .types import UInt8, IntType, IntVar
from .utils import get_type


class VirtualPointer:
    """Provide virtual pointer operation on bytearray."""

    def __init__(self,
                 source: bytearray,
                 data_type: Union[IntType, str],
                 byteorder: str = 'little',
                 offset: int = 0):
        self.source = source
        self.data_type = None
        self.byteorder = byteorder
        self.offset = offset

        self.set_type(data_type)

    def __add__(self, other):
        """Support addition."""
        return self.add(int(other))

    def __sub__(self, other):
        """Support subtraction."""
        return self.sub(int(other))

    def copy(self) -> "VirtualPointer":
        """Copy this object."""
        return self.__class__(source=self.source,
                              data_type=self.data_type,
                              byteorder=self.byteorder,
                              offset=self.offset)

    def set_type(self, data_type: Union[IntType, str]) -> NoReturn:
        """Set data type."""
        if isinstance(data_type, str):
            try:
                self.data_type = get_type(type_name=data_type)
            except NotImplementedError as e:
                raise InvalidOperationError('Unsupported type') from e
        else:
            self.data_type = data_type

    def add(self, num: int) -> "VirtualPointer":
        """Offset this pointer position."""
        obj = self.copy()
        obj.offset += num * self.data_type.get_size()
        return obj

    def sub(self, num: int) -> "VirtualPointer":
        """Reverse offset this pointer position."""
        obj = self.copy()
        obj.offset -= num * self.data_type.get_size()
        return obj

    def cast(self, data_type: Union[IntType, str]) -> "VirtualPointer":
        """Cast to the specified type."""
        obj = self.copy()
        obj.set_type(data_type)
        return obj

    def read_bytes(self, size: int) -> bytes:
        """Read bytes from the source bytearray."""
        if self.offset + size > len(self.source):
            raise InvalidOperationError('Read out of range')
        return bytes(self.source[self.offset:self.offset + size])

    def write_bytes(
            self, data: Union[bytes, bytearray, List[SupportsInt]]) -> NoReturn:
        """Write bytes into the source bytearray."""
        try:
            for i, v in enumerate(data):
                self.source[self.offset + i] = v
        except IndexError as e:
            raise InvalidOperationError('Write out of range') from e

    def read(self) -> IntVar:
        """Read an integer from the source bytearray."""
        data = self.read_bytes(self.data_type.get_size())
        return self.data_type.from_bytes(data, byteorder=self.byteorder)

    def write(self, value: SupportsInt) -> NoReturn:
        """Write an integer into the source bytearray."""
        data = self.data_type(value).to_bytes(byteorder=self.byteorder)
        self.write_bytes(data)


def vptr(source: bytearray,
         data_type: Union[IntType, str] = UInt8) -> VirtualPointer:
    """Short-hand for `VirtualPointer(source, data_type)`."""
    return VirtualPointer(source=source, data_type=data_type)
