import typing as t
from .ints import uint32_LE
from ..interfaces import Serializer


class String(Serializer[str]):
    "A unicode string, prefixed with it's byte length"

    _length_type: Serializer[int]

    def __init__(self, length_type: Serializer[int] | None = None) -> None:
        """_summary_

        Args:
            length_type (Serializer[int], optional): Defaults to uint32_LE
        """
        self._length_type = length_type or uint32_LE

    def write(self, f, value):
        data = value.encode("utf-8")
        self._length_type.write(f, len(data))
        f.write(data)

    def read(self, f):
        length = self._length_type.read(f)
        data = f.read(length)
        return data.decode("utf-8")
