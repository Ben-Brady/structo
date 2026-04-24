import math
import sys
import random
from dataclasses import dataclass
from utils import test

import struct
import pytest
import structo as st


@dataclass
class FloatDescriptor:
    size: int
    serializer: st.Serializer
    struct_format: str


float_descriptors: list[FloatDescriptor] = []


def declare_float(serializer: st.Serializer, *, format: str, size: int):
    float_descriptors.append(
        FloatDescriptor(size=size, serializer=serializer, struct_format=format)
    )


declare_float(st.float32, format="<f", size=4)
declare_float(st.float32_LE, format="<f", size=4)
declare_float(st.float32_BE, format=">f", size=4)
declare_float(st.float64, format="<d", size=8)
declare_float(st.float64_LE, format="<d", size=8)
declare_float(st.float64_BE, format=">d", size=8)


float_ids = [type(d.serializer).__name__ for d in float_descriptors]


@test("Floats: Encodes to specification")
@pytest.mark.parametrize("descriptor", float_descriptors, ids=float_ids)
def _(descriptor: FloatDescriptor):
    serializer = descriptor.serializer
    struct_format = descriptor.struct_format

    def perform_test(value: float):
        expected_bytes = struct.pack(struct_format, value)
        actual_bytes = serializer.to_bytes(value)
        assert (
            expected_bytes == actual_bytes
        ), f"Did not encode same as oracle: {struct_format} value={value}"
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


@test("Float: invalid size")
@pytest.mark.parametrize("descriptor", float_descriptors, ids=float_ids)
def _(descriptor: FloatDescriptor):
    size = descriptor.size
    serializer = descriptor.serializer

    serializer.from_bytes(bytes(size))
    with pytest.raises(Exception):
        serializer.from_bytes(bytes(size - 1))
    with pytest.raises(Exception):
        serializer.from_bytes(bytes(size + 1))
