from utils import test
import typing as t

import structo as st


@test("Optional: float vlaue")
def _():
    class Foo(st.Struct):
        a: t.Annotated[float | None, st.Optional(st.f64)]

    obj = Foo(a=1.0)
    assert obj == Foo.from_bytes(obj.to_bytes())


@test("Optional: object")
def _():
    class Bar(st.Struct):
        a: t.Annotated[int, st.u16_LE]
        b: t.Annotated[int, st.u16_LE]

    class Foo(st.Struct):
        a: t.Annotated[float | None, st.Optional(st.f64)]
        b: t.Annotated[Bar | None, st.Optional(Bar)]

    obj = Foo(a=1.0, b=None)
    assert obj == Foo.from_bytes(obj.to_bytes())


@test("Optional: empty")
def _():
    class Foo(st.Struct):
        a: t.Annotated[float | None, st.Optional(st.f64)]

    obj = Foo(a=None)
    assert obj == Foo.from_bytes(obj.to_bytes())
