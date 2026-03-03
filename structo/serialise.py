import io
import typing as t
import annotationlib
from .serializer import Format, Serializer


def get_serializer(format: Format) -> Serializer:
    from .object import SerializableObject

    class SerialiableObjectSerializer(Serializer):
        @staticmethod
        def write(buf: io.Writer, format: type, value: SerializableObject):
            annotations = annotationlib.get_annotations(format)
            for field_key, field_format in annotations.items():
                field_value = getattr(value, field_key)
                write_serializable(buf, field_format, field_value)

        @staticmethod
        def read(buf: io.Reader, format: type) -> SerializableObject:
            annotations = annotationlib.get_annotations(format)
            attrs = {}
            for field_key, field_format in annotations.items():
                field_value = read_serializable(buf, field_format)
                attrs[field_key] = field_value

            return format(**attrs)

    if hasattr(format, "__value__"):
        format = format.__value__

    if t.get_origin(format) is t.Annotated:
        args = t.get_args(format)
        serializers = [arg for arg in args if isinstance(arg, Serializer)]
        assert len(serializers) != 0, f"No serializers for {format} found"
        assert len(serializers) == 1, f"More than one serializers for {format} found"
        serializer = serializers[0]

        return serializer

    if isinstance(format, type) and issubclass(format, SerializableObject):
        return SerialiableObjectSerializer()

    if format == int:
        raise ValueError(
            f"No serializer for int, you need to use structo.int32, structo.int32 or similar instead"
        )
    if format == float:
        raise ValueError(
            f"No serializer for float, you need to use structo.float32 or structo.float64 instead"
        )
    if format == bytes:
        raise ValueError(
            f"No serializer for bytes, you need to use structo.Buffer or structo.Blob instead"
        )
    if format == list:
        raise ValueError(
            f"No serializer for list, you need to use structo.List or structo.Array instead"
        )

    raise NotImplementedError(f"No serializer found for {format}")


def write_serializable(buf: io.Writer, format: Format, value: t.Any):
    return get_serializer(format).write(buf, format, value)


def read_serializable(buf: io.Reader, format: Format) -> t.Any:
    return get_serializer(format).read(buf, format)


def read_uint(buf: io.Reader, format: Format) -> int:
    value = read_serializable(buf, format)

    assert isinstance(value, int), f"expected uint, got {format}"
    assert value >= 0, "expected uint, got {format}"

    return value
