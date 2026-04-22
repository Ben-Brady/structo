import typing as t
from .ints import uint32_LE
from ..interfaces import Serializer

NULL = bytes([0])


class CString(Serializer[bytes]):
    "A null terminated C string"

    def write(self, f, value):
        assert NULL not in value, f"Data encoded as a C String cannot include null, NULL found at value[{value.index(NULL)}]"

        f.write(value)
        f.write(NULL)

    def read(self, f):
        data = bytearray()
        while True:
            char = f.read(1)
            if char == NULL:
                return data
            else:
                data.append(char[0])
