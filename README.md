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

Work with pure NumPy data:

```python
import numbin as nb
import numpy as np


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

Work with complex data:

```python
from numbin.msg_ext import NumBinMessage


nbm = NumBinMessage()
data = {"tensor": arr, "labels": ["dog", "cat"], "safe": True}

# in memory
binary = nbm.dumps(data)
print(nbm.loads(binary))

# file
with open("data.bin", "wb") as f:
    nbm.dump(data, f)

with open("data.bin", "rb") as f:
    print(nbm.load(f))
```

## Benchmark

The code can be found in [bench.py](benchmark/bench.py)

Tested with Intel(R) Core(TM) i5-8500 CPU @ 3.00GHz Python 3.11.0.

```console
>>> benchmark for numpy array
========================================================================================================================
pickle_serde    size:         1 times: min(9.952e-06)   mid(1.0284e-05) max(0.00012502) 95%(1.0083e-05) Std.(1.2433e-06)
numbin_serde    size:         1 times: min(2.727e-06)   mid(2.824e-06)  max(5.563e-05)  95%(2.7679e-06) Std.(6.9532e-07)
numpy_save_load size:         1 times: min(0.00013145)  mid(0.00013528) max(0.0021547)  95%(0.00013252) Std.(2.1891e-05)
========================================================================================================================
pickle_serde    size:      1024 times: min(1.1219e-05)  mid(1.1626e-05) max(6.7387e-05) 95%(1.1352e-05) Std.(1.0844e-06)
numbin_serde    size:      1024 times: min(3.326e-06)   mid(3.444e-06)  max(4.3707e-05) 95%(3.371e-06)  Std.(7.5806e-07)
numpy_save_load size:      1024 times: min(0.00013785)  mid(0.00014344) max(0.00026173) 95%(0.00013913) Std.(6.8812e-06)
========================================================================================================================
pickle_serde    size:     65536 times: min(4.8282e-05)  mid(4.9399e-05) max(0.00029774) 95%(4.8512e-05) Std.(2.9386e-06)
numbin_serde    size:     65536 times: min(3.8543e-05)  mid(3.9357e-05) max(9.9388e-05) 95%(3.8681e-05) Std.(3.1692e-06)
numpy_save_load size:     65536 times: min(0.00021826)  mid(0.00022547) max(0.00074907) 95%(0.00021916) Std.(2.0406e-05)
========================================================================================================================
pickle_serde    size:   3145728 times: min(0.014393)    mid(0.017675)   max(0.030137)   95%(0.01456)    Std.(0.0036429)
numbin_serde    size:   3145728 times: min(0.020834)    mid(0.023769)   max(0.037167)   95%(0.02309)    Std.(0.0022647)
numpy_save_load size:   3145728 times: min(0.036523)    mid(0.038008)   max(0.29076)    95%(0.036596)   Std.(0.095368)
========================================================================================================================
pickle_serde    size: 201326592 times: min(1.5232)      mid(1.5588)     max(1.7401)     95%(1.5234)     Std.(0.09501)
numbin_serde    size: 201326592 times: min(1.5286)      mid(1.5301)     max(1.5348)     95%(1.5286)     Std.(0.0024368)
numpy_save_load size: 201326592 times: min(2.2289)      mid(2.3567)     max(2.7892)     95%(2.229)      Std.(0.21158)
>>> benchmark for normal data mixed with numpy array
========================================================================================================================
pickle_serde    size: <unknown> times: min(1.4121e-05)  mid(1.4568e-05) max(7.9592e-05) 95%(1.4355e-05) Std.(1.7201e-06)
nbmsg_serde     size: <unknown> times: min(9.188e-06)   mid(9.518e-06)  max(0.011783)   95%(9.331e-06)  Std.(3.5517e-05)
========================================================================================================================
pickle_serde    size: <unknown> times: min(5.4409e-05)  mid(5.4909e-05) max(0.00016216) 95%(5.4595e-05) Std.(4.3362e-06)
nbmsg_serde     size: <unknown> times: min(0.00010215)  mid(0.00010288) max(0.00023232) 95%(0.0001024)  Std.(6.7374e-06)
```
