from io import TextIOWrapper
from typing import Any

import msgpack
import numpy as np

from .codec import NumBin

EXT_CODE = 111
_nb = NumBin()


def ext_hook(code, data):
    if code == EXT_CODE:
        return _nb.loads(data)
    return msgpack.ExtType(code, data)


def _encode(obj):
    if isinstance(obj, np.ndarray):
        return msgpack.ExtType(EXT_CODE, _nb.dumps(obj))
    raise TypeError(f"unknown type: {type(obj)}")


class NumBinMessage(NumBin):
    """Binary serialization as an extension of MsgPack.

    It supports msgpack built-in type and NumPy ndarray.
    """

    def __init__(self) -> None:
        super().__init__()

    def dump(self, obj, fp: TextIOWrapper):
        return super().dump(obj, fp)

    def load(self, fp: TextIOWrapper) -> Any:
        return super().load(fp)

    def dumps(self, obj: Any) -> bytes:
        return msgpack.packb(obj, default=_encode)

    def loads(self, bytes):
        return msgpack.unpackb(bytes, ext_hook=ext_hook, use_list=False)
