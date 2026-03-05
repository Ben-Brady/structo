from structo import (
    SerializableObject,
    Serializer,
    write_serializable,
    read_serializable,
    uint32_LE,
    String,
    List,
)
import random
import typing as t
from pathlib import Path


class Post(SerializableObject):
    id: uint32_LE
    author: String[uint32_LE]
    tags: List[uint32_LE, String[uint32_LE]]


class PostsSerialiser(Serializer[t.Iterable[Post]]):
    def write(self, buf, format, value):
        for item in value:
            buf.write(bytes([255]))
            write_serializable(buf, Post, item)

        buf.write(bytes([0]))

    def read(self, buf, format):
        while True:
            continue_byte = buf.read(1)[0]
            if continue_byte == 0:
                break
            assert continue_byte == 255, "Continue byte was not 255"

            print("Loading...")  # to prove it's interspliced loading and yielding
            yield read_serializable(buf, Post)


type PostsIterable = t.Annotated[t.Iterable[Post], PostsSerialiser()]


# Too large to effectively store in memory
def generate_posts():
    for x in range(1_000_000):
        yield Post(
            id=random.randint(0, 1_000_000),
            author="Me",
            tags=[str(random.randint(0, 100)) for _ in range(random.randint(0, 10))],
        )


output = Path("output.raw")
if not output.exists():
    with open(output, "wb") as f:
        posts = generate_posts()
        write_serializable(f, PostsIterable, posts)

with open(output, "rb") as f:
    iterable_posts = read_serializable(f, PostsIterable)
    for post in iterable_posts:
        print(post)
