from typing import Optional

from .integer import IntType

def get_type(
    size: Optional[int] = None,
    signed: Optional[bool] = None,
    type_name: Optional[str] = None,
) -> IntType: ...
