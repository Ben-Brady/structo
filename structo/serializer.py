import io
import typing as t


class Serialiable:
    @classmethod
    def serializer(cls) -> Serializer[t.Self]: ...


class Serializer[T]:
    def sizeof(self) -> int | None:
        return None

    def write(self, buf: io.Writer, value: T): ...

    def read(self, buf: io.Reader) -> T: ...

    def to_bytes(self, value: T) -> bytes:
        buf = io.BytesIO()
        self.write(buf, value)
        buf.seek(0)
        return buf.getvalue()

    def from_bytes(self, data: bytes) -> T:
        buf = io.BytesIO(data)
        return self.read(buf)
