"""Extend msgpack to support NumPy ndarray."""

from typing import IO, Any

import msgpack
import numpy as np

from .codec import NumBin

EXT_CODE = 111
_nb = NumBin()


def ext_hook(code, data):
    """Msgapck hook to handle NumPy ndarray."""
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

    This requires extra dependencies: `pip install numbin[msgpack]`
    """

    def dump(self, obj, fp: IO[bytes]):
        """Serialize to binary and write to the file."""
        return super().dump(obj, fp)

    def load(self, fp: IO[bytes]) -> Any:
        """Read binary from the file and deserialize to NumPy array."""
        return super().load(fp)

    def dumps(self, obj: Any) -> bytes:
        """Serialize to binary."""
        return msgpack.packb(obj, default=_encode)

    def loads(self, buf: bytes):
        """Deserialize binary data to NumPy array."""
        return msgpack.unpackb(buf, ext_hook=ext_hook, use_list=False)


# alias
_nbm = NumBinMessage()
loads = _nbm.loads
load = _nbm.load
dumps = _nbm.dumps
dump = _nbm.dump
