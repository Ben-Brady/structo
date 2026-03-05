import typing as t
import io
from . import (
    uint8,
    uint16,
    uint32,
    uint64,
    int8,
    int16,
    int32,
    int64,
    float32,
    float64,
)
from .serializer import Serializer


class StructoReader:
    reader: io.Reader

    def __init__(self, reader: io.Reader) -> None:
        self.reader = reader

    def read(self, format: Serializer) -> t.Any:
        return format.read(self.reader)

    def read_uint8(self) -> int:
        return self.read(uint8)

    def read_uint16(self) -> int:
        return self.read(uint16)

    def read_uint32(self) -> int:
        return self.read(uint32)

    def read_uint64(self) -> int:
        return self.read(uint64)

    def read_int8(self) -> int:
        return self.read(int8)

    def read_int16(self) -> int:
        return self.read(int16)

    def read_int32(self) -> int:
        return self.read(int32)

    def read_int64(self) -> int:
        return self.read(int64)

    def read_float32(self) -> float:
        return self.read(float32)

    def read_float64(self) -> float:
        return self.read(float64)


class StructifyWriter:
    buf: io.Writer

    def __init__(self, buf: io.Writer) -> None:
        self.buf = buf

    def write(self, format: Serializer, value: t.Any) -> t.Any:
        format.write(self.buf, value)

    def write_uint8(self, value: int):
        return self.write(uint8, value)

    def write_uint16(self, value: int):
        return self.write(uint16, value)

    def write_uint32(self, value: int):
        return self.write(uint32, value)

    def write_uint64(self, value: int):
        return self.write(uint64, value)

    def write_int8(self, value: int):
        return self.write(int8, value)

    def write_int16(self, value: int):
        return self.write(int16, value)

    def write_int32(self, value: int):
        return self.write(int32, value)

    def write_int64(self, value: int):
        return self.write(int64, value)

    def write_float32(self, value: float):
        return self.write(float32, value)

    def write_float64(self, value: float):
        return self.write(float64, value)
