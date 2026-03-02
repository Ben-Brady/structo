"""
Structify
"""

__version__ = "0.0.1"

from .serialise import serialize, deserialize
from .types import (
    SerialiableObject,
    uint8,
    uint16,
    uint32,
    uint64,
    int8,
    int16,
    int32,
    int64,
    float32,
    float64,
    array,
    string,
    blob,
    fixedblob
)
from .utils import (
    StructifyReader,
    StructifyWriter,
    serialize_to_bytes,
    deserialize_from_bytes,
)
