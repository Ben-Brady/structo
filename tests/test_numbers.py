import math
import sys
import random
from dataclasses import dataclass
from utils import test

import struct
import pytest
import structo as st


@dataclass
class IntDescriptor:
    size: int
    serializer: st.Serializer
    struct_format: str
    value_range: tuple[int, int]


int_descriptors: list[IntDescriptor] = []


def declare_int(serializer: st.Serializer, *,
                format: str,
                range: tuple[int, int], size: int,):
    int_descriptors.append(IntDescriptor(
        size, serializer, format, range))


declare_int(st.uint8, format="B", range=(0, 255), size=1)

declare_int(st.uint16, format="<H", range=(0, 65_535), size=2)
declare_int(st.uint16_LE, format="<H", range=(0, 65_535), size=2)
declare_int(st.uint16_BE, format=">H", range=(0, 65_535), size=2)

declare_int(st.uint32, format="<I", range=(0, 4_294_967_295), size=4)
declare_int(st.uint32_LE, format="<I", range=(0, 4_294_967_295), size=4)
declare_int(st.uint32_BE, format=">I", range=(0, 4_294_967_295), size=4)

declare_int(st.uint64, format="<Q", range=(
    0, 18_446_744_073_709_551_615), size=8)
declare_int(st.uint64_LE, format="<Q", range=(
    0, 18_446_744_073_709_551_615), size=8)
declare_int(st.uint64_BE, format=">Q", range=(
    0, 18_446_744_073_709_551_615), size=8)

declare_int(st.int8, format="b", range=(-128, 127), size=1)

declare_int(st.int16, format="<h", range=(-32_768, 32_767), size=2)
declare_int(st.int16_LE, format="<h", range=(-32_768, 32_767), size=2)
declare_int(st.int16_BE, format=">h", range=(-32_768, 32_767), size=2)

declare_int(st.int32, format="<i",
            range=(-2_147_483_648, 2_147_483_647), size=4)
declare_int(st.int32_LE, format="<i",
            range=(-2_147_483_648, 2_147_483_647), size=4)
declare_int(st.int32_BE, format=">i",
            range=(-2_147_483_648, 2_147_483_647), size=4)

declare_int(
    st.int64,
    format="<q",
    range=(-9_223_372_036_854_775_808, 9_223_372_036_854_775_807),
    size=8
)
declare_int(
    st.int64_LE,
    format="<q",
    range=(-9_223_372_036_854_775_808, 9_223_372_036_854_775_807),
    size=8
)
declare_int(
    st.int64_BE,
    format=">q",
    range=(-9_223_372_036_854_775_808, 9_223_372_036_854_775_807),
    size=8
)


@dataclass
class FloatDescriptor:
    size: int
    serializer: st.Serializer
    struct_format: str


float_descriptors: list[FloatDescriptor] = []


def declare_float(serializer: st.Serializer, *,
                  format: str, size: int):
    float_descriptors.append(FloatDescriptor(
        size=size,
        serializer=serializer,
        struct_format=format
    ))


declare_float(st.float32, format="<f", size=4)
declare_float(st.float32_LE, format="<f", size=4)
declare_float(st.float32_BE, format=">f", size=4)
declare_float(st.float64, format="<d", size=8)
declare_float(st.float64_LE, format="<d", size=8)
declare_float(st.float64_BE, format=">d", size=8)


int_ids = [type(d.serializer).__name__ for d in int_descriptors]
float_ids = [type(d.serializer).__name__ for d in float_descriptors]


@test("Ints: Encodes to specification")
@pytest.mark.parametrize("descriptor", int_descriptors, ids=int_ids)
def _(descriptor: IntDescriptor):
    struct_format = descriptor.struct_format
    serializer = descriptor.serializer
    min_value, max_value = descriptor.value_range

    def perform_test(value: int):
        expected_bytes = struct.pack(struct_format, value)
        actual_bytes = serializer.to_bytes(value)
        assert expected_bytes == actual_bytes, (
            f"Did not encode same as oracle: {struct_format} value={value}"
        )
        decoded_value = serializer.from_bytes(actual_bytes)
        assert value == decoded_value

    perform_test(min_value)
    perform_test(max_value)

    with pytest.raises(Exception):
        serializer.to_bytes(min_value - 1)
    with pytest.raises(Exception):
        serializer.to_bytes(max_value + 1)

    for _ in range(1000):
        value = random.randint(min_value, max_value)
        perform_test(value)


@test("Floats: Encodes to specification")
@pytest.mark.parametrize("descriptor", float_descriptors, ids=float_ids)
def _(descriptor: FloatDescriptor):
    serializer = descriptor.serializer
    struct_format = descriptor.struct_format

    def perform_test(value: float):
        expected_bytes = struct.pack(struct_format, value)
        actual_bytes = serializer.to_bytes(value)
        assert expected_bytes == actual_bytes, (
            f"Did not encode same as oracle: {struct_format} value={value}"
        )
        decoded_value = serializer.from_bytes(actual_bytes)

        is_equal = value == decoded_value
        is_close = math.isclose(value, decoded_value, rel_tol=1e-7)
        is_both_nan = math.isnan(value) and math.isnan(decoded_value)
        is_both_inf = math.isinf(value) and math.isinf(decoded_value)
        assert is_equal or is_close or is_both_nan or is_both_inf

    perform_test(float("inf"))
    perform_test(float("-inf"))
    perform_test(float("nan"))
    perform_test(float("-nan"))

    for _ in range(1000):
        perform_test(random.random())


@test("Number: invalid size")
@pytest.mark.parametrize("descriptor", [*int_descriptors, *float_descriptors], ids=[*int_ids, *float_ids])
def _(descriptor: FloatDescriptor | IntDescriptor):
    size = descriptor.size
    serializer = descriptor.serializer


    serializer.from_bytes(bytes(size))
    with pytest.raises(Exception):
        serializer.from_bytes(bytes(size - 1))
    with pytest.raises(Exception):
        serializer.from_bytes(bytes(size + 1))
