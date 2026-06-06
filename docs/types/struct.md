# Struct

Stucts are the core of Structo, they allow you to serialise and deserialise multiple values together into a single object.

They are a extended dataclass that uses `typing.Annotated` to describe what types to use to store variables.

```py
class User(st.Struct):
    id: st.u32
    name: Annotated[str, st.String()]
    tags: Annotated[list[str], st.List(st.String())]
```

## Usage
