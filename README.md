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
size:            1      times: min(8.065e-06)   mid(8.457e-06)  max(0.00014736) 95%(8.185e-06)  Std.(3.1934e-06)
size:         1024      times: min(9.428e-06)   mid(1.015e-05)  max(0.00014235) 95%(9.638e-06)  Std.(3.8205e-06)
size:        65536      times: min(0.000155)    mid(0.0001581)  max(0.00061054) 95%(0.00015533) Std.(2.3462e-05)
size:      3145728      times: min(0.0072165)   mid(0.0082978)  max(0.015297)   95%(0.0073169)  Std.(0.001018)
size:    201326592      times: min(1.1303)      mid(1.23)       max(1.3989)     95%(1.1323)     Std.(0.089972)
================================================================================
numbin_serde
size:            1      times: min(1.974e-06)   mid(2.084e-06)  max(0.00019909) 95%(2.013e-06)  Std.(2.1158e-06)
size:         1024      times: min(2.514e-06)   mid(2.685e-06)  max(9.9267e-05) 95%(2.574e-06)  Std.(1.7772e-06)
size:        65536      times: min(2.3535e-05)  mid(2.4196e-05) max(0.00051521) 95%(2.3595e-05) Std.(1.586e-05)
size:      3145728      times: min(0.0068677)   mid(0.0075904)  max(0.020155)   95%(0.0069143)  Std.(0.0013657)
size:    201326592      times: min(0.51976)     mid(0.66418)    max(0.74812)    95%(0.52107)    Std.(0.083191)
================================================================================
numpy_save_load
size:            1      times: min(0.00010345)  mid(0.00011227) max(0.0096088)  95%(0.00010525) Std.(0.00010952)
size:         1024      times: min(0.00010638)  mid(0.00011138) max(0.00039846) 95%(0.00010751) Std.(2.5658e-05)
size:        65536      times: min(0.00016052)  mid(0.00016934) max(0.00057942) 95%(0.00016236) Std.(2.4938e-05)
size:      3145728      times: min(0.01337)     mid(0.017721)   max(0.023641)   95%(0.013613)   Std.(0.0024529)
size:    201326592      times: min(1.5571)      mid(2.5337)     max(5.0581)     95%(1.5796)     Std.(1.1949)
```
