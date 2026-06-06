import typing as t
import structo as st
from utils import test
import pytest
import io


@test("Blob: sizeof")
def _():
    assert st.Blob(st.i8).sizeof() == None


@test("Blob: basic")
def _():
    serializer = st.Blob()

    data = b"foo"
    assert data == serializer.from_bytes(serializer.to_bytes(data))
