# Number Types

## Endianness

Multi-byte integers have a big endian (`_BE`) and a little endiant (`_LE`) for their different
[endianness](https://en.wikipedia.org/wiki/Endianness). This determines the order the bytes
are stored. If omitted, Little Endian is used

Modern applications should use **little endian**, however lots of file formats and network
protocols use **big endian**. Make sure to double check when implementing a protocol.

## Unsigned Integers

Unsigned integers can only be positive.

| Type                | Bytes | Range       | Endianness |
| ------------------- | ----- | ----------- | ---------- |
| `structo.uint8`     | 1     | 0 to 255    | None       |
| `structo.uint16`    | 2     | 0 to 65.5k  | little     |
| `structo.uint16_LE` | 2     | 0 to 65.5k  | little     |
| `structo.uint16_BE` | 2     | 0 to 65.5k  | big        |
| `structo.uint32`    | 4     | 0 to 4.2B   | little     |
| `structo.uint32_LE` | 4     | 0 to 4.2B   | little     |
| `structo.uint32_BE` | 4     | 0 to 4.2B   | big        |
| `structo.uint64`    | 8     | 0 to 1.8e19 | little     |
| `structo.uint64_LE` | 8     | 0 to 1.8e19 | little     |
| `structo.uint64_BE` | 8     | 0 to 1.8e19 | big        |

## Signed Integers

Signed integers allow negative values and are stored as
[two's compliment](https://en.wikipedia.org/wiki/Two's_complement).


| Type               | Bytes | Range           | Endianness |
| ------------------ | ----- | --------------- | ---------- |
| `structo.int8`     | 1     | -128 to 127     | None       |
| `structo.int16`    | 2     | -32.7k to 32.7k | little     |
| `structo.int16_LE` | 2     | -32.7k to 32.7k | little     |
| `structo.int16_BE` | 2     | -32.7k to 32.7k | big        |
| `structo.int32`    | 4     | -2.1B to 2.1B   | little     |
| `structo.int32_LE` | 4     | -2.1B to 2.1B   | little     |
| `structo.int32_BE` | 4     | -2.1B to 2.1B   | big        |
| `structo.int64`    | 8     | -9e18 to 9e18   | little     |
| `structo.int64_LE` | 8     | -9e18 to 9e18   | little     |
| `structo.int64_BE` | 8     | -9e18 to 9e18   | big        |

## Floats

| Type                  | Bytes | Endianness |
| --------------------- | ----- | ---------- |
| `structo.float32`     | 4     | little     |
| `structo.float32_LE`  | 4     | little     |
| `structo.float32_BE`  | 4     | big        |
| `structo.float64`     | 8     | little     |
| `structo.float64_LE`  | 8     | little     |
| `structo.float64_BE`  | 8     | big        |
