from .exceptions import InvalidOperationError
from .integer import IntBase, uint8
from .utils import get_type


class VirtualPointer:
    """Provide pointer operation on bytearray.

    Args:
        source: The source ``bytearray`` to be read / write.
        data_type: The type of operated data. If it is ``str``, it will use
            ``utils.get_type`` to look up the type.
        byteorder: The byteorder of operated data.
        offset: The distance from beginning to operating position.
    """

    def __init__(self, source, data_type=uint8, byteorder="little", offset=0):
        self.source = source
        self.byteorder = byteorder
        self.offset = offset
        self.data_type = data_type

    def __add__(self, other):
        """Support addition."""
        return self.add(other)

    def __sub__(self, other):
        """Support subtraction."""
        return self.sub(other)

    @property
    def data_type(self):
        """Get data type."""
        return self._data_type

    @data_type.setter
    def data_type(self, type_or_name):
        """Set data type."""
        if isinstance(type_or_name, str):
            try:
                self._data_type = get_type(type_name=type_or_name)

            except ValueError as e:
                raise InvalidOperationError("Unsupported type") from e

        elif isinstance(type_or_name, type) and issubclass(type_or_name, IntBase):
            self._data_type = type_or_name

        else:
            raise TypeError("Invalid type")

    def copy(self):
        """Copy this object.

        The new object and the old object will operate on the same ``bytearray``.
        """
        return self.__class__(
            source=self.source,
            data_type=self.data_type,
            byteorder=self.byteorder,
            offset=self.offset,
        )

    def add(self, num):
        """Offset this pointer position."""
        obj = self.copy()
        obj.offset += num * self.data_type.get_size()
        return obj

    def sub(self, num):
        """Reverse offset this pointer position."""
        return self.add(-num)

    def cast(self, data_type):
        """Cast to the specified type."""
        obj = self.copy()
        obj.data_type = data_type
        return obj

    def read_bytes(self, size):
        """Read bytes from source ``bytearray``."""
        if self.offset + size > len(self.source):
            raise InvalidOperationError("Read out of range")

        return bytes(self.source[self.offset : self.offset + size])

    def write_bytes(self, data):
        """Write bytes into source ``bytearray``."""
        try:
            for i, v in enumerate(data):
                self.source[self.offset + i] = int(v)

        except IndexError as e:
            raise InvalidOperationError("Write out of range") from e

    def read(self):
        """Read an integer from source ``bytearray``."""
        data = self.read_bytes(self.data_type.get_size())
        return self.data_type.from_bytes(data, byteorder=self.byteorder)

    def write(self, value):
        """Write an integer into source ``bytearray``."""
        data = self.data_type(value).to_bytes(byteorder=self.byteorder)
        self.write_bytes(data)


def vptr(source, data_type=uint8, byteorder="little"):
    """Shorthand of `VirtualPointer(source, data_type, byteorder)`."""
    return VirtualPointer(source=source, data_type=data_type, byteorder=byteorder)
