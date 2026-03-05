from ..serializer import Serializer


class List[T](Serializer[list[T]]):
    "A list of items, prefixed with it's length"

    value_type: Serializer[T]
    length_type: Serializer[int]

    def __init__(self, length_type: Serializer[int], value_type: Serializer[T]) -> None:
        self.length_type = length_type
        self.value_type = value_type

    def write(self, buf, value):
        length = len(value)
        self.length_type.write(buf, length)
        for item in value:
            self.value_type.write(buf, item)

    def read(self, buf):
        length = self.length_type.read(buf)
        values = []
        for _ in range(length):
            value = self.value_type.read(buf)
            values.append(value)

        return values
