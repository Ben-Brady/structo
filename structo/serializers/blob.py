from .numbers import uint32_LE
from ..interfaces import Serializer


class Blob(Serializer[bytes]):
    "A set of arbitrary bytes, prefixed with it's length"

    _length_type: Serializer[int]

    def __init__(self, length_type: Serializer[int] | None = None) -> None:
        self._length_type = length_type or uint32_LE

    def write(self, f, value):
        self._length_type.write(f, len(value))
        f.write(value)

    def read(self, f):
        length = self._length_type.read(f)
        data = f.read(length)
        return data
