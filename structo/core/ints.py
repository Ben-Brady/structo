import typing as t
from ..interfaces import Serializer


class Int(Serializer[int]):
    __slots__ = ("bytes", "byteorder", "signed")
    bytes: int
    byteorder: t.Literal["little", "big"]
    signed: bool

    def __init__(
        self,
        bytes: int,
        byteorder: t.Literal["little", "big"],
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
            length=self.bytes, byteorder=self.byteorder, signed=self.signed
        )
        return f.write(data)

    def read(self, f):
        data = f.read(self.bytes)
        assert len(data) == self.bytes, f"Expected {self.bytes} bytes"

        if len(data) != self.bytes:
            raise ValueError(
                f"expected data with length {self.bytes}, "  # ------------
                f"received {len(data)}"
            )

        return int.from_bytes(data, byteorder=self.byteorder, signed=self.signed)


type u64 = t.Annotated[int, Int(bytes=8, byteorder="little", signed=False)]
"**unsigned 64bit integer - little endian**"
type u64_LE = t.Annotated[int, Int(bytes=8, byteorder="little", signed=False)]
"**unsigned 64bit integer - little endian**"
type u64_BE = t.Annotated[int, Int(bytes=8, byteorder="big", signed=False)]
"**unsigned 64bit integer - big endian**"


type u32 = t.Annotated[int, Int(bytes=4, byteorder="little", signed=False)]
"**unsigned 32bit integer - little endian**"
type u32_LE = t.Annotated[int, Int(bytes=4, byteorder="little", signed=False)]
"**unsigned 32bit integer - little endian**"
type u32_BE = t.Annotated[int, Int(bytes=4, byteorder="big", signed=False)]
"**unsigned 32bit integer - big endian**"


type u16 = t.Annotated[int, Int(bytes=2, byteorder="little", signed=False)]
"**unsigned 16bit integer - little endian**"
type u16_LE = t.Annotated[int, Int(bytes=2, byteorder="little", signed=False)]
"**unsigned 16bit integer - little endian**"
type u16_BE = t.Annotated[int, Int(bytes=2, byteorder="big", signed=False)]
"**unsigned 16bit integer - big endian**"

type u8 = t.Annotated[int, Int(bytes=1, byteorder="big", signed=False)]
"**unsigned 8bit integer**"


type i64 = t.Annotated[int, Int(bytes=8, byteorder="little", signed=True)]
"**signed 64bit integer - little endian**"
type i64_LE = t.Annotated[int, Int(bytes=8, byteorder="little", signed=True)]
"**signed 64bit integer - little endian**"
type i64_BE = t.Annotated[int, Int(bytes=8, byteorder="big", signed=True)]
"**signed 64bit integer - big endian**"


type i32 = t.Annotated[int, Int(bytes=4, byteorder="little", signed=True)]
"**signed 32bit integer - little endian**"
type i32_LE = t.Annotated[int, Int(bytes=4, byteorder="little", signed=True)]
"**signed 32bit integer - little endian**"
type i32_BE = t.Annotated[int, Int(bytes=4, byteorder="big", signed=True)]
"**signed 32bit integer - big endian**"


type i16 = t.Annotated[int, Int(bytes=2, byteorder="little", signed=True)]
"**signed 16bit integer - little endian**"
type i16_LE = t.Annotated[int, Int(bytes=2, byteorder="little", signed=True)]
"**signed 16bit integer - little endian**"
type i16_BE = t.Annotated[int, Int(bytes=2, byteorder="big", signed=True)]
"**signed 16bit integer - big endian**"


type i8 = t.Annotated[int, Int(bytes=1, byteorder="little", signed=True)]
"**signed 8bit integer**"
