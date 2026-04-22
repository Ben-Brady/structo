from ..interfaces import Serializer
from ..serialise import to_serializer


NONE_TYPE_BYTE = bytes([0])
VALUE_TYPE_BYTE = bytes([255])


class Optional[T](Serializer[T | None]):
    _value_type: Serializer[T]

    def __init__(self, value: Serializer[T] | type[T]) -> None:
        self._value_type = to_serializer(value)

    def write(self, f, value):
        if value is None:
            f.write(NONE_TYPE_BYTE)
        else:
            f.write(VALUE_TYPE_BYTE)
            self._value_type.write(f, value)

    def read(self, f):
        type_byte = f.read(1)

        assert type_byte in (
            NONE_TYPE_BYTE,
            VALUE_TYPE_BYTE,
        ), f"Unexpected type byte {type_byte}"

        if type_byte == NONE_TYPE_BYTE:
            return None
        else:
            return self._value_type.read(f)

