import typing as t
import io
import annotationlib

from ..interfaces import Serializer
from ..objects import Struct
from ..serialise import get_serializer


class StructSerializer[T: Struct](Serializer[T]):
    _annotations: dict[str, Serializer] = {}
    _type: type

    def __init__(self, type: type[T]) -> None:
        annotations: dict[str, Serializer] = {}
        self._type = type

        attrs = annotationlib.get_annotations(type)
        for key, value in attrs.items():
            try:
                annotations[key] = get_serializer(value)
            except Exception as e:
                raise ValueError(
                    f"Invalid attribute defintion for {type.__name__}.{key}"
                ) from e

        self._annotations = annotations

    def sizeof(self) -> int | None:
        total_size = 0
        for serializer in self._annotations.values():
            field_size = serializer.sizeof()
            if field_size is None:
                return None
            else:
                total_size += field_size

        return total_size

    def write(self, f, value):
        for field_key, field_format in self._annotations.items():
            field_value = getattr(value, field_key)
            field_format.write(f, field_value)

    def read(self, f):
        attrs = {}

        for field_key, field_format in self._annotations.items():
            field_value = field_format.read(f)
            attrs[field_key] = field_value

        return self._type(**attrs)
