import typing as t
import io
from dataclasses import dataclass
import annotationlib

from .serialise import get_serializer, write_serializable, read_serializable


class SerializableObjectMeta(type):
    def __new__(cls, name, bases, dct):

        new_class = super().__new__(cls, name, bases, dct)
        annotate = annotationlib.get_annotate_from_class_namespace(dct)
        if annotate:
            attrs = annotate(annotationlib.Format.VALUE_WITH_FAKE_GLOBALS)
            for key, value in attrs.items():
                try:
                    get_serializer(value)
                except Exception as e:
                    raise ValueError(
                        f"Invalid attribute defintion for {name}.{key}"
                    ) from e

        return dataclass(new_class)  # type: ignore


@t.dataclass_transform()
class SerializableObject(metaclass=SerializableObjectMeta):
    @classmethod
    def read(cls, buf: io.Reader) -> t.Self:

        return read_serializable(buf, cls)

    def write(self, buf: io.Writer):

        write_serializable(buf, type(self), self)

    @classmethod
    def from_bytes(cls, data: bytes) -> t.Self:
        buf = io.BytesIO(data)
        return cls.read(buf)

    def to_bytes(self) -> bytes:
        buf = io.BytesIO()
        self.write(buf)
        buf.seek(0)
        return buf.read()
