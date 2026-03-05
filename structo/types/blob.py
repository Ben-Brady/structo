from ..serializer import Serializer


class Blob(Serializer[bytes]):
    "A set of arbitrary bytes, prefixed with it's length"

    length_type: Serializer[int]

    def __init__(self, length_type: Serializer[int]) -> None:
        self.length_type = length_type

    def write(self, buf, value):
        self.length_type.write(buf, len(value))
        buf.write(value)

    def read(self, buf):
        length = self.length_type.read(buf)
        data = buf.read(length)
        return data
