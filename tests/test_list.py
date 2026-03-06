from utils import test
import typing as t

import structo as st


@test("List: nested bits")
def _():
    class Bits(st.PackedInts):
        a: t.Annotated[int, st.PackedInt(bits=2)]

    class Object(st.SerializableObject):
        foo: t.Annotated[list[Bits], st.List(st.uint8, Bits)]

    obj = Object(foo=[Bits(a=1)])
    assert obj == Object.from_bytes(obj.to_bytes())

