from ..interfaces import Serializer


class Literal(Serializer[bytes]):
    _values: list[bytes]
    _length: int

    def __init__(self, *values: bytes) -> None:
        assert len(values) > 0, "foo"
        length = len(values[0])

        for value in values:
            assert (
                len(value) == length
            ), f"All values in structo.Literal have to be the same length, expected {value} to be length {length}"

        self._length = length
        self._values = list(values)

    def write(self, f, value):
        assert value in self._values, f"{value} not in {b", ".join(self._values)}"
        f.write(value)

    def read(self, f):
        value = f.read(self._length)
        assert value in self._values, f"{value} not in {b", ".join(self._values)}"
        return value

    def sizeof(self):
        return self._length
