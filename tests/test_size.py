from typing import Annotated
import structo as st
import pytest
from utils import test


@test("sizeof(primatives): single parameter")
@pytest.mark.parametrize(
    "datatype,length",
    [
        (st.u8, 1),
        (st.u16, 2),
        (st.u32, 4),
        (st.u64, 8),
        (st.i8, 1),
        (st.i16, 2),
        (st.i32, 4),
        (st.i64, 8),
        (st.f32, 4),
        (st.f64, 8),
    ],
)
def _(datatype: type, length: int):
    serializer = st.get_serializer(datatype)
    assert serializer.sizeof() == length


@test("sizeof(SerializableObject): single parameter")
def _():
    class Foo(st.Struct):
        bar: st.u32_BE

    assert Foo.sizeof() == 4


@test("sizeof(SerializableObject): two arguemnts")
def _():
    class Foo(st.Struct):
        foo: st.u32_BE
        bar: st.u32_BE

    assert Foo.sizeof() == 8


@test("sizeof(SerializableObject): mixed arguments")
def _():
    class Foo(st.Struct):
        a: st.u32_BE
        b: st.u8
        c: Annotated[bytes, st.Buffer(100)]

    assert Foo.sizeof() == 4 + 1 + 100


@test("sizeof(SerializableObject): unknownable")
def _():
    class Foo(st.Struct):
        a: Annotated[str, st.String(st.u8)]

    assert Foo.sizeof() is None


@test("sizeof(SerializableObject): unknownable mixed")
def _():
    class Foo(st.Struct):
        a: Annotated[int, st.u8]
        b: Annotated[str, st.String(st.u8)]

    assert Foo.sizeof() is None
