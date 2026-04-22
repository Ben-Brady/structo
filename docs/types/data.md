# Types

## `Blob`

A dynamically set of bytes that is prefixed with it's length

### `Blob` Examples

```py
Blob(uint32_LE) # Blob with length stored as a uint32
```

## `Buffer`

A fixed length of atritrary bytes.

### `Buffer` Examples

```py
foo: Buffer(100) # The next 100 bytes

class Chunk(SerializableObject):
    chunk_id: Annotated[int, uint32_LE]
    checksum: Annotated[bytes, Buffer(8)]
    data: Annotated[bytes, Buffer(4096 - 8 - 4)]
```

::: structo.Buffer
