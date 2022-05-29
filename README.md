# Gravitum

Gravitum is a library for implementing decompiled code with Python.

## Requirements

- Python 3.6+

## Installation

```
$ pip install gravitum
```

## Usage

Gravitum defines some interger types based on the types of [numpy](https://github.com/numpy/numpy). You can use shorthand functions (`int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`) to create them.

```python
from gravitum import uint8

v = uint8(0x53)
```

Pointer operations are common in the decompiled code.

```c
unsigned __int8 data[8] = {71, 114, 97, 118, 105, 116, 117, 109};

unsigned __int8 *p = data;
unsigned __int8 v = p[4];

*((unsigned __int32 *)p + 1) = v;
```

So Gravitum provides `vptr`.

```python
from gravitum import vptr

data = bytearray([71, 114, 97, 118, 105, 116, 117, 109])

p = vptr(data, 'uint8')
v = p.add(4).read()

p.cast('uint32').add(1).write(v)
```

For IDA, Gravitum implements some functions (`rol*`, `ror*`, `byte*`, `word*`, `bswap*`, `clz`, etc.) that are often used in its output. You can import them from `gravitum.ida`.

```python
from gravitum import uint32
from gravitum.ida import ror4

v = uint32(0x53683477)
v = ror4(v, 2)
```
