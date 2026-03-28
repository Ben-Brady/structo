from typing import Annotated
from structo import Serializer, Serializable, Struct, String
from dataclasses import dataclass


@dataclass
class UserFlags(Serializable):
    is_alive: bool
    is_banned: bool
    is_admin: bool

    @classmethod
    def serializer(cls):
        return UserFlagsSerializer()


class UserFlagsSerializer(Serializer[UserFlags]):
    def write(self, f, value):
        byte = (
            int(value.is_alive) << 0 |
            int(value.is_admin) << 1 |
            int(value.is_banned) << 2
        )
        f.write(bytes([byte]))

    def read(self, f):
        byte = f.read(1)[0]
        return UserFlags(
            is_alive=((byte >> 0) & 1) == 1,
            is_admin=((byte >> 1) & 1) == 1,
            is_banned=((byte >> 2) & 1) == 1
        )


class User(Struct):
    name: Annotated[str, String()]
    flags: UserFlags
