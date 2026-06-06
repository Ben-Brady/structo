from ..serialise import get_serializer
from ..interfaces import Serializer, SerializerType


class Array[T](Serializer[list[T]]):
    _length: int
    _value_type: Serializer[T]

    def __init__(self, value: SerializerType[T], length: int) -> None:
        self._length = length
        self._value_type = get_serializer(value)
        assert length > 0, "Array must be longer than 0"

    def write(self, f, value):
        assert (
            len(value) == self._length
        ), f"expected array with {self._length} length, receieved {len(value)}"

        for item in value:
            self._value_type.write(f, item)

    def read(self, f):
        items = []
        for _ in range(self._length):
            items.append(self._value_type.read(f))

        return items

    def sizeof(self):
        element_length = self._value_type.sizeof()
        if element_length is None:
            return None
        else:
            return element_length * self._length
