import struct
import _pylong
_pylong.decimal
from ..interfaces import Serializer


class Float(Serializer[float]):
    format: str
    size: int

    def __init__(self, format: str, size: int) -> None:
        self.format = format
        self.size = size

    def sizeof(self):
        return self.size

    def write(self, f, value):
        data = struct.pack(self.format, value)
        return f.write(data)

    def read(self, f):
        data = f.read(self.size)
        assert len(data) == self.size, f"Expected {self.size} bytes"
        return struct.unpack(self.format, data)[0]


float64: Serializer[float] = Float(format="<d", size=8)
"**64bit float - little endian**"
float64_LE: Serializer[float] = Float(format="<d", size=8)
"**64bit float - little endian**"
float64_BE: Serializer[float] = Float(format=">d", size=8)
"**64bit float - big endian**"


float32: Serializer[float] = Float(format="<f", size=4)
"**32bit float - little endian**"
float32_LE: Serializer[float] = Float(format="<f", size=4)
"**32bit float - little endian**"
float32_BE: Serializer[float] = Float(format=">f", size=4)
"**32bit float - big endian**"
