from ..interfaces import Serializer


class Blob(Serializer[bytes]):
    "A set of arbitrary bytes, prefixed with it's length"

    _length_type: Serializer[int]

    def __init__(self, length_type: Serializer[int]) -> None:
        self._length_type = length_type

    def write(self, buf, value):
        self._length_type.write(buf, len(value))
        buf.write(value)

    def read(self, buf):
        length = self._length_type.read(buf)
        data = buf.read(length)
        return data
