# Buffer

A fixed length of atritrary bytes

## Examples

```py
foo: Buffer(100) # The next 100 bytes

class Chunk(SerializableObject):
    chunk_id: Annotated[int, uint32_LE]
    checksum: Annotated[bytes, Buffer(8)]
    data: Annotated[bytes, Buffer(4096 - 8 - 4)]
```
