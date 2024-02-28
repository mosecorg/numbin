"""Serde for NumPy ndarray."""

import struct
from io import BytesIO
from typing import IO

import numpy as np

NP_TYPE = [
    "bool",
    "int8",
    "int16",
    "int32",
    "int64",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
    "float16",
    "float32",
    "float64",
    "float128",
    "complex64",
    "complex128",
    "complex256",
]
TYPE_TO_INDEX = dict((t, i) for (i, t) in enumerate(NP_TYPE, start=1))
INDEX_TO_TYPE = dict((i, t) for (i, t) in enumerate(NP_TYPE, start=1))
BYTE_ORDER = "<"
DIM_FORMAT = "H"
SHAPE_FORMAT = "H"
INDEX_FORMAT = "H"
INDEX_DIM_SIZE = 4
SHAPE_SIZE = 2


class NumBin:
    """Binary serialization for numerical data.

    It only supports NumPy ndarray type.
    """

    def dump(self, array: np.ndarray, fp: IO[bytes]):
        """Serialize NumPy array to binary and write to the file."""
        fp.write(self.dumps(array))

    def load(self, fp: IO[bytes]) -> np.ndarray:
        """Read binary from the file and deserialize to NumPy array."""
        return self.loads(fp.read())

    def dumps(self, array: np.ndarray) -> bytes:
        """Serialize NumPy array to binary.

        | index_type | dim | shape | data |
        """
        shape = array.shape
        index = TYPE_TO_INDEX[array.dtype.name]
        binary = array.tobytes()
        data = BytesIO()
        data.write(struct.pack(f"{BYTE_ORDER}{INDEX_FORMAT}", index))
        data.write(struct.pack(f"{BYTE_ORDER}{DIM_FORMAT}", len(shape)))
        for size in shape:
            data.write(struct.pack(f"{BYTE_ORDER}{SHAPE_FORMAT}", size))
        data.write(binary)
        return data.getvalue()

    def loads(self, binary) -> np.ndarray:
        """Deserialize binary to NumPy array."""
        left, right = 0, INDEX_DIM_SIZE
        view = memoryview(binary)
        index, dim = struct.unpack(
            f"{BYTE_ORDER}{INDEX_FORMAT}{DIM_FORMAT}", view[left:right]
        )
        left += right
        right += dim * SHAPE_SIZE
        shape = struct.unpack(f"{BYTE_ORDER}{dim * SHAPE_FORMAT}", view[left:right])
        array = np.frombuffer(view[right:], dtype=INDEX_TO_TYPE[index])
        array.resize(shape)
        return array


# alias
_nb = NumBin()
loads = _nb.loads
load = _nb.load
dumps = _nb.dumps
dump = _nb.dump
