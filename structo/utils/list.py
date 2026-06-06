from ..core.ints import u32
from ..serialise import get_serializer
from ..interfaces import Serializer, SerializerType


class List[T](Serializer[list[T]]):
    "A list of items, prefixed with it's length"

    _length: Serializer[int]
    _value: Serializer[T]

    def __init__(
        self,
        value: SerializerType[T],
        length: SerializerType[int] = u32,
    ) -> None:
        self._length = get_serializer(length)
        self._value = get_serializer(value)

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
