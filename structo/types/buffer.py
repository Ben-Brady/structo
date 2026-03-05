import typing as t
from ..serializer import Serializer
from ..serialise import write_serializable, read_serializable, get_serializer


class BufferSerializer(Serializer[bytes]):
    def write(self, buf, format, value):
        (length,) = t.get_args(format)

        assert (
            len(value) == length
        ), f"recieved data with {len(value)} length, expected {length}"
        buf.write(value)

    def read(self, buf, format):
        (length,) = t.get_args(format)

        data = buf.read(length)
        return data

    def sizeof(self, format):
        (length,) = t.get_args(format)
        return length


type Buffer[Length] = t.Annotated[bytes, BufferSerializer()]
"""
**buffer[Length: int]**

A fixed length bytes

> Length: The integer type used to store the length

**Example**: `buffer[32]`

---
"""

