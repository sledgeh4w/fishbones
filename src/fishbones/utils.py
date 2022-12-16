import re
from typing import Optional, Type, TypeVar

from .integer import Int8, Int16, Int32, Int64, Integer, UInt8, UInt16, UInt32, UInt64

_T = TypeVar("_T", Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32, UInt64)


def get_type(
    size: Optional[int] = None,
    signed: Optional[bool] = None,
    type_name: Optional[str] = None,
) -> Type[Integer]:
    """Get type int with specified size and signed.

    Args:
        size: The size of the type.
        signed: Is the type signed.
        type_name: The lowercase name of type to find. If it is None,
            ``size`` and ``signed`` must be given.

    Raises:
        ValueError: If no matched type.
    """
    int_types = [Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32, UInt64]

    if type_name is not None:
        match = re.match(r"(u*)int(\d+)", type_name)

        if match:
            nbits = int(match.group(2))
            if nbits % 8 == 0:
                signed = not bool(match.group(1))
                size = nbits // 8

    if size is not None and signed is not None:
        for int_type in int_types:
            if int_type.get_size() == size and int_type.get_signed() == signed:
                return int_type

    raise ValueError("No matched type")


def truncate(x: Integer, c: int, to_type: Type[_T]) -> _T:
    """Truncate data."""
    data = x.to_bytes()
    to_size = to_type.get_size()
    return to_type.from_bytes(data[c : c + to_size])


def zero_extend(x: Integer, to_type: Type[_T]) -> _T:
    """Zero extend."""
    return to_type.from_bytes(x.to_bytes())


def sign_extend(x: Integer, to_type: Type[_T]) -> _T:
    """Sign extend."""
    t1 = get_type(size=x.get_size(), signed=True)
    t2 = get_type(size=to_type.get_size(), signed=True)
    return to_type.from_bytes(t2.from_bytes(t1(x).to_bytes()).to_bytes())
