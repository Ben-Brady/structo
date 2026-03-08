import annotationlib
import typing as t
from dataclasses import dataclass

from ..interfaces import Serializable, Serializer
from ..serialise import get_serializer


class SerializableObjectMeta(type):
    def __new__(cls, name, bases, dct):
        new_class = t.cast(type, super().__new__(cls, name, bases, dct))
        if name == "SerializableObject":
            return new_class

        annotate = annotationlib.get_annotate_from_class_namespace(dct)

        assert annotate, "No annotations method available"
        annotations = annotate(annotationlib.Format.VALUE_WITH_FAKE_GLOBALS)

        fields: dict[str, Serializer] = {}
        for key, annotation in annotations.items():
            try:
                fields[key] = get_serializer(annotation)
            except Exception as e:
                raise ValueError(f"Invalid attribute defintion for {name}.{key}") from e

        return t.cast(SerializableObject, dataclass(new_class))


# This is very messed up since we
@t.dataclass_transform()
class SerializableObject(Serializable, metaclass=SerializableObjectMeta):
    @classmethod
    def serializer(cls) -> Serializer[t.Self]:
        from ..serializers import ObjectSerializer

        return ObjectSerializer(cls)
