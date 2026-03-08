from ..interfaces import Serializable, Serializer

import typing as t
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
        from ..serializers import PackedIntSerializer

        return PackedIntSerializer(cls)
