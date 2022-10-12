import pickle
from dataclasses import dataclass
from io import BytesIO
from time import perf_counter

import numpy as np

from numbin import NumBin

nb = NumBin()


@dataclass(frozen=True)
class Data:
    arr: np.ndarray
    msg: str
    epoch: int = 10


def generate_data():
    return (
        Data(np.random.rand(1), "scalar", 10000),
        Data(np.random.rand(1024), "vector", 10000),
        Data(np.random.rand(64, 1024), "matrix", 1000),
        Data(np.random.randint(0, 255, (3, 1024, 1024)), "image", 100),
        Data(np.random.randint(0, 255, (64, 3, 1024, 1024)), "batch of images", 5),
    )


def pickle_serde(data: Data):
    pickle.loads(pickle.dumps(data.arr))


def numbin_serde(data: Data):
    nb.loads(nb.dumps(data.arr))


def numpy_save_load(data: Data):
    fp = BytesIO()
    np.save(fp, data.arr, allow_pickle=False, fix_imports=False)
    fp.seek(0)
    np.load(fp, allow_pickle=False, fix_imports=False)


def time_record(func, args=(), round=5):
    res = [0] * round
    for i in range(round):
        t0 = perf_counter()
        func(*args)
        res[i] = perf_counter() - t0
    return res


def benchmark():
    for func in [pickle_serde, numbin_serde, numpy_save_load]:
        print("=" * 80)
        print(f"{func.__name__}")
        for data in generate_data():
            t = time_record(func, (data,), data.epoch)
            print(
                f"size: {data.arr.size:12}\ttimes: "
                f"min({np.min(t):.5})\tmid({np.median(t):.5})\tmax({np.max(t):.5})\t"
                f"95%({np.percentile(t, 0.95):.5})\tStd.({np.std(t):.5})",
            )


if __name__ == "__main__":
    benchmark()
