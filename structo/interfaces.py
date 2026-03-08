import io
import typing as t


class Serializable:
    @classmethod
    def serializer(cls) -> Serializer[t.Self]: ...

    @classmethod
    def sizeof(cls) -> int | None:
        return cls.serializer().sizeof()

    @classmethod
    def read(cls, f: io.Reader) -> t.Self:
        return cls.serializer().read(f)

    @classmethod
    def from_bytes(cls, data: bytes) -> t.Self:
        return cls.serializer().from_bytes(data)

    def write(self, f: io.Writer):
        return self.serializer().write(f, self)

    def to_bytes(self) -> bytes:
        return self.serializer().to_bytes(self)


class Serializer[T]:
    def sizeof(self) -> int | None:
        return None

    def write(self, buf: io.Writer, value: T):
        raise NotImplementedError(f"{type(self).__name__} can't be serialized")

    def read(self, buf: io.Reader) -> T:
        raise NotImplementedError(f"{type(self).__name__} can't be deserialized")

    def to_bytes(self, value: T) -> bytes:
        buf = io.BytesIO()
        self.write(buf, value)
        buf.seek(0)
        return buf.getvalue()

    def from_bytes(self, data: bytes) -> T:
        buf = io.BytesIO(data)
        return self.read(buf)
