import re
from typing import Optional, List, Type

import numpy as np

from .types import (IntType, IntBase, Int8, Int16, Int32, Int64, UInt8, UInt16,
                    UInt32, UInt64)


def get_type(size: Optional[int] = None,
             signed: Optional[bool] = None,
             type_name: Optional[str] = None) -> IntType:
    """Get type int with specified size and signed."""
    if type_name is not None:
        match = re.match(r'(u*)int(\d+)', type_name)
        if not match:
            raise NotImplementedError()

        nbits = int(match.group(2))
        if nbits % 8:
            raise NotImplementedError()

        signed = not bool(match.group(1))
        size = nbits // 8

    int_types: List[Type[IntBase]] = [
        Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32, UInt64
    ]

    for int_type in int_types:
        if int_type.get_size() == size and int_type.get_signed() == signed:
            return int_type

    raise NotImplementedError()


def disable_numpy_overflow_warnings():
    """Disable overflow warnings of numpy."""
    np.seterr(over='ignore')
