import io
import os

from .Base import IBinaryParser
from ..streams import MemoryviewStream


class ValidatorStream:
    class ValidationError(Exception):
        def __init__(self, msg):
            super().__init__(msg)
    
    def __init__(self):
        self._primary_stream   = None
        self._reference_stream = None
    
    def set_primary_stream(self, stream):
        self._primary_stream = stream
        
    def set_reference_stream(self, stream):
        self._reference_stream = stream
    
    def close(self):
        if self._primary_stream is not None:
            self._primary_stream.close()
            self._primary_stream = None
        if self._reference_stream is not None:
            self._reference_stream.close()
            self._reference_stream = None
    
    def seek(self, offset, whence=os.SEEK_SET):
        self._primary_stream  .seek(offset, whence)
        self._reference_stream.seek(offset, whence)

    def tell(self):
        return self._primary_stream.tell()
    
    def read(self, count):
        data    = self._primary_stream.read(count)
        refdata = self._reference_stream.read(count)
        if data != refdata:
            raise self.ValidationError(f"Read {data} from primary stream, reference data is {refdata}")
        return data
    
    def write(self, data):
        raise NotImplementedError


class PrimaryFileIO:
    def __init__(self, rw, filepath):
        self.rw = rw
        self.rw._bytestream.set_primary_stream(open(filepath, 'rb'))

    def __enter__(self):
        return self.rw

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rw._bytestream.close()


class PrimarySSOIO:
    def __init__(self, rw, filepath):
        self.rw = rw
        with open(filepath, 'rb', buffering=0) as F:
            self.rw._bytestream.set_primary_stream(MemoryviewStream(F.read()))

    def __enter__(self):
        return self.rw

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rw._bytestream.close()


class PrimaryBytestreamIO:
    def __init__(self, rw, initializer):
        self.rw = rw
        self.rw._bytestream.set_primary_stream(io.BytesIO(initializer))

    def __enter__(self):
        return self.rw

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rw._bytestream.close()


class ReferenceFileIO:
    def __init__(self, rw, filepath):
        self.rw = rw
        self.rw._bytestream.set_reference_stream(open(filepath, 'rb'))

    def __enter__(self):
        return self.rw

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rw._bytestream.close()


class ReferenceSSOIO:
    def __init__(self, rw, filepath):
        self.rw = rw
        with open(filepath, 'rb', buffering=0) as F:
            self.rw._bytestream.set_reference_stream(MemoryviewStream(F.read()))

    def __enter__(self):
        return self.rw

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rw._bytestream.close()


class ReferenceBytestreamIO:
    def __init__(self, rw, initializer):
        self.rw = rw
        self.rw._bytestream.set_reference_stream(io.BytesIO(initializer))

    def __enter__(self):
        return self.rw

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rw._bytestream.close()


class ValidatorBase(IBinaryParser):
    def __init__(self):
        super().__init__()
        self._bytestream = ValidatorStream()

    def global_tell(self):
        return self._bytestream.tell()

    def global_seek(self, offset, whence=os.SEEK_SET):
        return self._bytestream.seek(offset, whence)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._bytestream.close()

    ##############################
    # VALIDATOR-SPECIFIC METHODS #
    ##############################
    def PrimaryFileIO(self, filepath):
        PrimaryFileIO(self, filepath)
        return self

    def PrimarySSOIO(self, filepath):
        PrimarySSOIO(self, filepath)
        return self

    def PrimaryBytestreamIO(self, initializer):
        PrimaryBytestreamIO(self, initializer)
        return self
    
    def ReferenceFileIO(self, filepath):
        ReferenceFileIO(self, filepath)
        return self

    def ReferenceSSOIO(self, filepath):
        ReferenceSSOIO(self, filepath)
        return self

    def ReferenceBytestreamIO(self, initializer):
        ReferenceBytestreamIO(self, initializer)
        return self
    
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
