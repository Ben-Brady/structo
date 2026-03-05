from typing import Annotated
import structo as st
import pytest
from utils import test


@test("sizeof(primatives): single parameter")
@pytest.mark.parametrize(
    "datatype,length",
    [
        (st.uint8, 1),
        (st.uint16, 2),
        (st.uint32, 4),
        (st.uint64, 8),
        (st.int8, 1),
        (st.int16, 2),
        (st.int32, 4),
        (st.int64, 8),
        (st.float32, 4),
        (st.float64, 8),
    ],
)
def _(datatype: st.Serializer, length: int):
    assert datatype.sizeof() == length


@test("sizeof(SerializableObject): single parameter")
def _():
    class Foo(st.SerializableObject):
        bar: Annotated[int, st.uint32_BE]

    assert Foo.sizeof() == 4


@test("sizeof(SerializableObject): two arguemnts")
def _():
    class Foo(st.SerializableObject):
        foo: Annotated[int, st.uint32_BE]
        bar: Annotated[int, st.uint32_BE]

    assert Foo.sizeof() == 8


@test("sizeof(SerializableObject): mixed arguments")
def _():
    class Foo(st.SerializableObject):
        a: Annotated[int, st.uint32_BE]
        b: Annotated[int, st.uint8]
        c: Annotated[bytes, st.Buffer(100)]

    assert Foo.sizeof() == 4 + 1 + 100


@test("sizeof(SerializableObject): unknownable")
def _():
    class Foo(st.SerializableObject):
        a: Annotated[str, st.String(st.uint8)]

    assert Foo.sizeof() is None


@test("sizeof(SerializableObject): unknownable mixed")
def _():
    class Foo(st.SerializableObject):
        a: Annotated[int, st.uint8]
        b: Annotated[str, st.String(st.uint8)]

    assert Foo.sizeof() is None
