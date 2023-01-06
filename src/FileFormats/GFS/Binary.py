from ...serialization.Serializable import Serializable
from .SubComponents.GFS0ContainerBinary import GFS0ContainerBinary


class GFSBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.magic = b'GFS0'
        self.containers = []
        
    def __repr__(self):
        return f"[GFS] Has {len(self.containers)} container{'' if len(self.containers) == 1 else 's'}"
        
    def read_write(self, rw):
        self.magic      = rw.rw_bytestring(self.magic, 4)
        rw.assert_equal(self.magic, b'GFS0')
        
        if rw.mode() == "read":
            finished = False
            while not finished:
                # Validation variable
                start_offset = rw.tell()
                
                # Read the data
                ctr = GFS0ContainerBinary()
                self.containers.append(ctr)
                rw.rw_obj(ctr)
                
                # Validate container size
                if ctr.size:
                    rw.assert_equal(ctr.size, rw.tell() - start_offset)
                
                # Check if final container
                if rw.peek_bytestring(1) == b'':
                    finished = True
                    
            # Check there's no more data
            rw.assert_at_eof()
                
        else:
            for ctr in self.containers:
                rw.rw_obj(ctr)