import typing as t
from ..t import Serializer
from ..serialise import serialize, deserialize, get_serializer


class FixedBlobSerializer(Serializer[bytes]):
    @staticmethod
    def write(buf, format, value):
        (length,) = t.get_args(format)

        assert len(value) == length, f"recieved data with {len(value)} length, expected {length}"
        buf.write(value)

    @staticmethod
    def read(buf, format):
        (length,) = t.get_args(format)

        data = buf.read(length)
        return data

    @staticmethod
    def length(format):
        (length,) = t.get_args(format)
        return length


class ArraySerializer(Serializer[list]):
    @staticmethod
    def write(buf, format, value):
        (length, tvalue) = t.get_args(format)

        assert len(value) == length, f"recieved array with {len(value)} length, expected {length}"
        for item in value:
            serialize(buf, tvalue, item)

    @staticmethod
    def read(buf, format):
        (length, tvalue) = t.get_args(format)

        items = []
        for _ in range(length):
            items.append(deserialize(buf, tvalue))

        return items

    @staticmethod
    def length(format):
        (length, tvalue) = t.get_args(format)

        element_length = get_serializer(tvalue).length(tvalue)
        if element_length is None:
            return None
        else:
            return element_length * length



type buffer[Length] = t.Annotated[bytes, FixedBlobSerializer]
"""
**buffer[Length: int]**

A fixed length bytes

> Length: The integer type used to store the length

**Example**: `buffer[32]`

---
"""


type array[Length, Value] = t.Annotated[list[Value], ArraySerializer]
"""
**array[Length: int, Value: Serializable]**

An fixed length array of values

> Length: The number of elmenets

> Value: The value to store in the array

**Example**: `array[8, uint32]`

---
"""
