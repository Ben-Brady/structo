from ..serializer import Serializer


class Array[T](Serializer[list[T]]):
    length: int
    type: Serializer[T]

    def __init__(self, length: int, type: Serializer[T]) -> None:
        assert length > 0, "Array must be longer than 0"
        self.length = length
        self.type = type

    def write(self, buf, value):
        assert (
            len(value) == self.length
        ), f"expected array with {self.length} length, receieved {len(value)}"

        for item in value:
            self.type.write(buf, item)

    def read(self, buf):
        items = []
        for _ in range(self.length):
            items.append(self.type.read(buf))

        return items

    def sizeof(self):
        element_length = self.type.sizeof()
        if element_length is None:
            return None
        else:
            return element_length * self.length

