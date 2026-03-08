import io
import struct
from ..interfaces import Serializer


def struct_serializer(sformat: str, bytes: int) -> Serializer:
    class StructSerializer(Serializer):
        def sizeof(self):
            return bytes

        def write(self, buf: io.Writer, value: int):
            data = struct.pack(sformat, value)
            return buf.write(data)

        def read(self, buf: io.Reader):
            data = buf.read(bytes)
            return struct.unpack(sformat, data)[0]

    return StructSerializer()


uint64_BE: Serializer[int] = struct_serializer(">Q", bytes=8)
"**unsigned 64bit integer - big endian**"

uint64_LE: Serializer[int] = struct_serializer("<Q", bytes=8)
"**unsigned 64bit integer - little endian**"

uint64 = uint64_BE
"**unsigned 64bit integer - big endian**"

uint32_BE: Serializer[int] = struct_serializer(">I", bytes=4)
"**unsigned 32bit integer - big endian**"

uint32_LE: Serializer[int] = struct_serializer("<I", bytes=4)
"**unsigned 32bit integer - little endian**"

uint32 = uint32_BE
"**unsigned 32bit integer - big endian**"

uint16_BE: Serializer[int] = struct_serializer(">H", bytes=2)
"**unsigned 16bit integer - big endian**"

uint16_LE: Serializer[int] = struct_serializer("<H", bytes=2)
"**unsigned 16bit integer - little endian**"

uint16 = uint16_BE
"**unsigned 16bit integer - big endian**"

uint8: Serializer[int] = struct_serializer("B", bytes=1)
"**unsigned 8bit integer**"

int64_BE: Serializer[int] = struct_serializer(">q", bytes=8)
"**signed 64bit integer - big endian**"

int64_LE: Serializer[int] = struct_serializer("<q", bytes=8)
"**signed 64bit integer - little endian**"

int64 = int64_BE
"**signed 64bit integer - big endian**"

int32_BE: Serializer[int] = struct_serializer(">i", bytes=4)
"**signed 32bit integer - big endian**"

int32_LE: Serializer[int] = struct_serializer("<i", bytes=4)
"**signed 32bit integer - little endian**"

int32 = int32_BE
"**signed 32bit integer - big endian**"

int16_BE: Serializer[int] = struct_serializer(">h", bytes=2)
"**signed 16bit integer - big endian**"

int16_LE: Serializer[int] = struct_serializer("<h", bytes=2)
"**signed 16bit integer - little endian**"

int16 = int16_BE
"**signed 16bit integer - big endian**"

int8: Serializer[int] = struct_serializer("b", bytes=1)
"**signed 8bit integer**"


float64_BE: Serializer[float] = struct_serializer(">d", bytes=8)
"**64bit float - big endian**"

float64_LE: Serializer[float] = struct_serializer("<d", bytes=8)
"**64bit float - little endian**"

float64 = float64_BE
"**64bit float - big endian**"

float32_BE: Serializer[float] = struct_serializer(">f", bytes=4)
"**32bit float - big endian**"

float32_LE: Serializer[float] = struct_serializer("<f", bytes=4)
"**32bit float - little endian**"

float32 = float32_BE
"**32bit float - big endian**"

