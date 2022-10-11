from io import BytesIO

import numpy as np
import pytest

from numbin.msg_ext import NumBinMessage


@pytest.fixture
def data():
    return {
        "tensor": np.random.rand(
            5,
            3,
            2,
        ),
        "category": 1000,
        "threshold": 0.7,
        "tags": ("cat", "dog"),
    }


@pytest.fixture
def nbm():
    return NumBinMessage()


def is_equal(x, y):
    if isinstance(x, np.ndarray):
        return isinstance(y, np.ndarray) and np.array_equal(x, y)
    if isinstance(x, dict):
        return len(x) == len(y) and all(is_equal(x[k], y[k]) for k in x)
    return x == y


def test_data_in_memory(nbm, data):
    b = nbm.dumps(data)
    assert isinstance(b, bytes)
    assert is_equal(data, nbm.loads(b))


def test_data_in_file(nbm, data):
    fp = BytesIO()
    nbm.dump(data, fp)
    fp.seek(0)
    assert is_equal(data, nbm.load(fp))
