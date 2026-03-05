from ..serializer import Serializer


class Buffer(Serializer[bytes]):
    length: int

    def __init__(self, length: int) -> None:
        self.length = length

    def write(self, buf, value):
        assert (
            len(value) == self.length
        ), f"expected data with length {self.length}, received {len(value)}"
        buf.write(value)

    def read(self, buf):
        data = buf.read(self.length)
        return data

    def sizeof(self):
        return self.length
