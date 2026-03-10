from utils import test
import typing as t

import pytest
import structo as st


@test("PackedInts: serialise on single bytes")
def _():
    class Foo(st.PackedInts):
        a: t.Annotated[int, st.PackedInt(bits=2)]
        b: t.Annotated[int, st.PackedInt(bits=3)]

    obj = Foo(a=0, b=3)
    assert obj == Foo.from_bytes(obj.to_bytes())


@test("PackedInts: serialise across byte boundaries single bytes")
def _():
    class Foo(st.PackedInts):
        a: t.Annotated[int, st.PackedInt(bits=5)]
        b: t.Annotated[int, st.PackedInt(bits=6)]
        c: t.Annotated[int, st.PackedInt(bits=5)]

    obj = Foo(a=0, b=63, c=0)
    assert obj == Foo.from_bytes(obj.to_bytes())


@test("PackedInts: multibyte integer")
def _():
    class Foo(st.PackedInts):
        a: t.Annotated[int, st.PackedInt(bits=11)]
        b: t.Annotated[int, st.PackedInt(bits=5)]

    obj = Foo(a=(2**11) - 1, b=0)
    assert obj == Foo.from_bytes(obj.to_bytes())


@test("PackedInts: max value throw error")
def _():
    class Foo(st.PackedInts):
        a: t.Annotated[int, st.PackedInt(bits=2)]

    with pytest.raises(Exception):
        Foo(a=4).to_bytes()


@test("PackedInts: max value throw error on constructor")
@pytest.mark.skip()
def _():
    class Foo(st.PackedInts):
        a: t.Annotated[int, st.PackedInt(bits=2)]

    with pytest.raises(Exception):
        Foo(a=4)


@test("PackedInts: sizeof")
def _():
    class OneByte_A(st.PackedInts):
        a: t.Annotated[int, st.PackedInt(bits=2)]
        b: t.Annotated[int, st.PackedInt(bits=1)]

    assert OneByte_A.sizeof() == 1

    class OneByte_B(st.PackedInts):
        a: t.Annotated[int, st.PackedInt(bits=8)]

    assert OneByte_B.sizeof() == 1

    class OneByte_C(st.PackedInts):
        a: t.Annotated[int, st.PackedInt(bits=3)]
        b: t.Annotated[int, st.PackedInt(bits=3)]
        c: t.Annotated[int, st.PackedInt(bits=2)]

    assert OneByte_C.sizeof() == 1

    class TwoBytes_A(st.PackedInts):
        a: t.Annotated[int, st.PackedInt(bits=5)]
        b: t.Annotated[int, st.PackedInt(bits=4)]

    assert TwoBytes_A.sizeof() == 2

    class TwoBytes_B(st.PackedInts):
        a: t.Annotated[int, st.PackedInt(bits=6)]
        b: t.Annotated[int, st.PackedInt(bits=6)]
        c: t.Annotated[int, st.PackedInt(bits=4)]

    assert TwoBytes_B.sizeof() == 2

    class ThreeBytes_A(st.PackedInts):
        a: t.Annotated[int, st.PackedInt(bits=6)]
        b: t.Annotated[int, st.PackedInt(bits=6)]
        c: t.Annotated[int, st.PackedInt(bits=5)]

    assert ThreeBytes_A.sizeof() == 3


@test("PackedInts: negative value raises error")
def _():
    class Foo(st.PackedInts):
        a: t.Annotated[int, st.PackedInt(bits=8)]

    with pytest.raises(Exception):
        Foo(-100).to_bytes()
