from utils import test
import typing as t

import structo as st


@test("Literal: reading basic")
def _():
    class Foo(st.SerializableObject):
        a: t.Annotated[bytes, st.Literal(b"a", b"b")]

    obj = Foo(a=b"a")
    assert obj == Foo.from_bytes(obj.to_bytes())
