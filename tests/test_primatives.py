import typing as t
from dataclasses import dataclass
from utils import test

import pytest
import structo as st


testdata: list[tuple[st.Serializer, t.Any, bytes]] = []


@dataclass
class EncodeTests[T]:
    datatype: st.Serializer
    tests: list[tuple[T, bytes]]


testsets: list[EncodeTests] = [
    EncodeTests(
        datatype=st.uint8,
        tests=[
            (1, bytes([1])),
            (100, bytes([100])),
            (255, bytes([255])),
        ],
    ),
    # EncodeTests(
    #     datatype=st.Literal["b"],
    #     tests=[
    #         (1, bytes([1])),
    #         (100, bytes([100])),
    #         (255, bytes([255])),
    #     ],
    # ),
]

for testset in testsets:
    for value, expected in testset.tests:
        testdata.append((testset.datatype, value, expected))


@dataclass
class BinaryEncodeTests[T]:
    tests: list[tuple[T, bytes]]
    le: st.Serializer
    be: st.Serializer
    be_default: st.Serializer


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
            # ((3 << 16) + (2 << 8) + 1, bytes([0, 3, 2, 1])),
            # ((4 << 24) + (3 << 16) + (2 << 8) + 1, bytes([4, 3, 2, 1])),
        ],
    ),
    BinaryEncodeTests(
        le=st.uint64_LE,
        be=st.uint64_BE,
        be_default=st.uint64,
        tests=[
            (1, bytes([0, 0, 0, 0, 0, 0, 0, 1])),
            # ((3 << 16) + (2 << 8) + 1, bytes([0, 0, 0, 0, 3, 2, 1])),
            # ((1 << 48) + 1, bytes([1, 0, 0, 0, 0, 0, 0, 1])),
        ],
    ),
]

for testset in binary_testsets:
    for value, expected in testset.tests:
        testdata.append((testset.be, value, expected))
        testdata.append((testset.be_default, value, expected))
        testdata.append((testset.le, value, bytes(reversed(expected))))


@test("Encode Decode Test")
@pytest.mark.parametrize("datatype,value,expected", testdata)
def _(datatype: st.Serializer, value, expected):
    actual = datatype.to_bytes(value)
    assert (
        actual == expected
    ), f"{datatype} {value=} | expected {expected}, recieved {actual}"


@test("uint: negative value raises error")
def _():
    with pytest.raises(Exception):
        st.uint8.to_bytes(-1)
