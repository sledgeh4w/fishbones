import re
from typing import Optional

from .types import (
    Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32, UInt64, IntType)


def get_type(
        size: Optional[int] = None,
        signed: Optional[bool] = None,
        type_name: Optional[str] = None
) -> IntType:
    """Get type int with specified size and signed."""
    if type_name is not None:
        match = re.match(r'(u*)int(\d+)', type_name)
        if not match:
            raise NotImplementedError()

        signed = not bool(match.group(1))
        size = int(match.group(2)) // 8

    if size == 1:
        return Int8 if signed else UInt8
    elif size == 2:
        return Int16 if signed else UInt16
    elif size == 4:
        return Int32 if signed else UInt32
    elif size == 8:
        return Int64 if signed else UInt64

    raise NotImplementedError()
