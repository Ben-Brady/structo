from structo import Serializer
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
    def write(self, buf, value):
        byte = 0
        if value.flag_a:
            byte += 1 << 0
        if value.flag_b:
            byte += 1 << 1
        if value.flag_c:
            byte += 1 << 2

        byte = buf.write(bytes([byte]))

    def read(self, buf):
        byte = buf.read(1)[0]
        flag_a = ((byte >> 0) & 1) != 0
        flag_b = ((byte >> 1) & 1) != 0
        flag_c = ((byte >> 2) & 1) != 0
        return Flags(
            flag_a=flag_a,
            flag_b=flag_b,
            flag_c=flag_c,
        )

    def sizeof(self):
        return 1


type FlagsDatatype = t.Annotated[Flags, FlagsSerialiser()]


value = Flags(
    flag_a=False,
    flag_b=True,
    flag_c=False,
)
output = FlagsSerialiser().to_bytes(value)
print(output)
print(FlagsSerialiser().from_bytes(output))
