# String

A UTF-8 encoded string with a dynamic length, the length is stored as a prefix.

The length is uint32 by default, meaning a max length of 4.2M characters.

## Examples

```py
String() # uint32 by default, max length 4.2GB
String(uint16_LE) # max length 65,536
String(uint8) # max length 255
```
