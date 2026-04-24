import typing as t
from ..interfaces import Serializer


class Int(Serializer[int]):
    __slots__ = ("bytes", "byteorder", "signed")
    bytes: int
    byteorder: t.Literal['little', 'big']
    signed: bool

    def __init__(
        self,
        bytes: int,
        byteorder: t.Literal['little', 'big'],
        signed: bool,
    ):
        assert bytes > 0, "Can't be zero bytes"
        self.bytes = bytes
        self.byteorder = byteorder
        self.signed = signed

    def sizeof(self):
        return self.bytes

    def write(self, f, value):
        data = value.to_bytes(
            length=self.bytes,
            byteorder=self.byteorder,
            signed=self.signed
        )
        return f.write(data)

    def read(self, f):
        data = f.read(self.bytes)
        assert len(data) == self.bytes, f"Expected {self.bytes} bytes"
        return int.from_bytes(data, byteorder=self.byteorder, signed=self.signed)


uint64 = Int(bytes=8, byteorder="little", signed=False)
"**unsigned 64bit integer - little endian**"
uint64_LE = Int(bytes=8, byteorder="little", signed=False)
"**unsigned 64bit integer - little endian**"
uint64_BE = Int(bytes=8, byteorder="big", signed=False)
"**unsigned 64bit integer - big endian**"


uint32 = Int(bytes=4, byteorder="little", signed=False)
"**unsigned 32bit integer - little endian**"
uint32_LE = Int(bytes=4, byteorder="little", signed=False)
"**unsigned 32bit integer - little endian**"
uint32_BE = Int(bytes=4, byteorder="big", signed=False)
"**unsigned 32bit integer - big endian**"


uint16 = Int(bytes=2, byteorder="little", signed=False)
"**unsigned 16bit integer - little endian**"
uint16_LE = Int(bytes=2, byteorder="little", signed=False)
"**unsigned 16bit integer - little endian**"
uint16_BE = Int(bytes=2, byteorder="big", signed=False)
"**unsigned 16bit integer - big endian**"

uint8 = Int(bytes=1, byteorder="big", signed=False)
"**unsigned 8bit integer**"


int64 = Int(bytes=8, byteorder="little", signed=True)
"**signed 64bit integer - little endian**"
int64_LE = Int(bytes=8, byteorder="little", signed=True)
"**signed 64bit integer - little endian**"
int64_BE = Int(bytes=8, byteorder="big", signed=True)
"**signed 64bit integer - big endian**"


int32 = Int(bytes=4, byteorder="little", signed=True)
"**signed 32bit integer - little endian**"
int32_LE = Int(bytes=4, byteorder="little", signed=True)
"**signed 32bit integer - little endian**"
int32_BE = Int(bytes=4, byteorder="big", signed=True)
"**signed 32bit integer - big endian**"


int16 = Int(bytes=2, byteorder="little", signed=True)
"**signed 16bit integer - little endian**"
int16_LE = Int(bytes=2, byteorder="little", signed=True)
"**signed 16bit integer - little endian**"
int16_BE = Int(bytes=2, byteorder="big", signed=True)
"**signed 16bit integer - big endian**"


int8 = Int(bytes=1, byteorder="little", signed=True)
"**signed 8bit integer**"
