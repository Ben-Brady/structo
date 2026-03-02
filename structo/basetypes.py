import typing as t
import io
from dataclasses import dataclass
import annotationlib
from abc import ABC

type Format = type | t.TypeAliasType

class Serializer[T]:
    def length(self, format: Format) -> int | None:
        return None

    def write(self, buf: io.Writer, format: Format, value: T): ...

    def read(self, buf: io.Reader, format: Format) -> T: ...


class _SerialiableObjectMeta(type):
    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
        annotate = annotationlib.get_annotate_from_class_namespace(dct)
        if annotate:
            print(annotate(annotationlib.Format.VALUE))
        return dataclass(new_class)  # type: ignore


@t.dataclass_transform()
class SerialiableObject(metaclass=_SerialiableObjectMeta):
    @classmethod
    def read(cls, buf: io.Reader) -> t.Self:
        from .serialise import deserialize

        return deserialize(buf, cls)

    def write(self, buf: io.Writer):
        from .serialise import serialize

        serialize(buf, type(self), self)

    @classmethod
    def from_bytes(cls, data: bytes) -> t.Self:
        buf = io.BytesIO(data)
        return cls.read(buf)

    def to_bytes(self) -> bytes:
        buf = io.BytesIO()
        self.write(buf)
        buf.seek(0)
        return buf.read()
