# Fishbones

[![build](https://github.com/sledgeh4w/fishbones/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/sledgeh4w/fishbones/actions/workflows/tests.yml)
![PyPI](https://img.shields.io/pypi/v/fishbones)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fishbones)
[![GitHub license](https://img.shields.io/github/license/sledgeh4w/fishbones)](https://github.com/sledgeh4w/fishbones/blob/main/LICENSE)

Fishbones is a library for implementing decompiled code with Python.

## Requirements

- Python 3.6+

## Installation

```
$ pip install fishbones
```

## Usage

Fishbones defines some integer types with fixed size. You can use shorthand functions (`int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`) to create them.

```python
from fishbones import uint8

v = uint8(0x53)
```

Pointer operations are common in the decompiled code.

```c
unsigned __int8 data[8] = {71, 114, 97, 118, 105, 116, 117, 109};

unsigned __int8 *p = data;
unsigned __int8 v = p[4];

*((unsigned __int32 *)p + 1) = v;
```

So Fishbones provides `vptr`.

```python
from fishbones import vptr

data = bytearray([71, 114, 97, 118, 105, 116, 117, 109])

p = vptr(data, 'uint8')
v = p.add(4).read()

p.cast('uint32').add(1).write(v)
```

In some cases, decompilers may use their built-in functions in the output. Fishbones implements some of them. You can look up from `fishbones.decompiler_builtins`.

```python
from fishbones import uint32
from fishbones.decompiler_builtins.ida import ror4

v = uint32(0x53683477)
v = ror4(v, 2)
```
