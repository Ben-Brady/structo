from typing import Annotated
from structo import uint16_LE, uint32_LE, SerializableObject, Literal


class WavHeader(SerializableObject):
    chunk_id: Annotated[bytes, Literal(b"RIFF")]
    chunk_size: Annotated[int, uint32_LE]
    format: Annotated[bytes, Literal(b"WAVE")]


class ChunkHeader(SerializableObject):
    id: Annotated[bytes, Literal(b"fmt ", b"data")]
    size: Annotated[int, uint32_LE]


class WavFormat(SerializableObject):
    audio_format: Annotated[int, uint16_LE]
    num_channels: Annotated[int, uint16_LE]
    sample_rate: Annotated[int, uint32_LE]
    byte_range: Annotated[int, uint32_LE]
    block_align: Annotated[int, uint16_LE]
    bits_per_sample: Annotated[int, uint16_LE]


with open("example.wav", "rb") as f:
    WavHeader.read(f)

    format_header = ChunkHeader.read(f)
    assert format_header.id == b'fmt '

    format_data = f.read(format_header.size)
    format = WavFormat.from_bytes(format_data)

    data_header = ChunkHeader.read(f)
    assert data_header.id == b"data"
    wav_data = f.read(data_header.size)

print(format)
print(len(wav_data))
