import typing as t
import io
from dataclasses import dataclass
from abc import ABC



class _SerialiableObjectMeta(type):
    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
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


type Format = type | t.TypeAliasType

class Serializer[T]:
    @staticmethod
    def length(format: Format) -> int | None:
        return None

    @staticmethod
    def write(buf: io.Writer, format: Format, value: T): ...

    @staticmethod
    def read(buf: io.Reader, format: Format) -> T: ...
