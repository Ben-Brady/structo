from structo import SerialiableObject, deserialize_from_bytes

def assert_serialises_correctly(before: SerialiableObject):
    obj_type = type(before)
    data = before.to_bytes()
    after = deserialize_from_bytes(obj_type, data)
    assert before == after, f"{before} did not save and load correctly"

def assert_equal(actual: bytes, expected: bytes):
    assert actual == expected, f"expected {expected}, recieved {actual}"
