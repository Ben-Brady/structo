import annotationlib
import io
import struct
import typing as t

from .types import (
    Format,
    SerialiableObject,
    array,
    string,
    blob,
    uint64,
    uint32,
    uint16,
    uint8,
    int64,
    int32,
    int16,
    int8,
    float64,
    float32,
)


class Serializer[T]:
    @staticmethod
    def write(buf: io.Writer, format: Format, value: T): ...

    @staticmethod
    def read(buf: io.Reader, format: Format) -> T: ...


class SerialiableObjectSerializer(Serializer):
    @staticmethod
    def write(buf: io.Writer, format: type, value: SerialiableObject):
        annotations = annotationlib.get_annotations(format)
        for field_key, field_format in annotations.items():
            field_value = getattr(value, field_key)
            serialize(buf, field_format, field_value)

    @staticmethod
    def read(buf: io.Reader, format: type) -> SerialiableObject:
        annotations = annotationlib.get_annotations(format)
        attrs = {}
        for field_key, field_format in annotations.items():
            field_value = deserialize(buf, field_format)
            attrs[field_key] = field_value

        return format(**attrs)


class ArraySerializer(Serializer[list]):
    @staticmethod
    def write(buf: io.Writer, format: Format, value: list):
        tlength, tvalue = t.get_args(format)

        length = len(value)
        serialize(buf, tlength, length)
        for item in value:
            serialize(buf, tvalue, item)

    @staticmethod
    def read(buf: io.Reader, format: Format):
        tlength, tvalue = t.get_args(format)

        length = read_uint(buf, tlength)
        values = []
        for _ in range(length):
            value = deserialize(buf, tvalue)
            values.append(value)

        return values


class StringSerializer(Serializer[str]):
    @staticmethod
    def write(buf: io.Writer, format: Format, value: str):
        (tlength,) = t.get_args(format)

        data = value.encode("utf-8")
        length = len(data)

        serialize(buf, tlength, length)
        buf.write(data)

    @staticmethod
    def read(buf: io.Reader, format: Format):
        (tlength,) = t.get_args(format)

        length = deserialize(buf, tlength)
        data = buf.read(length)
        return data.decode("utf-8")


class BlobSerializer(Serializer[bytes]):
    @staticmethod
    def write(buf: io.Writer, format: Format, value: bytes):
        (tlength,) = t.get_args(format)

        length = len(value)
        serialize(buf, tlength, length)
        buf.write(value)

    @staticmethod
    def read(buf: io.Reader, format: Format):
        (tlength,) = t.get_args(format)

        length = deserialize(buf, tlength)
        data = buf.read(length)
        return data


def create_struct_serializer[T](sformat: str, length: int) -> type[Serializer[T]]:
    class StructSerializer(Serializer[T]):
        @staticmethod
        def write(buf: io.Writer, _: type, value: int):
            return buf.write(struct.pack(sformat, value))

        @staticmethod
        def read(buf: io.Reader, _: type):
            return struct.unpack(sformat, buf.read(length))[0]

    return StructSerializer


def _get_serializer(format: Format) -> type[Serializer]:
    DIRECT_PRIMATIVES = {
        uint64: create_struct_serializer(">Q", 8),
        uint32: create_struct_serializer(">I", 4),
        uint16: create_struct_serializer(">H", 2),
        uint8: create_struct_serializer("B", 1),
        int64: create_struct_serializer(">q", 8),
        int32: create_struct_serializer(">i", 4),
        int16: create_struct_serializer(">h", 2),
        int8: create_struct_serializer("b", 1),
        float64: create_struct_serializer(">d", 8),
        float32: create_struct_serializer(">f", 4),
    }

    if format in DIRECT_PRIMATIVES:
        return DIRECT_PRIMATIVES[format]

    GENERICS_PRIMATIVES = {
        array: ArraySerializer,
        string: StringSerializer,
        blob: BlobSerializer,
    }
    origin = t.get_origin(format)
    if origin in GENERICS_PRIMATIVES:
        return GENERICS_PRIMATIVES[origin]

    if isinstance(format, type) and issubclass(format, SerialiableObject):
        return SerialiableObjectSerializer

    raise NotImplementedError(f"No serializer for {format}")


def read_uint(buf: io.Reader, format: Format) -> int:
    value = deserialize(buf, format)
    assert isinstance(value, int), "uint not value"
    return value


def serialize(buf: io.Writer, format: Format, value: t.Any):
    return _get_serializer(format).write(buf, format, value)


def deserialize(buf: io.Reader, format: Format) -> t.Any:
    return _get_serializer(format).read(buf, format)
