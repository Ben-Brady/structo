from utils import test
import typing as t

import structo as st


@test("SerialiableObject: object")
def _():
    class Foo(st.SerializableObject):
        a: t.Annotated[int, st.uint8]

    obj = Foo(a=1)
    assert obj == Foo.from_bytes(obj.to_bytes())


@test("SerialiableObject: multiple attributes")
def _():
    class Foo(st.SerializableObject):
        a: t.Annotated[int, st.uint8]
        b: t.Annotated[int, st.uint16_BE]

    obj = Foo(a=1, b=256)
    assert obj == Foo.from_bytes(obj.to_bytes())


@test("SerialiableObject: sizeof")
def _():

    class Foo(st.SerializableObject):
        a: t.Annotated[int, st.uint8]
        b: t.Annotated[str, st.uint8]

    assert Foo.sizeof() == 2


@test("SerialiableObject: sizeof unknowable")
def _():
    class Foo(st.SerializableObject):
        a: t.Annotated[int, st.uint8]
        b: t.Annotated[str, st.String(st.uint8)]

    assert Foo.sizeof() is None


@test("SerialiableObject: nested object")
def _():
    class Foo(st.SerializableObject):
        a: t.Annotated[int, st.uint8]

    class Bar(st.SerializableObject):
        foo: Foo

    obj = Bar(foo=Foo(1))
    assert obj == Bar.from_bytes(obj.to_bytes())

