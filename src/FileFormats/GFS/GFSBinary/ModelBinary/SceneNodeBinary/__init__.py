from ......serialization.Serializable import Serializable
from .NodeAttachmentBinary import NodeAttachmentBinary
from .PropertyBinary import PropertyBinary


class SceneNodeBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.name = None
        self.hash = None
        self.position = None
        self.rotation = None
        self.scale = None
        self.attachment_count = None
        self.attachments = None
        self.has_properties = None
        self.properties = None
        self.property_count = None
        self.float = 1.0
        self.child_count = None
        
        self.children = []
        
    def __repr__(self):
        return f"[GFD::SceneContainer::SceneNode] {self.name}, {self.child_count} children"
        
    def read_write(self, rw, node_list): 
        self.name        = rw.rw_uint16_sized_str(self.name)
        self.hash        = rw.rw_uint32(self.hash)
        self.position    = rw.rw_float32s(self.position, 3)
        self.rotation    = rw.rw_float32s(self.rotation, 4)
        self.scale       = rw.rw_float32s(self.scale, 3)
        
        self.attachment_count = rw.rw_uint32(self.attachment_count)
        self.attachments = rw.rw_obj_array(self.attachments, NodeAttachmentBinary, self.attachment_count)
        self.has_properties = rw.rw_uint8(self.has_properties)
        if self.has_properties:
            self.property_count = rw.rw_uint32(self.property_count)
            self.properties = rw.rw_obj_array(self.properties, PropertyBinary, self.property_count)
        self.float = rw.rw_float32(self.float)
        self.child_count = rw.rw_uint32(self.child_count)
        
        self.children = rw.rw_obj_array(self.children, SceneNodeBinary, self.child_count, node_list)
