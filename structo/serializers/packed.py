from ..interfaces import Serializable, Serializer

import math
import typing as t
from dataclasses import dataclass
import annotationlib


class Bits:
    bits: int

    def __init__(self, bits: int) -> None:
        self.bits = bits


class PackedBitsMeta(type):
    def __new__(cls, name, bases, dct):
        new_class = t.cast(type, super().__new__(cls, name, bases, dct))
        if name == "PackedBits":  # TODO: Don't do this
            return new_class

        annotate = annotationlib.get_annotate_from_class_namespace(dct)
        assert annotate, f"Annotations not found for {name}"

        annotations = annotate(annotationlib.Format.VALUE_WITH_FAKE_GLOBALS)

        bits: dict[str, int] = {}
        for key, value in annotations.items():
            err_msg = f"expected Annotated[int, PackedInt(...)] on {name}.{key}"
            assert t.get_origin(value) is t.Annotated, err_msg

            ints = [arg for arg in t.get_args(value) if isinstance(arg, Bits)]
            assert len(ints) <= 1, err_msg
            assert len(ints) == 1, err_msg
            bits[key] = ints[0].bits

        obj = t.cast(PackedBits, dataclass(new_class))
        obj._bits = bits
        return obj


@t.dataclass_transform()
class PackedBits(Serializable, metaclass=PackedBitsMeta):
    _bits: dict[str, int]

    @classmethod
    def serializer(cls) -> Serializer[t.Self]:
        return PackedBitsSerializer(cls)


class PackedBitsSerializer[T: PackedBits](Serializer[T]):
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
        return math.ceil(sum(self._bits.values()) / 8)
