from ..core.ints import uint32_LE
from ..interfaces import Serializer


class Blob(Serializer[bytes]):
    "A set of arbitrary bytes, prefixed with it's length"

    _length: Serializer[int]

    def __init__(self, length: Serializer[int] | None = None) -> None:
        self._length = length or uint32_LE

    def write(self, f, value):
        self._length.write(f, len(value))
        f.write(value)

    def read(self, f):
        length = self._length.read(f)
        data = f.read(length)

        if len(data) != length:
            raise ValueError(
                f"expected data with length {length}, "  # ------------
                f"received {len(data)}"
            )

        return data
