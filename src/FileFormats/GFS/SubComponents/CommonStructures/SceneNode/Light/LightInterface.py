from .LightBinary import LightBinary

    
class LightInterface:
    def __init__(self):
        self.node   = None
        self.binary = LightBinary()
        
    @classmethod
    def from_binary(cls, node_idx, binary):
        instance = cls()
        
        # Deal with unpacking later...
        instance.node = node_idx
        instance.binary = binary
        
        return instance
        
    def to_binary(self):
        return self.binary
