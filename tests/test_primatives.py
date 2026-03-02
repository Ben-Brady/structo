from structo import SerialiableObject, deserialize_from_bytes, uint16, uint16_LE, uint16_BE, serialize_to_bytes
import structo as st
from utils import assert_serialises_correctly, assert_equal

tests = {
    st.uint16_LE: [
        (1, bytes([1, 0])),
        ((256 * 2) + 1, bytes([1, 2]))
    ],
    st.uint16_BE: [
        (1, bytes([0, 1])),
        ((256 * 2) + 1, bytes([2, 1]))
    ]
}

def test_encode_primitives():
    for datatype in tests.keys():
        for value, expected in tests[datatype]:
            actual = serialize_to_bytes(datatype, value)
            assert actual == expected, f"{datatype=} {value=} | expected {expected}, recieved {actual}"
