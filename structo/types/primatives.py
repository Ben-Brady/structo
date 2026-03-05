import typing as t
import io
import struct
from ..serializer import Serializer


def struct_serializer(sformat: str, bytes: int) -> Serializer:
    class StructSerializer(Serializer):
        def sizeof(self, _):
            return bytes

        def write(self, buf: io.Writer, _: type, value: int):
            data = struct.pack(sformat, value)
            return buf.write(data)

        def read(self, buf: io.Reader, _: type):
            data = buf.read(bytes)
            return struct.unpack(sformat, data)[0]

    return StructSerializer()


type uint64_BE = t.Annotated[int, struct_serializer(">Q", bytes=8)]
"**unsigned 64bit integer - big endian**\n\n---"
type uint64_LE = t.Annotated[int, struct_serializer("<Q", bytes=8)]
"**unsigned 64bit integer - little endian**\n\n---"
uint64 = uint64_BE
"**unsigned 64bit integer - big endian**\n\n---"

type uint32_BE = t.Annotated[int, struct_serializer(">I", bytes=4)]
"**unsigned 32bit integer - big endian**\n\n---"
type uint32_LE = t.Annotated[int, struct_serializer("<I", bytes=4)]
"**unsigned 32bit integer - little endian**\n\n---"
uint32 = uint32_BE
"**unsigned 32bit integer - big endian**\n\n---"

type uint16_BE = t.Annotated[int, struct_serializer(">H", bytes=2)]
"**unsigned 16bit integer - big endian**\n\n---"
type uint16_LE = t.Annotated[int, struct_serializer("<H", bytes=2)]
"**unsigned 16bit integer - little endian**\n\n---"
uint16: t.TypeAlias = uint16_BE
"**unsigned 16bit integer - big endian**\n\n---"

type uint8 = t.Annotated[int, struct_serializer("B", bytes=1)]
"**unsigned 8bit integer**\n\n---"

uint = uint64_BE | uint64_LE | uint32_BE | uint32_LE | uint16_BE | uint8

type int64_BE = t.Annotated[int, struct_serializer(">q", bytes=8)]
"**signed 64bit integer - big endian**\n\n---"
type int64_LE = t.Annotated[int, struct_serializer("<q", bytes=8)]
"**signed 64bit integer - little endian**\n\n---"
int64 = int64_BE
"**signed 64bit integer - big endian**\n\n---"

type int32_BE = t.Annotated[int, struct_serializer(">i", bytes=4)]
"**signed 32bit integer - big endian**\n\n---"
type int32_LE = t.Annotated[int, struct_serializer("<i", bytes=4)]
"**signed 32bit integer - little endian**\n\n---"
int32 = int32_BE
"**signed 32bit integer - big endian**\n\n---"

type int16_BE = t.Annotated[int, struct_serializer(">h", bytes=2)]
"**signed 16bit integer - big endian**\n\n---"
type int16_LE = t.Annotated[int, struct_serializer("<h", bytes=2)]
"**signed 16bit integer - little endian**\n\n---"
int16 = int16_BE
"**signed 16bit integer - big endian**\n\n---"

type int8 = t.Annotated[int, struct_serializer("b", bytes=1)]
"**signed 8bit integer**\n\n---"


type float64_BE = t.Annotated[float, struct_serializer(">d", bytes=8)]
"**64bit float - big endian**\n\n---"
type float64_LE = t.Annotated[float, struct_serializer("<d", bytes=8)]
"**64bit float - little endian**\n\n---"
float64 = float64_BE
"**64bit float - big endian**\n\n---"

type float32_BE = t.Annotated[float, struct_serializer(">f", bytes=4)]
"**32bit float - big endian**\n\n---"
type float32_LE = t.Annotated[float, struct_serializer("<f", bytes=4)]
"**32bit float - little endian**\n\n---"
float32 = float32_BE
"**32bit float - big endian**\n\n---"


__all__ = ()
