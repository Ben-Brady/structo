import typing as t
from ..core.ints import u32
from ..interfaces import Serializer, SerializerType
from ..serialise import get_serializer

class String(Serializer[str]):
    "A unicode string, prefixed with it's byte length"

    __slots__ = ("_length_type",)
    _length_type: Serializer[int]

    def __init__(self, length_type: SerializerType[int] | None = None) -> None:
        """_summary_

        Args:
            length_type (Serializer[int], optional): Defaults to uint32_LE
        """
        self._length_type = get_serializer(length_type or u32)

    def write(self, f, value):
        data = value.encode("utf-8")
        self._length_type.write(f, len(data))
        f.write(data)

    def read(self, f):
        length = self._length_type.read(f)
        data = f.read(length)
        if len(data) != length:
            raise ValueError(
                f"expected data with length {length}, "  # ------------
                f"received {len(data)}"
            )

        return data.decode("utf-8")
