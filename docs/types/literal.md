# Byte Literal

It's a common pattern to have a fixed literal in a file format, Byte Literal lets you implements this more simply.

## Example

```py
from structo import Literal
filetype: Literal(b"mp4")

# You can specify multiple allowed values
chunk_type: Literal(b"data", b"head", b"fmt ")
```
