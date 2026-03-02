import typing as t
from ..t import Serializer
from ..serialise import serialize, deserialize, get_serializer


class LiteralSerializer(Serializer[bytes]):
    @staticmethod
    def write(buf, format, value):
        (tvalue,) = t.get_args(format)
        assert value == tvalue, f"expected {tvalue}, recieved {value}"
        buf.write(value)

    @staticmethod
    def read(buf, format):
        (tvalue,) = t.get_args(format)

        value = buf.read(len(tvalue))
        assert value == tvalue, f"expected {tvalue}, recieved {value}"
        return value

    @staticmethod
    def length(format):
        (tvalue,) = t.get_args(format)
        return len(tvalue)



type literal[Value] = t.Annotated[bytes, LiteralSerializer]
"""
**buffer[Value: bytes]**

A literal bytes value

> Value: The literal value

**Example**: `literal[b"mp4 "]`

---
"""
