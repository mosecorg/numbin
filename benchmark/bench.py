from __future__ import annotations
from functools import partial

import gc
import pickle
import subprocess
import traceback
from dataclasses import dataclass
from io import BytesIO
from time import perf_counter
from typing import List

import msgpack
import msgpack_numpy
import numpy as np
from safetensors.numpy import load as st_load
from safetensors.numpy import save as st_save

from numbin import NumBin
from numbin.msg_ext import NumBinMessage

import redis
from pyarrow import plasma


class PlasmaShmWrapper:
    def __init__(self, shm_path: str) -> None:
        self.client = plasma.connect(shm_path)

    def _put_plasma(self, data: List[bytes]) -> List[plasma.ObjectID]:
        return [self.client.put(x) for x in data]

    def _get_plasma(self, object_ids: List[plasma.ObjectID]) -> List[bytes]:
        objects = self.client.get(object_ids)
        self.client.delete(object_ids)
        return objects

    def put(self, data: List[bytes]) -> List[bytes]:
        object_ids = self._put_plasma(data)
        return [id.binary() for id in object_ids]

    def get(self, ids: List[bytes]) -> List[bytes]:
        object_ids = [plasma.ObjectID(id) for id in ids]
        return self._get_plasma(object_ids)


class RedisWrapper:
    def __init__(self, url: str = "") -> None:
        self.client = redis.from_url(url)

    def put(self, data: List[bytes]) -> List[int]:
        ids = []
        for item in data:
            _id = self.client.incr("test")
            self.client.set(_id, item)
        return ids

    def get(self, object_ids: List[str]) -> List[bytes]:
        datas = []
        for id in object_ids:
            datas.append(self.client.get(id))
        return datas


class RedisPipelineWrapper:
    def __init__(self, url: str = "") -> None:
        self.client = redis.from_url(url)

    def put(self, data: List[bytes]) -> List[int]:
        with self.client.pipeline() as p:
            for _ in range(len(data)):
                p.incr("test")
            ids = p.execute()

            for idx, id in enumerate(ids):
                p.set(id, data[idx])
            p.execute()
        return ids

    def get(self, object_ids: List[str]) -> List[bytes]:
        with self.client.pipeline() as p:
            for id in object_ids:
                p.get(id)
            return p.execute()


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


def generate_store_data():
    return (
        Data(
            {"msg": "long message" * 1000, "vec": np.random.rand(1024)},
            "long message with 1024 vector",
            10,
        ),
        Data(
            {
                "int": 233,
                "float": 3.14,
                "vec": np.random.rand(1024),
                "matrix": np.random.rand(64, 1024),
            },
            "int, float, vector and matrix",
            10,
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


def generate_store_np_data():
    return (
        Data(np.random.rand(1), "scalar", 100),
        Data(np.random.rand(1024), "vector", 100),
        Data(np.random.rand(64, 1024), "matrix", 100),
        Data(np.random.rand(3, 1024, 1024), "image", 10),
        Data(np.random.rand(64, 3, 1024, 1024), "batch of images", 5),
    )


def pickle_serde(data: Data):
    pickle.loads(
        pickle.dumps(data.arr, fix_imports=False, protocol=pickle.HIGHEST_PROTOCOL),
        fix_imports=False,
    )


def safets_serde(data: Data):
    st_load(st_save({"": data.arr}))[""]


def numbin_serde(data: Data):
    nb.loads(nb.dumps(data.arr))


def nbmsg_serde(data: Data):
    nbm.loads(nbm.dumps(data.arr))


def numpy_serde(data: Data):
    fp = BytesIO()
    np.save(fp, data.arr, allow_pickle=False, fix_imports=False)
    fp.seek(0)
    np.load(fp, allow_pickle=False, fix_imports=False)


def msg_np_serde(data: Data):
    msgpack.unpackb(
        msgpack.packb(data.arr, default=msgpack_numpy.encode),
        object_hook=msgpack_numpy.decode,
    )


def plasma_store(duplicate: int, data: Data):
    global plasam_client
    ids = plasam_client.put([pickle.dumps(data.arr)] * duplicate)
    plasam_client.get(ids)


def redis_store(duplicate: int, data: Data):
    global redis_client
    ids = redis_client.put([pickle.dumps(data.arr)] * duplicate)
    redis_client.get(ids)


def redis_pipeline_store(duplicate: int, data: Data):
    global redis_pipeline_client
    ids = redis_client.put([pickle.dumps(data.arr)] * duplicate)
    redis_client.get(ids)


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
    socket_path = "/tmp/bench.redis.sock"
    with plasma.start_plasma_store(plasma_store_memory=2000 * 1000 * 1000) as (
        shm_path,
        proc,
    ), subprocess.Popen(
        ["redis-server", "--unixsocket", socket_path, "--port", "0"]
    ) as proc:
        global plasam_client, redis_client, redis_pipeline_client
        plasam_client = PlasmaShmWrapper(shm_path)
        redis_client = RedisWrapper(f"unix://{socket_path}")
        redis_pipeline_client = RedisPipelineWrapper(f"unix://{socket_path}")
        print(">>> benchmark for numpy array")

        store_funcs = []
        for duplicate in range(1, 1100, 500):
            for f in [plasma_store, redis_store, redis_pipeline_store]:
                fd = partial(f, duplicate)
                fd.__name__ = f"{f.__name__}_{duplicate}"
                store_funcs.append(fd)

        for data, store_np_data in zip(generate_np_data(), generate_store_np_data()):
            print("=" * 120)
            for func in [
                pickle_serde,
                numbin_serde,
                numpy_serde,
                safets_serde,
                msg_np_serde,
            ]:
                display_result(func, data)
            for func in store_funcs:
                display_result(func, store_np_data)

        print(">>> benchmark for normal data mixed with numpy array")
        for data, store_data in zip(generate_data(), generate_store_data()):
            print("=" * 120)
            for func in [pickle_serde, nbmsg_serde]:
                display_result(func, data)
            for func in store_funcs:
                display_result(func, store_data)


if __name__ == "__main__":
    benchmark()
