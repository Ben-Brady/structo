import typing as t
import os
from .numbers import uint32_LE, uint64_LE
from ..interfaces import Serializer


class LazyList[T](Serializer[t.Iterable[T]]):
    "A list of items, prefixed with it's length. Read and saved lazily"

    _value: Serializer[T]
    _LENGTH_TYPE = uint64_LE
    _SIZE_TYPE = uint64_LE

    def __init__(self, value: Serializer[T]) -> None:
        self._value = value

    def write(self, f, value):
        start = f.tell()

        self._LENGTH_TYPE.write(f, 0)
        self._SIZE_TYPE.write(f, 0)

        length = 0
        size = 0
        for item in value:
            data = self._value.to_bytes(item)
            f.write(data)
            length += 1
            size += len(data)

        end = f.tell()

        f.seek(start)
        self._LENGTH_TYPE.write(f, length)
        self._SIZE_TYPE.write(f, size)
        f.seek(end)

    def read(self, f):
        length = self._LENGTH_TYPE.read(f)
        size = self._SIZE_TYPE.read(f)
        next_element = f.tell()
        f.seek(size, 1)  # skip over to continue parsing

        def iter():
            nonlocal next_element
            for _ in range(length):
                f.seek(next_element)
                value = self._value.read(f)
                next_element = f.tell()
                yield value

        return iter()
