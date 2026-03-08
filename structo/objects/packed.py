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
        assert annotate, f"Annotations not found for {name}"

        annotations = annotate(annotationlib.Format.VALUE_WITH_FAKE_GLOBALS)

        bits: dict[str, int] = {}
        for key, value in annotations.items():
            err_msg = f"expected Annotated[int, PackedInt(...)] on {name}.{key}"
            assert t.get_origin(value) is t.Annotated, err_msg

            ints = [arg for arg in t.get_args(value) if isinstance(arg, PackedInt)]
            assert len(ints) <= 1, err_msg
            assert len(ints) == 1, err_msg
            bits[key] = ints[0].bits

        obj = t.cast(PackedInts, dataclass(new_class))
        obj._bits = bits
        return obj


# This is very messed up since we
@t.dataclass_transform()
class PackedInts(Serializable, metaclass=PackedIntsMeta):
    _bits: dict[str, int]

    @classmethod
    def serializer(cls) -> Serializer[t.Self]:
        from ..serializers import PackedIntSerializer

        return PackedIntSerializer(cls)
