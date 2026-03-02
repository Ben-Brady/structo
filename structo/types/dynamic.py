import typing as t
import io
from .primatives import uint
from ..t import Serializer, Format
from ..serialise import serialize, deserialize, read_uint

class ListSerializer(Serializer[list]):
    @staticmethod
    def write(buf: io.Writer, format: Format, value: list):
        tlength, tvalue = t.get_args(format)

        length = len(value)
        serialize(buf, tlength, length)
        for item in value:
            serialize(buf, tvalue, item)

    @staticmethod
    def read(buf: io.Reader, format: Format):
        tlength, tvalue = t.get_args(format)

        length = read_uint(buf, tlength)
        values = []
        for _ in range(length):
            value = deserialize(buf, tvalue)
            values.append(value)

        return values


class StringSerializer(Serializer[str]):
    @staticmethod
    def write(buf: io.Writer, format: Format, value: str):
        (tlength,) = t.get_args(format)
        data = value.encode("utf-8")
        length = len(data)

        serialize(buf, tlength, length)
        buf.write(data)

    @staticmethod
    def read(buf: io.Reader, format: Format):
        (tlength,) = t.get_args(format)

        length = deserialize(buf, tlength)
        data = buf.read(length)
        return data.decode("utf-8")


class BlobSerializer(Serializer[bytes]):
    @staticmethod
    def write(buf: io.Writer, format: Format, value: bytes):
        (tlength,) = t.get_args(format)

        length = len(value)
        serialize(buf, tlength, length)
        buf.write(value)

    @staticmethod
    def read(buf: io.Reader, format: Format):
        (tlength,) = t.get_args(format)

        length = deserialize(buf, tlength)
        data = buf.read(length)
        return data

type blob[Length: uint] = t.Annotated[bytes, BlobSerializer]
"""
**blob[Length: uint]**

A set of arbitrary bytes, prefixed with it's length

> Length: The integer type used to store the length

**Example**: `blob[uint32]`
---
"""

type string[Length] = t.Annotated[str, StringSerializer]
"""
string[Length: uint]
A string, prefixed with it's length

> Length: The integer type used to store the length

**Example**: `string[uint32]`

---
"""

type list[Length, Value] = t.Annotated[list, ListSerializer]
"""
list[Length: uint, Value: Serializable]
A list of elements, prefixed with it's length

> Length: The integer type used to store the length

> Value: The value to store in the array

**Example**: `list[uint16, float64]`

---
"""

