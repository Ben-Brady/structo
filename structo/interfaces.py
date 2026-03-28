import io
import typing as t


class Serializable:
    @classmethod
    def serializer(cls) -> Serializer[t.Self]: ...

    @classmethod
    def sizeof(cls) -> int | None:
        return cls.serializer().sizeof()

    def write(self, f: t.IO[bytes]):
        return self.serializer().write(f, self)

    @classmethod
    def read(cls, f: t.IO[bytes]) -> t.Self:
        return cls.serializer().read(f)

    def to_bytes(self) -> bytes:
        return self.serializer().to_bytes(self)

    @classmethod
    def from_bytes(cls, data: bytes) -> t.Self:
        return cls.serializer().from_bytes(data)


class Serializer[T]:
    def sizeof(self) -> int | None:
        return None

    def write(self, f: t.IO[bytes], value: T):
        raise NotImplementedError(f"{type(self).__name__} can't be serialized")

    def read(self, f: t.IO[bytes]) -> T:
        raise NotImplementedError(f"{type(self).__name__} can't be deserialized")

    def to_bytes(self, value: T) -> bytes:
        buf = io.BytesIO()
        self.write(buf, value)
        buf.seek(0)
        return buf.getvalue()

    def from_bytes(self, data: bytes) -> T:
        buf = io.BytesIO(data)
        value = self.read(buf)
        assert buf.tell() == len(data), f"expected {buf.tell()} bytes, received {len(data)} bytes"
        return value
