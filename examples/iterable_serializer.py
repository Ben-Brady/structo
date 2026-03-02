from structo import SerialiableObject, Serializer, serialize, deserialize, uint32_LE, String, List
import random
import typing as t
from pathlib import Path


class Post(SerialiableObject):
    id: uint32_LE
    author: String[uint32_LE]
    tags: List[uint32_LE, String[uint32_LE]]


class PostsSerialiser(Serializer[t.Iterable[Post]]):
    @staticmethod
    def write(buf, format, value):
        for item in value:
            buf.write(bytes([255]))
            serialize(buf, Post, item)

        buf.write(bytes([0]))

    @staticmethod
    def read(buf, format):
        while True:
            continue_byte = buf.read(1)[0]
            if continue_byte == 0:
                break
            assert continue_byte == 255, "Continue byte was not 255"

            print("Loading...") # to provie it's interspliced loading and yielding
            yield deserialize(buf, Post)

type posts_datatype = t.Annotated[t.Iterable[Post], PostsSerialiser()]


# Too large to effectively store in memory
def generate_posts():
    for x in range(1_000_000):
        yield Post(
            id=random.randint(0, 1_000_000),
            author="Me",
            tags=[
                str(random.randint(0, 100))
                for _ in range(random.randint(0, 10))
            ]
        )



output = Path("output.raw")
if not output.exists():
    with open(output, "wb") as f:
        serialize(f, posts_datatype, generate_posts())

with open(output, "rb") as f:
    iterable_posts = deserialize(f, posts_datatype)
    for post in iterable_posts:
        print(post)

