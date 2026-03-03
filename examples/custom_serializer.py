from structo import Serializer, serialize_to_bytes, deserialize_from_bytes
from dataclasses import dataclass
import typing as t

# We don't inherit from SerialiableObject
# since we're using a custom serializer
@dataclass
class Flags:
    flag_a: bool
    flag_b: bool
    flag_c: bool

class FlagsSerialiser(Serializer[Flags]):
    # This is optional, but allows for size calculations
    @staticmethod
    def length(format):
        return 1

    @staticmethod
    def write(buf, format, value):
        byte = 0
        if value.flag_a:
            byte += 1 << 0
        if value.flag_b:
            byte += 1 << 1
        if value.flag_c:
            byte += 1 << 2

        byte = buf.write(bytes([byte]))

    @staticmethod
    def read(buf, format):
        byte = buf.read(1)[0]
        flag_a = ((byte >> 0) & 1) != 0
        flag_b = ((byte >> 1) & 1) != 0
        flag_c = ((byte >> 2) & 1) != 0
        return Flags(
            flag_a=flag_a,
            flag_b=flag_b,
            flag_c=flag_c,
        )

type FlagsDatatype = t.Annotated[Flags, FlagsSerialiser]


value = Flags(
    flag_a=False,
    flag_b=True,
    flag_c=False,
)
output = serialize_to_bytes(flags_datatype, value)
print(output)
print(deserialize_from_bytes(flags_datatype, output))

