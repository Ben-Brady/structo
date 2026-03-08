# List

A dynaimcally length list of values, prefixed with a length.

You must specifiy the length type and value type

## Examples

```py
List(String())
# list[float] with max length of 65536
List(float32, length=uint16_LE)
```
