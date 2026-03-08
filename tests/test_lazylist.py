from utils import test
import typing as t

import structo as st


@test("LazyList: basic")
def _():
    class Foo(st.SerializableObject):
        values: t.Annotated[t.Iterable[int], st.LazyList(st.uint8)]

    obj = Foo(values=[1, 2, 3])
    after_obj = Foo.from_bytes(obj.to_bytes())
    assert list(after_obj.values) == [1, 2, 3]


@test("LazyList: with adjecet properties")
def _():
    class Foo(st.SerializableObject):
        a: t.Annotated[int, st.uint8]
        values: t.Annotated[t.Iterable[int], st.LazyList(st.uint8)]
        c: t.Annotated[int, st.uint8]

    obj = Foo(a=63, values=[1, 2, 3], c=64)
    after_obj = Foo.from_bytes(obj.to_bytes())
    assert after_obj.a == obj.a, after_obj
    assert after_obj.c == obj.c, after_obj
    assert list(after_obj.values) == [1, 2, 3], after_obj


@test("LazyList: accessing multiple iterators at once")
def _():
    class Foo(st.SerializableObject):
        a: t.Annotated[t.Iterable[int], st.LazyList(st.uint8)]
        b: t.Annotated[t.Iterable[int], st.LazyList(st.uint8)]

    obj = Foo(
        a=[1, 2, 3, 4, 5],
        b=[5, 10, 15, 20, 25],
    )
    after_obj = Foo.from_bytes(obj.to_bytes())
    for a, b in zip(after_obj.a, after_obj.b):
        assert a * 5 == b
