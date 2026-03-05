from structo import Literal, serialize_to_bytes, SerializableObject


class Foo(SerializableObject):
    bar: Literal[b"foo"] = ... # type: ignore


serialize_to_bytes(Literal[b"foo"], b"foo")
