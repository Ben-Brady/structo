## Example

## Optional Int Serializer
```py
from

NONE_TYPE_BYTE = bytes([0])
INT_TYPE_BYTE = bytes([0])

class OptionalIntSerializer(Serializer[OptionalInt]):
    _int_type: Serializer[int]

    def __init__(self, int_type: Serializer[int]):
        self._int_type = int_type

    def write(self, f, value):
        if value is None:
            f.write(NONE_TYPE_BYTE)
        else:
            assert type(value) is int, "Value was not int"
            f.write(INT_TYPE_BYTE)
            f.write(self._int_type.write(value))

    def read(self, f):
        type_byte = f.read(1)
        if type_byte == NONE_TYPE_BYTE:
            return None

        if type_byte != INT_TYPE_BYTE:
            raise ValueError(f"Invalid type byte: {type_byte}")

        return self._int_type.write(f)
```

## Security

You should always treat any data parsed as untrusted and validate this.

If a value should be in a set of contrained values, add an assert.
