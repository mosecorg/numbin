import struct
from io import BytesIO
from typing import IO

import numpy as np

NP_TYPE = [
    np.dtype("bool"),
    np.dtype("int8"),
    np.dtype("int16"),
    np.dtype("int32"),
    np.dtype("int64"),
    np.dtype("uint8"),
    np.dtype("uint16"),
    np.dtype("uint32"),
    np.dtype("uint64"),
    np.dtype("float16"),
    np.dtype("float32"),
    np.dtype("float64"),
    np.dtype("float128"),
    np.dtype("complex64"),
    np.dtype("complex128"),
    np.dtype("complex256"),
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

    def __init__(self) -> None:
        pass

    def dump(self, array: np.ndarray, fp: IO[bytes]):
        fp.write(self.dumps(array))

    def load(self, fp: IO[bytes]) -> np.ndarray:
        return self.loads(fp.read())

    def dumps(self, array: np.ndarray) -> bytes:
        """Serialize NumPy array to binary.

        | index_type | dim | shape | data |
        """
        shape = array.shape
        index = TYPE_TO_INDEX[array.dtype]
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
