import typing as t
from typing import Annotated
from structo import (
    Struct,
    Serializer,
    uint32_LE,
    String,
    List,
)
import random
from pathlib import Path


class Post(Struct):
    id: Annotated[int, uint32_LE]
    author: Annotated[str, String(uint32_LE)]
    tags: Annotated[list[str], List(String(uint32_LE), uint32_LE)]


CONTINUE_BYTE = bytes([255])
NULL_TERMINATOR = bytes([0])


class PostsSerialiser(Serializer[t.Iterable[Post]]):
    def write(self, f, value):
        for item in value:
            f.write(CONTINUE_BYTE)
            item.write(f)

        f.write(NULL_TERMINATOR)

    def read(self, f):
        while True:
            continue_byte = f.read(1)
            if continue_byte == NULL_TERMINATOR:
                break

            assert continue_byte == CONTINUE_BYTE, "Continue byte was not 255"

            # to prove it's interspliced loading and yielding
            print("Loading...")
            yield Post.read(f)


type PostsIterable = t.Annotated[t.Iterable[Post], PostsSerialiser()]


# Too large to effectively store in memory
def generate_posts():
    for x in range(1_000_000):
        yield Post(
            id=random.randint(0, 1_000_000),
            author="Me",
            tags=[str(random.randint(0, 100))
                  for _ in range(random.randint(0, 10))],
        )


output = Path("output.raw")
if not output.exists():
    with open(output, "wb") as f:
        posts = generate_posts()
        PostsSerialiser().write(f, posts)

with open(output, "rb") as f:
    iterable_posts = PostsSerialiser().read(f)
    for post in iterable_posts:
        print(post)
