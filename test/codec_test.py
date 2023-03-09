from io import BytesIO

import numpy as np
import pytest

import numbin as nb


@pytest.fixture
def array():
    return np.random.rand(3, 5)


def test_num_in_memory(array):
    b = nb.dumps(array)
    assert isinstance(b, bytes)
    assert np.array_equal(array, nb.loads(b))


def test_num_in_file(array):
    fp = BytesIO()
    nb.dump(array, fp)
    fp.seek(0)
    assert np.array_equal(array, nb.load(fp))
