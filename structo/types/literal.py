import typing as t
import types
from ..serializer import Serializer


class LiteralSerializer(Serializer[bytes]):
    value: bytes

    def __init__(self, value: t.TypeVar) -> None:
        print(value)
        print(t.get_origin(value))
        print(t.get_args(value))
        print(t.evaluate_forward_ref(value))
        assert (
            value is None
        ), "Literal must have a bytes parameter, e.g. Literal[b'foo']"
        assert isinstance(
            value, bytes
        ), "Literal parameter must be type bytes, e.g. Literal[b'foo']"

    def write(self, buf, format, value):
        assert value == self.value, f"expected {self.value}, recieved {value}"
        buf.write(self.value)

    def read(self, buf, format):
        value = buf.read(len(self.value))
        assert value == self.value, f"expected {self.value}, recieved {value}"
        return self.value

    def sizeof(self, format):
        return len(self.value)


type _Literal[Value] = t.Annotated[bytes, LiteralSerializer(Value)]


class Literal(bytes):
    """
    **buffer[Value: bytes]**

    A literal bytes value

    > Value: The literal value

    **Example**: `literal[b"mp4"]`

    ---
    """

    @classmethod
    def __class_getitem__(cls, value: t.Any):
        return _Literal[bytes]
