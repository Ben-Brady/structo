from structo import uint16_LE, uint32_LE, SerializableObject, Literal


class RiffHeader(SerializableObject):
    chunk_id: Literal[b"RIFF"]
    chunk_size: uint32_LE
    format: Literal[b"WAVE"]


class FormatChunkHeader(SerializableObject):
    id: Literal[b"fmt "]
    size: uint32_LE


class DataChunkHeader(SerializableObject):
    id: Literal[b"data"]
    size: uint32_LE


class WavFormat(SerializableObject):
    audio_format: uint16_LE
    num_channels: uint16_LE
    sample_rate: uint32_LE
    byte_range: uint32_LE
    block_align: uint16_LE
    bits_per_sample: uint16_LE


with open("example.wav", "rb") as f:
    RiffHeader.read(f)

    format_header = FormatChunkHeader.read(f)
    format_data = f.read(format_header.size)
    format = WavFormat.from_bytes(format_data)

    data_header = DataChunkHeader.read(f)
    wav_data = f.read(data_header.size)

print(format)
print(len(wav_data))
