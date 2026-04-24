from ..core.ints import uint32_LE
from ..serialise import to_serializer
from ..interfaces import Serializer


class List[T](Serializer[list[T]]):
    "A list of items, prefixed with it's length"

    _length: Serializer[int]
    _value: Serializer

    def __init__(self, value: Serializer[T] | type[T], length: Serializer[int] = uint32_LE) -> None:
        self._length = length
        self._value = to_serializer(value)

    def write(self, f, value):
        length = len(value)
        self._length.write(f, length)
        for item in value:
            self._value.write(f, item)

    def read(self, f):
        length = self._length.read(f)
        values = []
        for _ in range(length):
            value = self._value.read(f)
            values.append(value)

        return values
