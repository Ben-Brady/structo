import io
import typing as t
from .serializer import Serializer


def get_serializer(format: type) -> Serializer:
    from .serializer import Serializer
    from .object import SerializableObject
    from .types.object import ObjectSerializer

    if t.get_origin(format) is t.Annotated:
        args = t.get_args(format)
        serializers = [arg for arg in args if isinstance(arg, Serializer)]
        assert len(serializers) != 0, f"No serializers for {format} found"
        assert len(serializers) == 1, f"More than one serializers for {format} found"
        serializer = serializers[0]

        return serializer

    if issubclass(format, SerializableObject):
        return ObjectSerializer(format)

    # Nicely formatted errors:
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
