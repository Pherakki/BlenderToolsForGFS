import os

from . import Base


class CounterBase(Base.IBinaryParser):
    def __init__(self):
        super().__init__()
        self.offset = 0

    def global_tell(self):
        return self.offset

    def global_seek(self, offset, whence=os.SEEK_SET):
        if whence == os.SEEK_SET:
            self.offset = offset
        elif whence == os.SEEK_CUR:
            self.offset += offset
        else:
            raise ValueError(f"Invalid whence operation '{whence}'")

    def advance_offset(self, value):
        self.offset += value
    
    @staticmethod
    def _get_rw_method(descriptor):
        return descriptor.count
