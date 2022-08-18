# Gravitum

[![build](https://github.com/Sh4ww/gravitum/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/Sh4ww/gravitum/actions/workflows/tests.yml)
![PyPI](https://img.shields.io/pypi/v/gravitum)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gravitum)
[![GitHub license](https://img.shields.io/github/license/Sh4ww/gravitum)](https://github.com/Sh4ww/gravitum/blob/main/LICENSE)

Gravitum is a library for implementing decompiled code with Python.

## Requirements

- Python 3.6+

## Installation

```
$ pip install gravitum
```

## Usage

Gravitum defines some interger types with fixed size. You can use shorthand functions (`int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`) to create them.

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

In some cases, decompilers may use their built-in functions in the output. Gravitum implements some of them. You can look up from `gravitum.decompiler_builtins`.

```python
from gravitum import uint32
from gravitum.decompiler_builtins.ida import ror4

v = uint32(0x53683477)
v = ror4(v, 2)
```
