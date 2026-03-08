# Blob

A dynamically set of bytes that is prefixed with it's length

## Usage

When creating your own system, always use a uint number. Signed intergers are allows for compatiblity with existing systems

## Examples

```py
Blob(uint32_BE) # Blob with length stored as uint32bit
```
