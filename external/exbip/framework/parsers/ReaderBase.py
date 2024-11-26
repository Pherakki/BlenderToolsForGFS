import io
import os

from .Base import IBinaryParser
from ..streams import MemoryviewStream


class FileIO:
    def __init__(self, rw, filepath):
        self.rw = rw
        self.filepath = filepath

    def __enter__(self):
        rw = self.rw
        rw._bytestream = open(self.filepath, 'rb')
        rw.read_bytes = rw._bytestream.read
        return rw

    def __exit__(self, exc_type, exc_val, exc_tb):
        rw = self.rw
        rw._bytestream.close()
        rw._bytestream = None
        rw.read_bytes = rw._default_read_bytes


class SSOIO:
    def __init__(self, rw, filepath):
        self.rw = rw
        self.filepath = filepath

    def __enter__(self):
        rw = self.rw
        with open(self.filepath, 'rb', buffering=0) as F:
            rw._bytestream = MemoryviewStream(F.read())
            rw.read_bytes = rw._bytestream.read
        return rw

    def __exit__(self, exc_type, exc_val, exc_tb):
        rw = self.rw
        rw._bytestream = None
        rw.read_bytes = rw._default_read_bytes


class BytestreamIO:
    def __init__(self, rw, initializer):
        self.rw = rw
        self.initializer = initializer

    def __enter__(self):
        rw = self.rw
        rw._bytestream = io.BytesIO(self.initializer)
        rw.read_bytes  = rw._bytestream.read
        return rw

    def __exit__(self, exc_type, exc_val, exc_tb):
        rw = self.rw
        rw._bytestream.close()
        rw._bytestream = None
        rw.read_bytes = rw._default_read_bytes


class ReaderBase(IBinaryParser):
    def __init__(self):
        super().__init__()
        self._bytestream = None

    def global_tell(self):
        return self._bytestream.tell()

    def global_seek(self, offset, whence=os.SEEK_SET):
        return self._bytestream.seek(offset, whence)

    ###########################
    # READER-SPECIFIC METHODS #
    ###########################
    def FileIO(self, filepath):
        return FileIO(self, filepath)

    def SSOIO(self, filepath):
        return SSOIO(self, filepath)

    def BytestreamIO(self, initializer):
        return BytestreamIO(self, initializer)

    def _default_read_bytes(self, length):
        return self._bytestream.read(length)

    read_bytes = _default_read_bytes

    def peek_bytestring(self, length):
        val = self.read_bytes(length)
        self.seek(-len(val), 1)
        return val

    @staticmethod
    def _get_rw_method(descriptor):
        return descriptor.deserialize
