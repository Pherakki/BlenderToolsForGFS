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
    
    @classmethod
    def walk_nodes(cls, node, operator):
        operator.begin(node)
        for child in node.children[::-1]:
            cls.walk_nodes(child, operator)
        operator.end()
    
    @classmethod
    def fetch_attachment(cls, node, attachment_type):
        ag = AttachmentGetter(attachment_type)
        cls.walk_nodes(node, ag)
        return ag.attachments

    def flattened(self):
        fn = FlatNodesWalker()
        self.walk_nodes(self, fn)
        return fn.flat_nodes
    
    def get_meshes    (self): return self.fetch_attachment(self, 4)
    def get_cameras   (self): return self.fetch_attachment(self, 5)
    def get_lights    (self): return self.fetch_attachment(self, 6)
    def get_epls      (self): return self.fetch_attachment(self, 7)
    def get_epl_leaves(self): return self.fetch_attachment(self, 8)
    def get_morphs    (self): return self.fetch_attachment(self, 9)


class FlatNodes:
    def __init__(self):
        self.nodes        = []
        self.node_parents = []
        
        self.meshes       = []
        self.cameras      = []
        self.lights       = []
        self.epls         = []
        self.epl_leaves   = []
        self.morphs       = []


class FlatNodesWalker:
    def __init__(self):
        self.flat_nodes = FlatNodes()
        self.parent_stack = [-1]
    
    def begin(self, node):
        fn = self.flat_nodes
        
        idx = len(fn.nodes)
        fn.nodes.append(node)
        fn.node_parents.append(self.parent_stack[-1])
        self.parent_stack.append(len(fn.nodes)-1)
        
        for attachment in node.attachments:
            if   attachment.type == 4: lst = fn.meshes
            elif attachment.type == 5: lst = fn.cameras
            elif attachment.type == 6: lst = fn.lights
            elif attachment.type == 7: lst = fn.epls
            elif attachment.type == 8: lst = fn.epl_leaves
            elif attachment.type == 9: lst = fn.morphs
            else: raise NotImplementedError("Unhandled attachment type '{atype}' encountered when flattening nodes")
            
            lst.append((idx, attachment.data))

    def end(self):
        self.parent_stack.pop(-1)
        

class AttachmentGetter:
    def __init__(self, attachment_type):
        self.attachment_type = attachment_type
        self.attachments = []
        self.current_idx = 0
        
    def begin(self, node):
        for attachment in node.attachments:
            if attachment.type == self.attachment_type:
                self.attachments.append((self.current_idx, attachment.data))
        self.current_idx += 1
        
    def end(self):
        return