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
| `structo.u8`     | 1     | 0 to 255    | None       |
| `structo.u16`    | 2     | 0 to 65.5k  | little     |
| `structo.u16_LE` | 2     | 0 to 65.5k  | little     |
| `structo.u16_BE` | 2     | 0 to 65.5k  | big        |
| `structo.u32`    | 4     | 0 to 4.2B   | little     |
| `structo.u32_LE` | 4     | 0 to 4.2B   | little     |
| `structo.u32_BE` | 4     | 0 to 4.2B   | big        |
| `structo.u64`    | 8     | 0 to 1.8e19 | little     |
| `structo.u64_LE` | 8     | 0 to 1.8e19 | little     |
| `structo.u64_BE` | 8     | 0 to 1.8e19 | big        |

## Signed Integers

Signed integers allow negative values and are stored as
[two's compliment](https://en.wikipedia.org/wiki/Two's_complement).


| Type               | Bytes | Range           | Endianness |
| ------------------ | ----- | --------------- | ---------- |
| `structo.i8`     | 1     | -128 to 127     | None       |
| `structo.i16`    | 2     | -32.7k to 32.7k | little     |
| `structo.i16_LE` | 2     | -32.7k to 32.7k | little     |
| `structo.i16_BE` | 2     | -32.7k to 32.7k | big        |
| `structo.i32`    | 4     | -2.1B to 2.1B   | little     |
| `structo.i32_LE` | 4     | -2.1B to 2.1B   | little     |
| `structo.i32_BE` | 4     | -2.1B to 2.1B   | big        |
| `structo.i64`    | 8     | -9e18 to 9e18   | little     |
| `structo.i64_LE` | 8     | -9e18 to 9e18   | little     |
| `structo.i64_BE` | 8     | -9e18 to 9e18   | big        |

## Floats

| Type                  | Bytes | Endianness |
| --------------------- | ----- | ---------- |
| `structo.f32`     | 4     | little     |
| `structo.f32_LE`  | 4     | little     |
| `structo.f32_BE`  | 4     | big        |
| `structo.f64`     | 8     | little     |
| `structo.f64_LE`  | 8     | little     |
| `structo.f64_BE`  | 8     | big        |
