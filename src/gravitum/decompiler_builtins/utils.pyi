from typing import Type, TypeVar

from ..integer import IntVar, int8, int16, int32, int64, uint8, uint16, uint32, uint64

_T = TypeVar("_T", int8, int16, int32, int64, uint8, uint16, uint32, uint64)

def truncate(x: IntVar, c: int, to_type: Type[_T]) -> _T: ...
def zero_extend(x: IntVar, to_type: Type[_T]) -> _T: ...
def sign_extend(x: IntVar, to_type: Type[_T]) -> _T: ...