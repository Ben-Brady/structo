import typing as t
from .primatives import uint
from ..serializer import Serializer
from ..serialise import write_serializable, read_serializable, read_uint

class StringSerializer(Serializer[str]):
    def write(self, buf, format, value):
        (tlength,) = t.get_args(format)
        data = value.encode("utf-8")
        length = len(data)

        write_serializable(buf, tlength, length)
        buf.write(data)

    def read(self, buf, format):
        (tlength,) = t.get_args(format)

        length = read_serializable(buf, tlength)
        data = buf.read(length)
        return data.decode("utf-8")



type String[Length] = t.Annotated[str, StringSerializer()]
"""
string[Length: uint]
A string, prefixed with it's length

> Length: The integer type used to store the length

**Example**: `string[uint32]`

---
"""
