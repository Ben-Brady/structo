import typing as t
from ..serializer import Serializer


class LiteralSerializer(Serializer[bytes]):
    def write(self, buf, format, value):
        (tvalue,) = t.get_args(format)
        assert value == tvalue, f"expected {tvalue}, recieved {value}"
        buf.write(value)

    def read(self, buf, format):
        (tvalue,) = t.get_args(format)

        value = buf.read(len(tvalue))
        assert value == tvalue, f"expected {tvalue}, recieved {value}"
        return value

    def length(self, format):
        (tvalue,) = t.get_args(format)
        return len(tvalue)


type Literal[Value] = t.Annotated[bytes, LiteralSerializer()]
"""
**buffer[Value: bytes]**

A literal bytes value

> Value: The literal value

**Example**: `literal[b"mp4"]`

---
"""
