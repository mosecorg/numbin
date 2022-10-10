from io import BytesIO

import numpy as np
import pytest

from numbin import NumBin


@pytest.fixture
def array():
    return np.random.rand(3, 5)


@pytest.fixture
def nb():
    return NumBin()


def test_num_in_memory(nb, array):
    b = nb.dumps(array)
    assert isinstance(b, bytes)
    assert np.array_equal(array, nb.loads(b))


def test_num_in_file(nb, array):
    fp = BytesIO()
    nb.dump(array, fp)
    fp.seek(0)
    assert np.array_equal(array, nb.load(fp))
