import os


class MemoryviewStream:
    def __init__(self, buffer=None):
        self.offset = 0
        self.buffer = memoryview(buffer) if buffer is not None else None
    
    def read(self, size):
        o = self.offset
        return self.buffer[o:o+size]
    
    def seek(self, offset, whence=os.SEEK_SET):
        if whence==os.SEEK_SET:
            self.offset = offset
        elif whence==os.SEEK_CUR:
            self.offset += offset
        elif whence==os.SEEK_END:
            self.offset = len(self.buffer) - offset
        else:
            raise ValueError(f"invalid whence ({whence}, should be 0, 1 or 2)")
    
    def tell(self):
        return self.offset
