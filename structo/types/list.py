import typing as t
from .primatives import uint
from ..serializer import Serializer
from ..serialise import write_serializable, read_serializable, read_uint


class ListSerializer(Serializer[list[t.Any]]):
    def write(self, buf, format, value):
        tlength, tvalue = t.get_args(format)

        length = len(value)
        write_serializable(buf, tlength, length)
        for item in value:
            write_serializable(buf, tvalue, item)

    def read(self, buf, format):
        tlength, tvalue = t.get_args(format)

        length = read_uint(buf, tlength)
        values = []
        for _ in range(length):
            value = read_serializable(buf, tvalue)
            values.append(value)

        return values

type List[Length, Value] = t.Annotated[list[Value], ListSerializer()]
"""
list[Length: uint, Value: Serializable]
A list of elements, prefixed with it's length

> Length: The integer type used to store the length

> Value: The value to store in the array

**Example**: `list[uint16, float64]`

---
"""
