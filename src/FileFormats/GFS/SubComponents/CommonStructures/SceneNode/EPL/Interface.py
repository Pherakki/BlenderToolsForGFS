from .EPLBinary import EPLFlags, EPLBinary
from .. import SceneGraphInterface


class EPLInterface:
    def __init__(self):
        self.node = None
        
        self.flags       = EPLFlags()
        self._scenegraph = SceneGraphInterface.SceneGraphInterface()
        self.animation   = None
        self.unknown     = 0
    
    @property
    def nodes(self):
        return self._scenegraph.nodes
    @nodes.setter
    def nodes(self, value):
        self._scenegraph.nodes = value
    
    @property
    def leaves(self):
        return self._scenegraph.epl_leaves
    @leaves.setter
    def leaves(self, value):
        self._scenegraph.epl_leaves = value
        
    @classmethod
    def from_binary(cls, node_idx, binary):
        instance = cls()
        
        instance._scenegraph = instance._scenegraph.flattened(binary.root_node)
        
        if len(instance._scenegraph.meshes):  print("WARNING: EPL has meshes!")
        if len(instance._scenegraph.cameras): print("WARNING: EPL has cameras!")
        if len(instance._scenegraph.lights):  print("WARNING: EPL has lights!")
        if len(instance._scenegraph.epls):    print("WARNING: EPL has sub-EPLs!")
        
        instance.flags     = binary.flags
        instance.node      = node_idx
        instance.animation = binary.animation
        instance.unknown   = binary.unknown
        
        return instance
    
    def to_binary(self):
        binary = EPLBinary()
        binary.flags = self.flags
        binary.root_node = self._scenegraph.packed()[0]
        if self.animation is not None:
            binary.animation = self.animation
        binary.unknown = self.unknown
        
        return binary
