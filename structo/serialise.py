import typing as t
from .interfaces import Serializer, Serializable


def to_serializer[T](format: type[T] | Serializer[T]) -> Serializer[T]:
    if isinstance(format, Serializer):
        return format

    if isinstance(format, type) and issubclass(format, Serializable):
        return format._cached_serializer()

    raise AssertionError(f"Invalid value_type: {format}")


serializer_cache: dict[int, Serializer] = {}


def get_serializer(format: type | Serializer) -> Serializer:
    cache_key = id(format)
    if cache_key in serializer_cache:
        return serializer_cache[cache_key]

    if t.get_origin(format) is t.Annotated:
        args = t.get_args(format)
        serializers = [arg for arg in args if isinstance(arg, Serializer)]
        assert len(serializers) != 0, f"No serializers for {format} found"
        assert len(serializers) == 1, f"More than one serializers for {format} found"
        serializer = serializers[0]
        serializer_cache[cache_key] = serializer
        return serializer

    if isinstance(format, type) and issubclass(format, Serializable):
        serializer_cache[cache_key] = format._cached_serializer()
        return serializer_cache[cache_key]

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
