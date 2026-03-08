from .numbers import uint32_LE
from ..serialise import to_serializer
from ..interfaces import Serializer


class List[T](Serializer[list[T]]):
    "A list of items, prefixed with it's length"

    _length_type: Serializer[int]
    _value_type: Serializer

    def __init__(self, value: Serializer[T] | type[T], length: Serializer[int] | None = None) -> None:
        self._length_type = length or uint32_LE
        self._value_type = to_serializer(value)

    def write(self, buf, value):
        length = len(value)
        self._length_type.write(buf, length)
        for item in value:
            self._value_type.write(buf, item)

    def read(self, buf):
        length = self._length_type.read(buf)
        values = []
        for _ in range(length):
            value = self._value_type.read(buf)
            values.append(value)

        return values
