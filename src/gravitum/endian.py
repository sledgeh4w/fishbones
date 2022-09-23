import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

BIG_ENDIAN: Literal["big"] = "big"
LITTLE_ENDIAN: Literal["little"] = "little"

# Default use little endian.
BYTE_ORDER: Literal["big", "little"] = LITTLE_ENDIAN


def set_endian(endian: Literal["little", "big"]):
    """Set global endian."""
    global BYTE_ORDER
    BYTE_ORDER = endian
