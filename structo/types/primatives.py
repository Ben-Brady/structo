import typing as t
import io
import struct
from ..basetypes import Serializer

def struct_serializer(sformat: str, bytes: int) -> Serializer:
    class StructSerializer(Serializer):
        def length(self, _):
            return bytes

        def write(self, buf: io.Writer, _: type, value: int):
            data = struct.pack(sformat, value)
            return buf.write(data)

        def read(self, buf: io.Reader, _: type):
            data = buf.read(bytes)
            return struct.unpack(sformat, data)[0]

    return StructSerializer()


type uint64_BE = t.Annotated[int, struct_serializer(">Q", bytes=8)]
type uint64_LE = t.Annotated[int, struct_serializer("<Q", bytes=8)]
type uint64 = uint64_BE

type uint32_BE = t.Annotated[int, struct_serializer(">I", bytes=4)]
type uint32_LE = t.Annotated[int, struct_serializer("<I", bytes=4)]
type uint32 = uint32_BE

type uint16_BE = t.Annotated[int, struct_serializer(">H", bytes=2)]
type uint16_LE = t.Annotated[int, struct_serializer("<H", bytes=2)]
type uint16 = uint16_BE

type uint8 = t.Annotated[int, struct_serializer("B", bytes=1)]

type uint = uint64_BE | uint64_LE | uint32_BE | uint32_LE | uint16_BE | uint8

type int64_BE = t.Annotated[int, struct_serializer(">q", bytes=8)]
type int64_LE = t.Annotated[int, struct_serializer("<q", bytes=8)]
type int64 = int64_BE

type int32_BE = t.Annotated[int, struct_serializer(">i", bytes=4)]
type int32_LE = t.Annotated[int, struct_serializer("<i", bytes=4)]
type int32 = int32_BE

type int16_BE = t.Annotated[int, struct_serializer(">h", bytes=2)]
type int16_LE = t.Annotated[int, struct_serializer("<h", bytes=2)]
type int16 = int16_BE

type int8 = t.Annotated[int, struct_serializer("b", bytes=1)]


type float64_BE = t.Annotated[float, struct_serializer(">d", bytes=8)]
type float64_LE = t.Annotated[float, struct_serializer("<d", bytes=8)]
type float64 = float64_BE

type float32_BE = t.Annotated[float, struct_serializer(">f", bytes=4)]
type float32_LE = t.Annotated[float, struct_serializer("<f", bytes=4)]
type float32 = float32_BE


__all__ = ()
