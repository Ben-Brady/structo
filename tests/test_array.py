import typing as t
import structo as st
from utils import test
import pytest


@test("Array: sizeof")
def _():
    assert st.Array(st.i8, 4).sizeof() == 4


@test("Array: PackedInts")
def _():
    class Bits(st.PackedBits):
        a: t.Annotated[int, st.Bits(bits=2)]

    class Object(st.Struct):
        bits: t.Annotated[list[Bits], st.Array(Bits, 2)]

    obj = Object(bits=[Bits(a=1), Bits(a=2)])
    assert obj == Object.from_bytes(obj.to_bytes())


@test("Array: regular example")
def _():
    class Foo(st.Struct):
        a: t.Annotated[list[int], st.Array(st.u8, 3)]

    obj = Foo(a=[1, 2, 3])
    assert obj == Foo.from_bytes(obj.to_bytes())


@test("Array: too little values")
def _():
    class Foo(st.Struct):
        a: t.Annotated[list[int], st.Array(st.u8, length=3)]

    with pytest.raises(Exception):
        Foo(a=[1, 2]).to_bytes()


@test("Array: too many values")
def _():
    class Foo(st.Struct):
        a: t.Annotated[list[int], st.Array(st.u8, length=3)]

    with pytest.raises(Exception):
        Foo(a=[1, 2, 3, 4]).to_bytes()
