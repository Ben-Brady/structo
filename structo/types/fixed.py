import typing as t
from ..serializer import Serializer
from ..serialise import write_serializable, read_serializable, get_serializer


class FixedBlobSerializer(Serializer[bytes]):
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

    def length(self, format):
        (length,) = t.get_args(format)
        return length


class ArraySerializer(Serializer[list]):
    def write(self, buf, format, value):
        length, tvalue = t.get_args(format)

        assert (
            len(value) == length
        ), f"recieved array with {len(value)} length, expected {length}"
        for item in value:
            write_serializable(buf, tvalue, item)

    def read(self, buf, format):
        length, tvalue = t.get_args(format)

        items = []
        for _ in range(length):
            items.append(read_serializable(buf, tvalue))

        return items

    def length(self, format):
        length, tvalue = t.get_args(format)

        element_length = get_serializer(tvalue).length(tvalue)
        if element_length is None:
            return None
        else:
            return element_length * length


type Buffer[Length] = t.Annotated[bytes, FixedBlobSerializer]
"""
**buffer[Length: int]**

A fixed length bytes

> Length: The integer type used to store the length

**Example**: `buffer[32]`

---
"""


type Array[Length, Value] = t.Annotated[list[Value], ArraySerializer]
"""
**array[Length: int, Value: Serializable]**

An fixed length array of values

> Length: The number of elmenets

> Value: The value to store in the array

**Example**: `array[8, uint32]`

---
"""
