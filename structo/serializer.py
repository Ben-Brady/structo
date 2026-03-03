import typing as t
import io

type Format = type | t.TypeAliasType


class Serializer[T]:
    def length(self, format: Format) -> int | None:
        return None

    def write(self, buf: io.Writer, format: Format, value: T): ...

    def read(self, buf: io.Reader, format: Format) -> T: ...
