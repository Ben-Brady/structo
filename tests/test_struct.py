from utils import test
import typing as t

import structo as st


@test("SerialiableObject: object")
def _():
    class Foo(st.Struct):
        a: st.u8

    obj = Foo(a=1)
    assert obj == Foo.from_bytes(obj.to_bytes())


@test("SerialiableObject: multiple attributes")
def _():
    class Foo(st.Struct):
        a: st.u8
        b: st.u16_BE

    obj = Foo(a=1, b=256)
    assert obj == Foo.from_bytes(obj.to_bytes())


@test("SerialiableObject: sizeof")
def _():

    class Foo(st.Struct):
        a: st.u8
        b: st.u8

    assert Foo.sizeof() == 2


@test("SerialiableObject: sizeof unknowable")
def _():
    class Foo(st.Struct):
        a: st.u8
        b: t.Annotated[str, st.String(st.u8)]

    assert Foo.sizeof() is None


@test("SerialiableObject: nested object")
def _():
    class Foo(st.Struct):
        a: st.u8

    class Bar(st.Struct):
        foo: Foo

    obj = Bar(foo=Foo(1))
    assert obj == Bar.from_bytes(obj.to_bytes())


@test("SerialiableObject: accepts annotated TypeAliases")
def _():
    type u8 = t.Annotated[int, st.u8]

    class Foo(st.Struct):
        a: u8

    obj = Foo(1)
    assert obj == obj.from_bytes(obj.to_bytes())
