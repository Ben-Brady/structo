import typing as t
from ..serializer import Serializer


class String(Serializer[str]):
    "A unicode string, prefixed with it's byte length"

    length_type: Serializer[int]

    def __init__(self, length_type: Serializer[int]) -> None:
        self.length_type = length_type

    def write(self, buf, value):
        data = value.encode("utf-8")
        self.length_type.write(buf, len(data))
        buf.write(data)

    def read(self, buf):
        length = self.length_type.read(buf)
        data = buf.read(length)
        return data.decode("utf-8")
