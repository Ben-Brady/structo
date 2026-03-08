# Serializable

In order for classes (such as PackedInts) to be serialiable without having to annotate a serializer, they implement `Serializable`.

This is just means they have a method that returns a serialiazer based on thier class.

```py
class Serializable:
    @classmethod
    def serializer(cls) -> Serializer[t.Self]: ...
```

For example, for Serili
```py
from .serializers import ObjectSerializer

class SerializableObject(Serializable):
    @classmethod
    def serializer(cls) -> Serializer[t.Self]:
        return ObjectSerializer(cls)
```

## Examples

### Basic Serializable

```py
from structo import Serializer, Serializable, SerializableObject
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
            int(value.is_alive)  << 0 +
            int(value.is_admin)  << 1 +
            int(value.is_banned) << 2
        )
        f.write(bytes([byte]))

    def read(self, f):
        byte = f.read(1)[0]
        return UserFlags(
            is_alive  = ((byte >> 0) & 1) == 1,
            is_admin  = ((byte >> 1) & 1) == 1,
            is_banned = ((byte >> 2) & 1) == 1
        )


class User(SerializableObject):
    name: str
    flags: UserFlags

```



Note: in this example you could use a packed ints instead
