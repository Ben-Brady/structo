import typing as t
import struct

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
        if len(data) != self.size:
            raise ValueError(
                f"expected data with length {self.size}, "  # ------------
                f"received {len(data)}"
            )

        return struct.unpack(self.format, data)[0]


type f64 = t.Annotated[float, Float(format="<d", size=8)]
"**64bit float - little endian**"
type f64_LE = t.Annotated[float, Float(format="<d", size=8)]
"**64bit float - little endian**"
type f64_BE = t.Annotated[float, Float(format=">d", size=8)]
"**64bit float - big endian**"


type f32 = t.Annotated[float, Float(format="<f", size=4)]
"**32bit float - little endian**"
type f32_LE = t.Annotated[float, Float(format="<f", size=4)]
"**32bit float - little endian**"
type f32_BE = t.Annotated[float, Float(format=">f", size=4)]
"**32bit float - big endian**"
