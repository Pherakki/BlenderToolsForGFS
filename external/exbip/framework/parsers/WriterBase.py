import io
import os

from . import Base


class FileIO:
    def __init__(self, rw, filepath):
        self.rw = rw
        self.filepath = filepath

    def __enter__(self):
        self.rw._bytestream = open(self.filepath, 'wb')
        return self.rw

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rw._bytestream.close()
        self.rw._bytestream = None


class BytestreamIO:
    def __init__(self, rw):
        self.rw = rw

    def __enter__(self):
        self.rw._bytestream = io.BytesIO()
        return self.rw

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rw._bytestream.close()
        self.rw._bytestream = None


class WriterBase(Base.IBinaryParser):
    def __init__(self):
        super().__init__()
        self._bytestream = None

    def global_tell(self):
        return self._bytestream.tell()

    def global_seek(self, offset, whence=os.SEEK_SET):
        return self._bytestream.seek(offset, whence)

    def FileIO(self, filepath):
        return FileIO(self, filepath)

    ######
    # PRE-CALCULATE FILE SIZE, CREATE BUFFER WITH THAT SIZE,
    # WRITE TO BUFFER WITHOUT NEED FOR RE-ALLOCATION,
    # SAVE BUFFER!!!

    def BytestreamIO(self):
        return BytestreamIO(self)

    def write_bytes(self, value):
        return self._bytestream.write(value)
    
    @staticmethod
    def _get_rw_method(descriptor):
        return descriptor.serialize
