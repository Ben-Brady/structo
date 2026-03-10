from math import ceil

from ..objects import PackedInts
from ..interfaces import Serializer

import typing as t


class PackedIntSerializer[T: PackedInts](Serializer[T]):
    _size: int
    _bits: dict[str, int]
    _cls: type[type[T]]

    def __init__(self, cls: type[T]) -> None:
        self._cls = cls
        self._bits = cls._bits
        self._size = self.sizeof()

    def write(self, f, value):
        output = 0
        offset = 0
        for field_key, bits in self._bits.items():
            field_value = getattr(value, field_key)

            max_value = (2**bits) - 1

            assert field_value >= 0, "Cannot serialize negative values"
            assert (
                field_value <= max_value
            ), f"{self._cls.__name__}{field_key} exceed max value, {field_value} > {max_value}"
            output += field_value << offset
            offset += bits

        data = bytearray(self._size)
        for x in range(self._size):
            byte = output & 255
            output >>= 8
            data[x] = byte

        f.write(data)

    def read(self, f):
        data = f.read(self._size)
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
        return ceil(sum(self._bits.values()) / 8)
