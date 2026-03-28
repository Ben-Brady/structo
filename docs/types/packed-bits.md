# PackedInts

PackedInts lets you pack bits into fewer bytes.

It's total

```py
import structo as st

class Foo(st.PackedBits):
    type: t.Annotated[int, st.Bits(2)]
    completed: t.Annotated[int, st.Bits(1)]
    id: t.Annotated[int, st.Bits(5)]
```
