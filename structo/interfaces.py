import io
import types
import typing as t


class Serializable:

    @classmethod
    def serializer(cls) -> Serializer[t.Self]:
        raise NotImplementedError(f"serializer() not implemented for {cls}")

    _serializer: types.EllipsisType | Serializer[t.Self] = ...

    @classmethod
    def _cached_serializer(cls) -> Serializer[t.Self]:
        if cls._serializer is ...:
            cls._serializer = cls.serializer()

        return cls._serializer

    @classmethod
    def sizeof(cls) -> int | None:
        return cls._cached_serializer().sizeof()

    def write(self, f: t.IO[bytes]):
        return self._cached_serializer().write(f, self)

    @classmethod
    def read(cls, f: t.IO[bytes]) -> t.Self:
        return cls._cached_serializer().read(f)

    def to_bytes(self) -> bytes:
        return self._cached_serializer().to_bytes(self)

    @classmethod
    def from_bytes(cls, data: bytes) -> t.Self:
        return cls._cached_serializer().from_bytes(data)


class Serializer[T]:
    def sizeof(self) -> int | None:
        return None

    def write(self, f: t.IO[bytes], value: T):
        "Writes a value"
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

        all_read = buf.tell()
        if all_read != len(data):
            # TODO: Test
            raise ValueError(f"{len(data) - all_read} bytes left unread")

        return value
