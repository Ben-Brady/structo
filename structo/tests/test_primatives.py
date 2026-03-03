import typing as t
from dataclasses import dataclass

import pytest
import structo as st
from structo import (
    SerializableObject,
    deserialize_from_bytes,
    uint16,
    uint16_LE,
    uint16_BE,
    serialize_to_bytes,
)
from utils import assert_serialises_correctly, assert_equal


testdata: list[tuple[st.Format, t.Any, bytes]] = []


@dataclass
class EncodeTests[T]:
    datatype: st.Format
    tests: list[tuple[T, bytes]]


testdata.append((st.Literal[b"foo"], b"foo", b"foo"))

testsets: list[EncodeTests] = [
    EncodeTests(
        datatype=st.uint8,
        tests=[
            (1, bytes([1])),
            (100, bytes([100])),
            (255, bytes([255])),
        ],
    ),
    EncodeTests(
        datatype=st.Literal,
        tests=[
            (1, bytes([1])),
            (100, bytes([100])),
            (255, bytes([255])),
        ],
    ),
]

for testset in testsets:
    for value, expected in testset.tests:
        testdata.append((testset.datatype, value, expected))


@dataclass
class BinaryEncodeTests[T]:
    tests: list[tuple[T, bytes]]
    le: st.Format
    be: st.Format
    be_default: st.Format


binary_testsets: list[BinaryEncodeTests] = [
    BinaryEncodeTests(
        le=st.uint16_LE,
        be=st.uint16_BE,
        be_default=st.uint16,
        tests=[
            (1, bytes([0, 1])),
            ((256 * 2) + 1, bytes([2, 1])),
        ],
    ),
    BinaryEncodeTests(
        le=st.uint32_LE,
        be=st.uint32_BE,
        be_default=st.uint32,
        tests=[
            (1, bytes([0, 0, 0, 1])),
            ((2 << 8) + 1, bytes([0, 0, 2, 1])),
            ((3 << 16) + (2 << 8) + 1, bytes([0, 3, 2, 1])),
            ((4 << 24) + (3 << 16) + (2 << 8) + 1, bytes([4, 3, 2, 1])),
        ],
    ),
    BinaryEncodeTests(
        le=st.uint64_LE,
        be=st.uint64_BE,
        be_default=st.uint64,
        tests=[
            (1, bytes([0, 0, 0, 0, 0, 0, 0, 1])),
            ((3 << 16) + (2 << 8) + 1, bytes([0, 0, 0, 0, 3, 2, 1])),
            ((1 << 48) + 1, bytes([1, 0, 0, 0, 0, 0, 0, 1])),
        ],
    ),
]

for testset in binary_testsets:
    for value, expected in testset.tests:
        testdata.append((testset.be, value, expected))
        testdata.append((testset.be_default, value, expected))
        testdata.append((testset.le, value, bytes(reversed(expected))))


@pytest.mark.parametrize("datatype,value,expected", testdata)
def test_encode_primitives(datatype, value, expected):
    actual = serialize_to_bytes(datatype, value)
    assert (
        actual == expected
    ), f"{datatype} {value=} | expected {expected}, recieved {actual}"
