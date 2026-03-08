from ..serialise import to_serializer
from ..interfaces import Serializer


class Array[T](Serializer[list[T]]):
    _length: int
    _value_type: Serializer[T]

    def __init__(self, length: int, value_type: Serializer[T] | type[T]) -> None:
        assert length > 0, "Array must be longer than 0"
        self._length = length
        self._value_type = to_serializer(value_type)

    def write(self, buf, value):
        assert (
            len(value) == self._length
        ), f"expected array with {self._length} length, receieved {len(value)}"

        for item in value:
            self._value_type.write(buf, item)

    def read(self, buf):
        items = []
        for _ in range(self._length):
            items.append(self._value_type.read(buf))

        return items

    def sizeof(self):
        element_length = self._value_type.sizeof()
        if element_length is None:
            return None
        else:
            return element_length * self._length
