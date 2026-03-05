from ..serializer import Serializer


class Literal(Serializer[bytes]):
    values: list[bytes]
    _length: int

    def __init__(self, *values: bytes) -> None:
        assert len(values) > 0, "foo"
        length = len(values[0])

        for value in values:
            assert (
                len(value) == length
            ), f"All values in structo.Literal have to be the same length, expected {value} to be length {length}"

        self._length = length
        self.values = list(values)

    def write(self, buf, value):
        assert value in self.values, f"{value} not in {b", ".join(self.values)}"
        buf.write(self.values)

    def read(self, buf):
        value = buf.read(self._length)
        assert value in self.values, f"{value} not in {b", ".join(self.values)}"
        return value

    def sizeof(self):
        return self._length
