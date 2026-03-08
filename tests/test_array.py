import typing as t
import structo as st
from utils import test


@test("Array: sizeof")
def _():
    assert st.Array(st.int8, 4).sizeof() == 4


@test("Array: nested bits")
def _():
    class Bits(st.PackedInts):
        a: t.Annotated[int, st.PackedInt(bits=2)]

    class Object(st.SerializableObject):
        bits: t.Annotated[list[Bits], st.Array(Bits, 2)]

    obj = Object(bits=[Bits(1), Bits(2)])
    assert obj == Object.from_bytes(obj.to_bytes())
