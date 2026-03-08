# PackedInts

PackedInts lets you pack bits into fewer bytes.

It's total


```py
import structo as st

class Foo(st.PackedInts):
    type: t.Annotated[int, st.PackedInt(bits=2)]
    completed: t.Annotated[int, st.PackedInt(bits=1)]
    b: t.Annotated[int, st.PackedInt(bits=5)]
```
