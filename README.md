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

Tested with Intel(R) Core(TM) i5-8500 CPU @ 3.00GHz.

```console
================================================================================
pickle_serde
size:            1      times: min(9.877e-06)   mid(1.0278e-05) max(7.6076e-05) 95%(9.961e-06)  Std.(1.9686e-06)
size:         1024      times: min(1.1584e-05)  mid(1.2048e-05) max(3.8084e-05) 95%(1.1724e-05) Std.(9.4674e-07)
size:        65536      times: min(0.00026807)  mid(0.00026876) max(0.0006682)  95%(0.00026823) Std.(1.3797e-05)
size:      3145728      times: min(0.015116)    mid(0.015333)   max(0.035099)   95%(0.01512)    Std.(0.0019832)
size:    201326592      times: min(2.309)       mid(2.3179)     max(2.6027)     95%(2.309)      Std.(0.11552)
================================================================================
numbin_serde
size:            1      times: min(2.423e-06)   mid(2.484e-06)  max(4.0442e-05) 95%(2.44e-06)   Std.(3.9544e-07)
size:         1024      times: min(3.225e-06)   mid(3.333e-06)  max(3.0047e-05) 95%(3.266e-06)  Std.(6.4336e-07)
size:        65536      times: min(4.2823e-05)  mid(4.3306e-05) max(0.00037845) 95%(4.2958e-05) Std.(1.1183e-05)
size:      3145728      times: min(0.023136)    mid(0.023507)   max(0.025562)   95%(0.023197)   Std.(0.00039479)
size:    201326592      times: min(1.5148)      mid(1.518)      max(1.5418)     95%(1.5148)     Std.(0.010186)
================================================================================
numpy_save_load
size:            1      times: min(0.00012347)  mid(0.00012813) max(0.0027535)  95%(0.00012458) Std.(3.5254e-05)
size:         1024      times: min(0.00013147)  mid(0.0001368)  max(0.00026768) 95%(0.00013283) Std.(9.2795e-06)
size:        65536      times: min(0.00022034)  mid(0.00022681) max(0.00081372) 95%(0.00022168) Std.(2.1723e-05)
size:      3145728      times: min(0.027812)    mid(0.028208)   max(0.029269)   95%(0.027837)   Std.(0.00023815)
size:    201326592      times: min(2.1069)      mid(2.1491)     max(2.466)      95%(2.1082)     Std.(0.13059)
```
