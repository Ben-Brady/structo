from .serializer import Serializable, Serializer
import typing as t
import io
from typing import Annotated
from dataclasses import dataclass
import annotationlib


class PackedInt:
    bits: int

    def __init__(self, *, bits: int) -> None:
        self.bits = bits


class PackedIntsMeta(type):
    def __new__(cls, name, bases, dct):
        new_class = t.cast(type, super().__new__(cls, name, bases, dct))
        if name == "PackedInts":
            return new_class

        annotate = annotationlib.get_annotate_from_class_namespace(dct)
        assert annotate

        bits: dict[str, PackedInt] = {}
        attrs = annotate(annotationlib.Format.VALUE_WITH_FAKE_GLOBALS)
        for key, value in attrs.items():
            assert t.get_origin(value) is t.Annotated

            ints = [arg for arg in t.get_args(value) if isinstance(arg, PackedInt)]
            assert len(ints) == 1
            bits[key] = ints[0]

        obj = t.cast(PackedInts, dataclass(new_class))
        obj._bits = bits
        return obj


# This is very messed up since we
@t.dataclass_transform()
class PackedInts(Serializable, metaclass=PackedIntsMeta):
    _bits: dict[str, PackedInt]

    @classmethod
    def serializer(cls) -> Serializer[t.Self]:
        from .types import PackedIntSerializer

        return PackedIntSerializer(cls)

    @classmethod
    def sizeof(cls) -> int | None:
        return cls.serializer().sizeof()

    def write(self, buf: io.Writer):
        return self.serializer().write(buf, self)

    @classmethod
    def read(cls, buf: io.Reader) -> t.Self:
        return cls.serializer().read(buf)

    def to_bytes(self) -> bytes:
        return self.serializer().to_bytes(self)

    @classmethod
    def from_bytes(cls, data: bytes) -> t.Self:
        return cls.serializer().from_bytes(data)


class Foo(PackedInts):
    type: Annotated[int, PackedInt(bits=2)]
    bar: Annotated[int, PackedInt(bits=10)]
    offset: Annotated[int, PackedInt(bits=4)]
