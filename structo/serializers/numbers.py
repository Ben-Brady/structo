import typing as t
import io
import struct
from ..interfaces import Serializer


def struct_serializer(sformat: str, size: int) -> Serializer:
    class StructPackSerializer(Serializer):
        def sizeof(self):
            return size

        def write(self, f, value):
            data = struct.pack(sformat, value)
            return f.write(data)

        def read(self, f):
            data = f.read(size)
            assert len(data) == size, f"Expected {size} bytes"
            return struct.unpack(sformat, data)[0]

    return StructPackSerializer()


def int_serializer(
    *,
    name: str,
    size: int,
    byteorder: t.Literal['little', 'big'],
    signed: bool,
) -> Serializer:
    class IntSerializer(Serializer[int]):
        def sizeof(self):
            return size

        def write(self, f, value):
            data = value.to_bytes(size, byteorder=byteorder, signed=signed)
            return f.write(data)

        def read(self, f):
            data = f.read(size)
            assert len(data) == size, f"Expected {size} bytes"
            return int.from_bytes(data, byteorder=byteorder, signed=signed)
    IntSerializer.__name__ = name
    return IntSerializer()


uint64: Serializer[int] = int_serializer(
    name="uint64",
    size=8, byteorder="little", signed=False)
"**unsigned 64bit integer - little endian**"

uint64_LE: Serializer[int] = int_serializer(name="uint64_LE",
                                            size=8, byteorder="little", signed=False)
"**unsigned 64bit integer - little endian**"

uint64_BE: Serializer[int] = int_serializer(name="uint64_BE",
                                            size=8, byteorder="big", signed=False)
"**unsigned 64bit integer - big endian**"


uint32: Serializer[int] = int_serializer(name="uint32",
                                         size=4, byteorder="little", signed=False)
"**unsigned 32bit integer - little endian**"

uint32_LE: Serializer[int] = int_serializer(name="uint32_LE",
                                            size=4, byteorder="little", signed=False)
"**unsigned 32bit integer - little endian**"

uint32_BE: Serializer[int] = int_serializer(name="uint32_BE",
                                            size=4, byteorder="big", signed=False)
"**unsigned 32bit integer - big endian**"


uint16: Serializer[int] = int_serializer(
    name="uint16", size=2,
    byteorder="little", signed=False)
"**unsigned 16bit integer - little endian**"

uint16_LE: Serializer[int] = int_serializer(
    name="uint16_LE", size=2,
    byteorder="little", signed=False)
"**unsigned 16bit integer - little endian**"

uint16_BE: Serializer[int] = int_serializer(
    name="uint16_BE", size=2,
    byteorder="big", signed=False)
"**unsigned 16bit integer - big endian**"


uint8: Serializer[int] = int_serializer(name="uint8",
                                        size=1, byteorder="big", signed=False)
"**unsigned 8bit integer**"


int64: Serializer[int] = int_serializer(
    name="int64", size=8,
    byteorder="little", signed=True)
"**signed 64bit integer - little endian**"

int64_LE: Serializer[int] = int_serializer(
    name="int64_LE", size=8,
    byteorder="little", signed=True)
"**signed 64bit integer - little endian**"

int64_BE: Serializer[int] = int_serializer(
    name="int64_BE", size=8,
    byteorder="big", signed=True)
"**signed 64bit integer - big endian**"


int32: Serializer[int] = int_serializer(
    name="int32", size=4,
    byteorder="little", signed=True)
"**signed 32bit integer - little endian**"
int32_LE: Serializer[int] = int_serializer(
    name="int32_LE", size=4,
    byteorder="little", signed=True)
"**signed 32bit integer - little endian**"
int32_BE: Serializer[int] = int_serializer(
    name="int32_BE", size=4,
    byteorder="big", signed=True)
"**signed 32bit integer - big endian**"


int16: Serializer[int] = int_serializer(
    name="int16", size=2,
    byteorder="little", signed=True)
"**signed 16bit integer - little endian**"

int16_LE: Serializer[int] = int_serializer(
    name="int16_LE", size=2,
    byteorder="little", signed=True)
"**signed 16bit integer - little endian**"

int16_BE: Serializer[int] = int_serializer(
    name="int16_BE", size=2,
    byteorder="big", signed=True)
"**signed 16bit integer - big endian**"


int8: Serializer[int] = int_serializer(
    name="int8", size=1,
    byteorder="little", signed=True)
"**signed 8bit integer**"


float64: Serializer[float] = struct_serializer("<d", size=8)
"**64bit float - little endian**"

float64_LE: Serializer[float] = struct_serializer("<d", size=8)
"**64bit float - little endian**"

float64_BE: Serializer[float] = struct_serializer(">d", size=8)
"**64bit float - big endian**"


float32: Serializer[float] = struct_serializer("<f", size=4)
"**32bit float - little endian**"

float32_LE: Serializer[float] = struct_serializer("<f", size=4)
"**32bit float - little endian**"

float32_BE: Serializer[float] = struct_serializer(">f", size=4)
"**32bit float - big endian**"
