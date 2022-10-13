# NumBin

<p align="center">
  <a href="https://pypi.org/project/numbin/">
    <img src="https://badge.fury.io/py/numbin.svg" alt="PyPI version" height="20">
  </a>
  <a href="https://pypi.org/project/numbin">
    <img src="https://img.shields.io/pypi/pyversions/numbin" alt="Python Version" />
  </a>
  <a href="https://tldrlegal.com/license/apache-license-2.0-(apache-2.0)">
    <img src="https://img.shields.io/github/license/mosecorg/numbin" alt="License" height="20">
  </a>
  <a href="https://github.com/mosecorg/numbin/actions/workflows/python-check.yml">
    <img src="https://github.com/mosecorg/numbin/actions/workflows/python-check.yml/badge.svg" alt="Check status" height="20">
  </a>
</p>

An efficient binary serialization format for numerical data.

## Install

```sh
pip install numbin
```

## Usage

```python
from numbin import NumBin
import numpy as np

nb = NumBin()
arr = np.random.rand(5, 3)

# in memory
binary = nb.dumps(arr)
print(nb.loads(binary))

# file
with open("num.bin", "wb") as f:
    nb.dump(arr, f)

with open("num.bin", "rb") as f:
    print(nb.load(f))
```
## Benchmark

The code can be found in [bench.py](benchmark/bench.py)

Tested with AMD Ryzen 7 5800H.

```console
================================================================================
pickle_serde
size:            1      times: min(8.266e-06)   mid(8.637e-06)  max(0.00017574) 95%(8.386e-06)  Std.(4.4708e-06)
size:         1024      times: min(9.027e-06)   mid(9.588e-06)  max(0.00048644) 95%(9.157e-06)  Std.(6.6986e-06)
size:        65536      times: min(0.00014838)  mid(0.00015669) max(0.00059667) 95%(0.00015015) Std.(3.4924e-05)
size:      3145728      times: min(0.0078354)   mid(0.0088624)  max(0.026796)   95%(0.0079751)  Std.(0.0018613)
size:    201326592      times: min(1.4744)      mid(2.6627)     max(12.929)     95%(1.4906)     Std.(4.9328)
================================================================================
numbin_serde
size:            1      times: min(1.823e-06)   mid(1.973e-06)  max(0.00090879) 95%(1.863e-06)  Std.(9.2777e-06)
size:         1024      times: min(2.504e-06)   mid(2.665e-06)  max(0.00024218) 95%(2.555e-06)  Std.(3.2113e-06)
size:        65536      times: min(3.3083e-05)  mid(3.3905e-05) max(0.0026087)  95%(3.3248e-05) Std.(8.1968e-05)
size:      3145728      times: min(0.0092391)   mid(0.011318)   max(0.12104)    95%(0.0093036)  Std.(0.012046)
size:    201326592      times: min(0.84969)     mid(1.7524)     max(3.2798)     95%(0.88241)    Std.(0.7914)
================================================================================
numpy_save_load
size:            1      times: min(0.00010159)  mid(0.00010938) max(0.10722)    95%(0.00010299) Std.(0.0012863)
size:         1024      times: min(0.00010753)  mid(0.00014313) max(0.0010275)  95%(0.00011039) Std.(4.629e-05)
size:        65536      times: min(0.00016488)  mid(0.00018317) max(0.0022175)  95%(0.00016596) Std.(7.817e-05)
size:      3145728      times: min(0.013115)    mid(0.014641)   max(0.091159)   95%(0.013145)   Std.(0.0090796)
size:    201326592      times: min(0.83881)     mid(1.6322)     max(3.0162)     95%(0.84089)    Std.(0.85819)
```
