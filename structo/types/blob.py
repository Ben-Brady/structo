import typing as t
from .primatives import uint
from ..serializer import Serializer
from ..serialise import write_serializable, read_serializable, read_uint



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
