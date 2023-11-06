from .EPLLeafBinary import EPLLeafBinary


class EPLLeafInterface:
    def __init__(self):
        self.node = None
        self.binary = None
        
    @classmethod
    def from_binary(self, node_idx, binary):
        self.node = node_idx
        self.binary = binary
    
    def to_binary(self):
        return self.binary
