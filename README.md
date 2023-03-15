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

Tested with Intel(R) Core(TM) i7-13700K Python 3.11.0.

```shell
pip install .[bench]
python benchmark/bench.py
```

```console
>>> benchmark for numpy array
========================================================================================================================
pickle_serde	size:         1	times: min(3.33e-06)	mid(3.782e-06)	max(5.6893e-05)	95%(3.491e-06)	Std.(2.1728e-07)
numbin_serde	size:         1	times: min(9.9101e-07)	mid(1.106e-06)	max(0.00016518)	95%(1.032e-06)	Std.(1.9601e-07)
numpy_serde	size:         1	times: min(4.9589e-05)	mid(5.2873e-05)	max(0.0010263)	95%(5.0937e-05)	Std.(7.0191e-06)
safets_serde	size:         1	times: min(3.558e-06)	mid(4.141e-06)	max(0.00016262)	95%(3.841e-06)	Std.(3.9577e-07)
msg_np_serde	size:         1	times: min(1.743e-06)	mid(1.937e-06)	max(3.4253e-05)	95%(1.83e-06)	Std.(1.3042e-07)
========================================================================================================================
pickle_serde	size:      1024	times: min(3.555e-06)	mid(4.158e-06)	max(9.9592e-05)	95%(3.813e-06)	Std.(5.7795e-07)
numbin_serde	size:      1024	times: min(1.204e-06)	mid(1.355e-06)	max(2.9116e-05)	95%(1.256e-06)	Std.(1.668e-07)
numpy_serde	size:      1024	times: min(5.0394e-05)	mid(5.4297e-05)	max(0.00019953)	95%(5.2156e-05)	Std.(2.0507e-06)
safets_serde	size:      1024	times: min(4.08e-06)	mid(4.667e-06)	max(4.5634e-05)	95%(4.342e-06)	Std.(2.6851e-07)
msg_np_serde	size:      1024	times: min(2.081e-06)	mid(2.339e-06)	max(3.0831e-05)	95%(2.194e-06)	Std.(2.1181e-07)
========================================================================================================================
pickle_serde	size:     65536	times: min(1.9884e-05)	mid(2.1078e-05)	max(9.3203e-05)	95%(2.024e-05)	Std.(1.2878e-06)
numbin_serde	size:     65536	times: min(1.6847e-05)	mid(1.7845e-05)	max(5.5421e-05)	95%(1.7083e-05)	Std.(1.0197e-06)
numpy_serde	size:     65536	times: min(0.00010117)	mid(0.00010785)	max(0.00022275)	95%(0.00010237)	Std.(4.3429e-06)
safets_serde	size:     65536	times: min(4.0613e-05)	mid(4.2319e-05)	max(0.00010681)	95%(4.0948e-05)	Std.(2.1643e-06)
msg_np_serde	size:     65536	times: min(2.4801e-05)	mid(2.6234e-05)	max(7.0627e-05)	95%(2.5042e-05)	Std.(1.2072e-06)
========================================================================================================================
pickle_serde	size:   3145728	times: min(0.0077576)	mid(0.0080867)	max(0.016288)	95%(0.0077705)	Std.(0.00068357)
numbin_serde	size:   3145728	times: min(0.0093903)	mid(0.013968)	max(0.014586)	95%(0.013006)	Std.(0.00054932)
numpy_serde	size:   3145728	times: min(0.016239)	mid(0.017057)	max(0.017629)	95%(0.01627)	Std.(0.00038771)
safets_serde	size:   3145728	times: min(0.01532)	mid(0.016254)	max(0.022971)	95%(0.015348)	Std.(0.00083347)
msg_np_serde	size:   3145728	times: min(0.016298)	mid(0.021077)	max(0.021851)	95%(0.019673)	Std.(0.00062183)
========================================================================================================================
pickle_serde	size: 201326592	times: min(0.89339)	mid(0.89483)	max(0.89901)	95%(0.89343)	Std.(0.0020278)
numbin_serde	size: 201326592	times: min(0.87285)	mid(0.87507)	max(0.87934)	95%(0.87292)	Std.(0.0021327)
numpy_serde	size: 201326592	times: min(0.76402)	mid(0.76939)	max(0.8509)	95%(0.76415)	Std.(0.032678)
safets_serde	size: 201326592	times: min(1.7488)	mid(1.7555)	max(1.8294)	95%(1.7489)	Std.(0.030627)
msg_np_serde	size: 201326592	times: min(1.3325)	mid(1.3386)	max(1.343)	95%(1.3325)	Std.(0.004391)
```
