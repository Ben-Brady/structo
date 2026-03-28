import typing as t
from structo import uint16_LE, uint32_LE, Struct, Literal, Buffer


class WavHeader(Struct):
    chunk_id: t.Annotated[str, Literal(b"RIFF")]
    file_size: t.Annotated[int, uint32_LE]
    format: t.Annotated[str, Literal(b"WAVE")]


class ChunkHeader(Struct):
    id: t.Annotated[str, Buffer(4)]
    size: t.Annotated[int, uint32_LE]


class WavInfoChunk(Struct):
    audio_format: t.Annotated[int, uint16_LE]
    num_channels: t.Annotated[int, uint16_LE]
    sample_rate: t.Annotated[int, uint32_LE]
    byte_range: t.Annotated[int, uint32_LE]
    block_align: t.Annotated[int, uint16_LE]
    bits_per_sample: t.Annotated[int, uint16_LE]


def read_wav_file(f: t.IO) -> tuple[WavInfoChunk, bytes]:
    format_header = ChunkHeader.read(f)
    assert format_header.id == b"fmt "

    format_data = f.read(format_header.size)
    format = WavInfoChunk.from_bytes(format_data)

    data_header = ChunkHeader.read(f)
    assert data_header.id == b"data"
    wav_data = f.read(data_header.size)
    return format, wav_data
