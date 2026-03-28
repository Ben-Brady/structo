from utils import test
import typing as t

import pytest
import structo as st


@test("Literal: reading basic")
def _():
    class Foo(st.Struct):
        a: t.Annotated[bytes, st.Literal(b"a", b"b")]

    obj = Foo(a=b"a")
    assert obj == Foo.from_bytes(obj.to_bytes())


@test("Literal: invalid literal fails")
def _():
    class Foo(st.Struct):
        a: t.Annotated[bytes, st.Literal(b"a", b"b")]

    with pytest.raises(Exception):
        Foo(a=b"c").to_bytes()
