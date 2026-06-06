import typing as t
from .interfaces import Serializer, Serializable, SerializerType

serializer_cache: dict[int, Serializer[t.Any]] = {}


def get_serializer[T](format: SerializerType[T]) -> Serializer[T]:
    cache_key = id(format)
    if cache_key in serializer_cache:
        return serializer_cache[cache_key]

    if isinstance(format, t.TypeAliasType):
        format = format.__value__

    if isinstance(format, Serializer):
        return format

    if t.get_origin(format) is t.Annotated:
        args = t.get_args(format)
        serializers = []
        for arg in args:
            try:
                serializers.append(get_serializer(arg))
            except:
                pass

        assert len(serializers) != 0, f"No serializers for {format} found"
        assert len(serializers) == 1, f"More than one serializers for {format} found"
        serializer = serializers[0]
        serializer_cache[cache_key] = serializer
        return serializer

    if isinstance(format, type) and issubclass(format, Serializable):
        serializer_cache[cache_key] = format._cached_serializer()
        return serializer_cache[cache_key]

    # Nicely formatted errors
    if format == int:
        raise ValueError(
            f"No serializer for int, you need to use Annotated[int, structo.int64] instead"
        )
    if format == float:
        raise ValueError(
            f"No serializer for float, you need to use Annotated[int, structo.float64] instead"
        )
    if format == bytes:
        raise ValueError(
            f"No serializer for bytes, you need to use Annotated[bytes structo.Blob] instead"
        )
    if format == list:
        raise ValueError(
            f"No serializer for list, you need to use Annotated[list, structo.List] instead"
        )

    raise NotImplementedError(f"No serializer found for {format}")
