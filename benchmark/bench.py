import gc
import pickle
import traceback
from dataclasses import dataclass
from io import BytesIO
from time import perf_counter

import numpy as np

from numbin import NumBin
from numbin.msg_ext import NumBinMessage

nb = NumBin()
nbm = NumBinMessage()


@dataclass(frozen=True)
class Data:
    arr: np.ndarray | dict
    msg: str
    epoch: int


def generate_data():
    return (
        Data(
            {"msg": "long message" * 1000, "vec": np.random.rand(1024)},
            "long message with 1024 vector",
            10000,
        ),
        Data(
            {
                "int": 233,
                "float": 3.14,
                "vec": np.random.rand(1024),
                "matrix": np.random.rand(64, 1024),
            },
            "int, float, vector and matrix",
            100,
        ),
    )


def generate_np_data():
    return (
        Data(np.random.rand(1), "scalar", 10000),
        Data(np.random.rand(1024), "vector", 10000),
        Data(np.random.rand(64, 1024), "matrix", 1000),
        Data(np.random.rand(3, 1024, 1024), "image", 100),
        Data(np.random.rand(64, 3, 1024, 1024), "batch of images", 5),
    )


def pickle_serde(data: Data):
    pickle.loads(
        pickle.dumps(data.arr, fix_imports=False, protocol=pickle.HIGHEST_PROTOCOL),
        fix_imports=False,
    )


def numbin_serde(data: Data):
    nb.loads(nb.dumps(data.arr))


def nbmsg_serde(data: Data):
    nbm.loads(nbm.dumps(data.arr))


def numpy_save_load(data: Data):
    fp = BytesIO()
    np.save(fp, data.arr, allow_pickle=False, fix_imports=False)
    fp.seek(0)
    np.load(fp, allow_pickle=False, fix_imports=False)


def time_record(func, data: Data, threshold=1):
    res = []
    total_sec = 0
    while total_sec < threshold:
        for _ in range(data.epoch):
            t0 = perf_counter()
            try:
                func(data)
            except:
                print(traceback.format_exc())
            finally:
                res.append(perf_counter() - t0)
                total_sec += res[-1]
    return res


def display_result(func, data):
    gc_flag = gc.isenabled()
    gc.disable()
    try:
        t = time_record(func, data)
    finally:
        if gc_flag:
            gc.enable()
    size = data.arr.size if isinstance(data.arr, np.ndarray) else "<unknown>"
    print(
        f"{func.__name__}\tsize: {size:9}\ttimes: "
        f"min({np.min(t):.5})\tmid({np.median(t):.5})\tmax({np.max(t):.5})\t"
        f"95%({np.percentile(t, 0.95):.5})\tStd.({np.std(t):.5})",
    )


def benchmark():
    print(">>> benchmark for numpy array")
    for data in generate_np_data():
        print("=" * 120)
        for func in [pickle_serde, numbin_serde, numpy_save_load]:
            display_result(func, data)

    print(">>> benchmark for normal data mixed with numpy array")
    for data in generate_data():
        print("=" * 120)
        for func in [pickle_serde, nbmsg_serde]:
            display_result(func, data)


if __name__ == "__main__":
    benchmark()
