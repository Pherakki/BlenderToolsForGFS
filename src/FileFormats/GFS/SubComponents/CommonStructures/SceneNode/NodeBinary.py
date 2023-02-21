from ......serialization.Serializable import Serializable
from ...CommonStructures import ObjectName, PropertyBinary
from ...CommonStructures.SizedObjArrayModule import SizedObjArray
from .NodeAttachmentBinary import NodeAttachmentBinary


class SceneNodeBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.name = ObjectName()
        self.position = None
        self.rotation = None
        self.scale = None
        self.attachment_count = 0
        self.attachments = []
        self.has_properties = None
        self.properties = SizedObjArray(PropertyBinary)
        self.float = 1.0
        
        self.children = SizedObjArray(SceneNodeBinary)
        
    def __repr__(self):
        return f"[GFD::SceneContainer::SceneNode] {self.name}, {self.attachment_count} attachments, {self.properties.count} properties, {self.children.count} children"
        
    def read_write(self, rw, version):
        self.name        = rw.rw_obj(self.name, version)
        self.position    = rw.rw_float32s(self.position, 3)
        self.rotation    = rw.rw_float32s(self.rotation, 4)
        self.scale       = rw.rw_float32s(self.scale, 3)
        
        self.attachment_count = rw.rw_uint32(self.attachment_count)
        self.attachments = rw.rw_obj_array(self.attachments, NodeAttachmentBinary, self.attachment_count, type(self), version)
        self.has_properties = rw.rw_uint8(self.has_properties)
        if self.has_properties:
            rw.rw_obj(self.properties, version)
        self.float = rw.rw_float32(self.float)
        
        rw.rw_obj(self.children, version)
