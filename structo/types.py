import typing as t
import io
from dataclasses import dataclass

type uint8 = int
type uint16 = int
type uint32 = int
type uint64 = int

type int8 = int
type int16 = int
type int32 = int
type int64 = int

type float32 = float
type float64 = float

type uint = uint8 | uint16 | uint32 | uint64
type sint = int8 | int16 | int32 | int64


type fixedblob[Length] = bytes
"""
fixedblob[Length]
A fixed length of data

> **length**: The length of the data in bytes

Example:
```
fixedblob[32] # 32 bytes of data
```
---
#### Bytes Documentation
"""

type blob[Length: uint] = bytes
"""
blob[Length: uint]
An arbitrary

> Length: The integer type used to store the length
"""
type string[Length: uint] = str
"""
string[Length: uint]

> Length: The integer type used to store the length
"""

type array[Length: uint, Value: Serializable] = list
"""
array[Length: uint, Value: Serializable]

> Length: The integer type used to store the length

> Value: The value to store in the array
"""


class _SerialiableObjectMeta(type):
    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
        return dataclass(new_class)  # type: ignore


@t.dataclass_transform()
class SerialiableObject(metaclass=_SerialiableObjectMeta):
    @classmethod
    def read(cls, buf: io.Reader) -> t.Self:
        from .serialise import deserialize

        return deserialize(buf, type(cls))

    def write(self, buf: io.Writer):
        from .serialise import serialize

        serialize(buf, type(self), self)

    def from_bytes(self, data: bytes) -> t.Self:
        buf = io.BytesIO(data)
        return self.read(buf)

    def to_bytes(self) -> bytes:
        buf = io.BytesIO()
        self.write(buf)
        buf.seek(0)
        return buf.read()


type Primative = string | array | uint | int | float
type Serializable = SerialiableObject | Primative
type Format = type | t.TypeAliasType
