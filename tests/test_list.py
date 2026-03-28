from utils import test
import typing as t

import pytest
import structo as st


@test("List: regular example")
def _():
    class Foo(st.Struct):
        a: t.Annotated[list[int], st.List(st.uint8)]

    obj = Foo(a=[1, 2, 3])
    assert obj == Foo.from_bytes(obj.to_bytes())


@test("List: over max size")
def _():
    class Foo(st.Struct):
        a: t.Annotated[list[int], st.List(st.uint8, length=st.uint8)]
    with pytest.raises(Exception):
        Foo(a=[1] * 300).to_bytes()


@test("List: nested bits")
def _():
    class Bits(st.PackedBits):
        a: t.Annotated[int, st.Bits(bits=2)]

    class Object(st.Struct):
        foo: t.Annotated[list[Bits], st.List(Bits)]

    obj = Object(foo=[Bits(a=1)])
    assert obj == Object.from_bytes(obj.to_bytes())
