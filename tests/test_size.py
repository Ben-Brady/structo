import structo as st
import pytest
from utils import test


@test("sizeof(primatives): single parameter")
@pytest.mark.parametrize(
    "datatype,length",
    [
        (st.uint8, 1),
        (st.uint16, 2),
        (st.uint32, 4),
        (st.uint64, 8),
        (st.int8, 1),
        (st.int16, 2),
        (st.int32, 4),
        (st.int64, 8),
        (st.float32, 4),
        (st.float64, 8),
    ],
)
def _(datatype, length):
    assert st.sizeof(datatype) == length


@test("sizeof(SerializableObject): single parameter")
def _():
    class Foo(st.SerializableObject):
        bar: st.uint32_BE

    assert st.sizeof(Foo) == 4


@test("sizeof(SerializableObject): two arguemnts")
def _():
    class Foo(st.SerializableObject):
        foo: st.uint32_BE
        bar: st.uint32_BE

    assert st.sizeof(Foo) == 8


@test("sizeof(SerializableObject): mixed arguments")
def _():
    class Foo(st.SerializableObject):
        a: st.uint32_BE
        b: st.uint8
        c: st.Buffer[100]

    assert st.sizeof(Foo) == 4 + 1 + 100


@test("sizeof(SerializableObject): unknownable")
def _():
    class Foo(st.SerializableObject):
        a: st.String[st.uint8]

    assert st.sizeof(Foo) is None


@test("sizeof(SerializableObject): unknownable mixed")
def _():
    class Foo(st.SerializableObject):
        a: st.uint8
        b: st.String[st.uint8]

    assert st.sizeof(Foo) is None
