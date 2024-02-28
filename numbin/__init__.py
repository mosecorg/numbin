"""NumBin is a binary serialization format for numerical data."""

from .codec import NumBin, dump, dumps, load, loads

__all__ = ["NumBin", "dumps", "dump", "loads", "load"]
