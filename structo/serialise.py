import io
import typing as t
import annotationlib
from .basetypes import (
    Format, Serializer, SerialiableObject
)


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


def get_serializer(format: Format) -> Serializer:
    if hasattr(format, "__value__"):
        format = format.__value__

    if t.get_origin(format) is t.Annotated:
        args = t.get_args(format)
        serializers = [arg for arg in args if isinstance(arg, Serializer)]
        assert len(serializers) != 0, f"No serializers for {format} found"
        assert len(serializers) == 1, f"More than one serializers for {format} found"
        serializer = serializers[0]

        return serializer

    if isinstance(format, type) and issubclass(format, SerialiableObject):
        return SerialiableObjectSerializer()

    if format == int:
        raise ValueError(f"No serializer for int, you need to use structo uint32, int32, etc instead")
    if format == float:
        raise ValueError(f"No serializer for float, you need to use structo float32 or float64 instead")
    if format == bytes:
        raise ValueError(f"No serializer for float, you need to use structor Buffer or Blob instead")
    if format == list:
        raise ValueError(f"No serializer for list, you need to use structo List or Array instead")

    raise NotImplementedError(f"No serializer for {format}")


def serialize(buf: io.Writer, format: Format, value: t.Any):
    return get_serializer(format).write(buf, format, value)


def deserialize(buf: io.Reader, format: Format) -> t.Any:
    return get_serializer(format).read(buf, format)

def read_uint(buf: io.Reader, format: Format) -> int:
    value = deserialize(buf, format)

    assert isinstance(value, int), f"expected uint, got {format}"
    assert value >= 0 , "expected uint, got {format}"

    return value

