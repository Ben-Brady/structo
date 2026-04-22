import typing as t
from ..interfaces import Serializer


class Buffer(Serializer[bytes]):
    _length: int

    def __init__(self, length: int) -> None:
        self._length = length

    def write(self, f: t.IO[bytes], value: bytes):
        assert (
            len(value) == self._length
        ), f"expected data with length {self._length}, received {len
                                                                 (value)}"
        f.write(value)

    def read(self, f: t.IO[bytes]) -> bytes:
        data = f.read(self._length)
        return data

    def sizeof(self) -> int:
        return self._length
