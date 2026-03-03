import typing as t
import io
from .primatives import uint
from ..serializer import Serializer, Format
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


class BlobSerializer(Serializer[bytes]):
    def write(self, buf, format, value):
        (tlength,) = t.get_args(format)

        length = len(value)
        write_serializable(buf, tlength, length)
        buf.write(value)

    def read(self, buf, format):
        (tlength,) = t.get_args(format)

        length = read_serializable(buf, tlength)
        data = buf.read(length)
        return data


type Blob[Length: uint] = t.Annotated[bytes, BlobSerializer()]
"""
**blob[Length: uint]**

A set of arbitrary bytes, prefixed with it's length

> Length: The integer type used to store the length

**Example**: `blob[uint32]`
---
"""

type String[Length] = t.Annotated[str, StringSerializer()]
"""
string[Length: uint]
A string, prefixed with it's length

> Length: The integer type used to store the length

**Example**: `string[uint32]`

---
"""

type List[Length, Value] = t.Annotated[list[Value], ListSerializer()]
"""
list[Length: uint, Value: Serializable]
A list of elements, prefixed with it's length

> Length: The integer type used to store the length

> Value: The value to store in the array

**Example**: `list[uint16, float64]`

---
"""
