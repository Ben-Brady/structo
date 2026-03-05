def test(name: str):
    def wrapper(func):
        # automatically mark async tests
        # if inspect.iscoroutinefunction(func):
        #     func = pytest.mark.asyncio(func)

        func.__globals__[" " + name] = func

    return wrapper


from structo import SerializableObject, deserialize_from_bytes


def assert_serialises_correctly(before: SerializableObject):
    obj_type = type(before)
    data = before.to_bytes()
    after = deserialize_from_bytes(obj_type, data)
    assert before == after, f"{before} did not save and load correctly"


def assert_equal(actual: bytes, expected: bytes):
    assert actual == expected, f"expected {expected}, recieved {actual}"
