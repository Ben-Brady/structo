from io import Reader, Writer
from math import ceil

from structo import Serializer
from ..packed import PackedInts, PackedInt
import typing as t


class PackedIntSerializer[T: PackedInts](Serializer[T]):
    size: int
    _bits: dict[str, int]
    _cls: type[type[T]]

    def __init__(self, cls: type[T]) -> None:
        total_bits = sum(x.bits for x in cls._bits.values())
        self._cls = cls
        self.size = ceil(total_bits / 8)

        self._bits = {}
        for key, value in cls._bits.items():
            self._bits[key] = value.bits

    def write(self, buf: Writer, value: T):
        output = 0
        offset = 0
        for field_key, bits in self._bits.items():
            field_value = getattr(value, field_key)

            max_value = (2**bits) - 1
            assert field_value <= max_value, f"{self._cls.__name__}{field_key} exceed max value, {field_value} > {max_value}"
            output += field_value << offset
            offset += bits

        data = bytearray(self.size)
        for x in range(self.size):
            byte = output & 255
            output >>= 8
            data[x] = byte

        buf.write(data)

    def read(self, buf: Reader) -> T:
        data = buf.read(self.size)
        integer = int.from_bytes(data, "little")
        attrs: dict[str, t.Any] = {}

        offset = 0
        for field_key, bits in self._bits.items():

            mask = (2**bits) - 1
            value = (integer >> offset) & mask

            offset += bits
            attrs[field_key] = value

        return self._cls(**attrs)

    def sizeof(self) -> int:
        return self.size
