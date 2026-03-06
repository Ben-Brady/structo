import io
import annotationlib
import typing as t
from dataclasses import dataclass

from .serializer import Serialiable, Serializer
from .serialise import get_serializer


class SerializableObjectMeta(type):
    def __new__(cls, name, bases, dct):
        new_class = t.cast(type, super().__new__(cls, name, bases, dct))
        if name == "SerializableObject":
            return new_class

        annotate = annotationlib.get_annotate_from_class_namespace(dct)
        _annotations: dict[str, Serializer] = {}

        if annotate:
            attrs = annotate(annotationlib.Format.VALUE_WITH_FAKE_GLOBALS)
            for key, value in attrs.items():
                try:
                    serializer = get_serializer(value)
                    _annotations[key] = serializer
                except Exception as e:
                    raise ValueError(
                        f"Invalid attribute defintion for {name}.{key}"
                    ) from e

        return t.cast(SerializableObject, dataclass(new_class))


# This is very messed up since we
@t.dataclass_transform()
class SerializableObject(Serialiable, metaclass=SerializableObjectMeta):
    @classmethod
    def serializer(cls) -> Serializer[t.Self]:
        from .types import ObjectSerializer
        return ObjectSerializer(cls)

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
