import re
from typing import List, Optional, Type

from .types import (
    integer,
    int8,
    int16,
    int32,
    int64,
    uint8,
    uint16,
    uint32,
    uint64,
)


def get_type(
    size: Optional[int] = None,
    signed: Optional[bool] = None,
    type_name: Optional[str] = None,
) -> Type[integer]:
    """Get type int with specified size and signed.

    Args:
        size: The size of the type.
        signed: The signed of the type.
        type_name: The lowercase name of type to find.
            If it is None, ``size`` and ``signed`` must be given.
    """
    if type_name is not None:
        match = re.match(r"(u*)int(\d+)", type_name)
        if not match:
            raise ValueError("Match type failed")

        nbits = int(match.group(2))
        if nbits % 8:
            raise ValueError("Match type failed")

        signed = not bool(match.group(1))
        size = nbits // 8

    int_types: List[Type[integer]] = [
        int8,
        int16,
        int32,
        int64,
        uint8,
        uint16,
        uint32,
        uint64,
    ]

    for int_type in int_types:
        if int_type.get_size() == size and int_type.get_signed() == signed:
            return int_type

    raise ValueError("Match type failed")
