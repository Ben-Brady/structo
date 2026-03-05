import structo as st
from utils import test


@test("Array: sizeof")
def _():
    assert st.Array(4, st.int8).sizeof() == 4
