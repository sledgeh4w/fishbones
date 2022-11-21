from typing import List, SupportsInt, Union

from .exceptions import InvalidOperationError
from .integer import Integer, IntType, IntVar, uint8
from .utils import get_type


class VirtualPointer:
    """Provide pointer operation on bytearray.

    Args:
        source: The source ``bytearray`` to be read / write.
        data_type: The type of operated data. If it is ``str``, it will use
            ``utils.get_type`` to look up the type.
        offset: The distance from beginning to operating position.
    """

    def __init__(
        self,
        source: bytearray,
        data_type: Union[IntType, str] = uint8,
        offset: int = 0,
    ):
        self.source = source
        self.offset = offset
        self.data_type = data_type

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.sub(other)

    def __eq__(self, other):
        if not isinstance(other, VirtualPointer):
            return False

        return (
            self.source == other.source
            and self.offset == other.offset
            and self.data_type == other.data_type
        )

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, type_or_name: Union[IntType, str]):
        if isinstance(type_or_name, str):
            try:
                self._data_type = get_type(type_name=type_or_name)

            except ValueError as e:
                raise InvalidOperationError("Unsupported type") from e

        elif isinstance(type_or_name, type) and issubclass(type_or_name, Integer):
            self._data_type = type_or_name

        else:
            raise TypeError("Invalid type")

    def copy(self) -> "VirtualPointer":
        """Copy this object.

        The new object and the old object will operate on the same ``bytearray``.
        """
        return self.__class__(
            source=self.source,
            data_type=self.data_type,
            offset=self.offset,
        )

    def add(self, num: int) -> "VirtualPointer":
        """Offset this pointer position."""
        obj = self.copy()
        obj.offset += num * self.data_type.get_size()
        return obj

    def sub(self, num: int) -> "VirtualPointer":
        """Reverse offset this pointer position."""
        return self.add(-num)

    def cast(self, data_type: Union[IntType, str]) -> "VirtualPointer":
        """Cast to the specified type."""
        obj = self.copy()
        obj.data_type = data_type
        return obj

    def read_bytes(self, size: int) -> bytes:
        """Read bytes from source ``bytearray``."""
        if self.offset + size > len(self.source):
            raise InvalidOperationError("Read out of range")

        return bytes(self.source[self.offset : self.offset + size])

    def write_bytes(self, data: Union[bytes, bytearray, List[SupportsInt]]):
        """Write bytes into source ``bytearray``."""
        try:
            for i, v in enumerate(data):
                self.source[self.offset + i] = int(v)

        except IndexError as e:
            raise InvalidOperationError("Write out of range") from e

    def read(self) -> IntVar:
        """Read an integer from source ``bytearray``."""
        data = self.read_bytes(self.data_type.get_size())
        return self.data_type.from_bytes(data)

    def write(self, value: SupportsInt):
        """Write an integer into source ``bytearray``."""
        data = self.data_type(value).to_bytes()
        self.write_bytes(data)


def vptr(source: bytearray, data_type: Union[IntType, str] = uint8) -> VirtualPointer:
    """Shorthand of `VirtualPointer(source, data_type)`."""
    return VirtualPointer(source=source, data_type=data_type)
