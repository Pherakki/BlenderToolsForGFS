from ......serialization.Serializable import Serializable
from ......serialization.utils import safe_format, hex32_format
from ...CommonStructures import BitVector, SceneNodeBinary
from .SkinningDataBinary import SkinningDataBinary


class ModelFlags(BitVector):
    has_bounding_box    = BitVector.DEF_FLAG(0x00)
    has_bounding_sphere = BitVector.DEF_FLAG(0x01)
    has_skin_data       = BitVector.DEF_FLAG(0x02)
    flag_3              = BitVector.DEF_FLAG(0x03)
    flag_4              = BitVector.DEF_FLAG(0x04)
    flag_5              = BitVector.DEF_FLAG(0x05)
    flag_6              = BitVector.DEF_FLAG(0x06)
    flag_7              = BitVector.DEF_FLAG(0x07)
    flag_8              = BitVector.DEF_FLAG(0x08)
    flag_9              = BitVector.DEF_FLAG(0x09)
    flag_10             = BitVector.DEF_FLAG(0x0A)
    flag_11             = BitVector.DEF_FLAG(0x0B)
    flag_12             = BitVector.DEF_FLAG(0x0C)
    flag_13             = BitVector.DEF_FLAG(0x0D)
    flag_14             = BitVector.DEF_FLAG(0x0E)
    flag_15             = BitVector.DEF_FLAG(0x0F)
    flag_16             = BitVector.DEF_FLAG(0x10)
    flag_17             = BitVector.DEF_FLAG(0x11)
    flag_18             = BitVector.DEF_FLAG(0x12)
    flag_19             = BitVector.DEF_FLAG(0x12)
    flag_20             = BitVector.DEF_FLAG(0x14)
    flag_21             = BitVector.DEF_FLAG(0x15)
    flag_22             = BitVector.DEF_FLAG(0x16)
    flag_23             = BitVector.DEF_FLAG(0x17)
    flag_24             = BitVector.DEF_FLAG(0x18)
    flag_25             = BitVector.DEF_FLAG(0x19)
    flag_26             = BitVector.DEF_FLAG(0x1A)
    flag_27             = BitVector.DEF_FLAG(0x1B)
    flag_28             = BitVector.DEF_FLAG(0x1C)
    flag_29             = BitVector.DEF_FLAG(0x1D)
    flag_30             = BitVector.DEF_FLAG(0x1E)
    flag_31             = BitVector.DEF_FLAG(0x1F)


class AttachmentGetter:
    def __init__(self, attachment_type):
        self.attachment_type = attachment_type
        self.attachments = []
        self.current_idx = 0
        
    def __call__(self, node):
        for attachment in node.attachments:
            if attachment.type == self.attachment_type:
                self.attachments.append((self.current_idx, attachment.data))
        self.current_idx += 1


class FlatNodes:
    def __init__(self):
        self.nodes   = []
        self.meshes  = []
        self.cameras = []
        self.lights  = []
        self.epls    = []
        self.morphs  = []


class FlatNodesWalker:
    def __init__(self):
        self.flat_nodes = FlatNodes()
    
    def __call__(self, node):
        fn = self.flat_nodes
        
        idx = len(fn.nodes)
        fn.nodes.append(node)

        for attachment in node.attachments:
            if   attachment.type == 4: lst = fn.meshes
            elif attachment.type == 5: lst = fn.cameras
            elif attachment.type == 6: lst = fn.lights
            elif attachment.type == 7: lst = fn.epls
            elif attachment.type == 9: lst = fn.morphs
            else: raise NotImplementedError("Unhandled attachment type '{atype}' encountered when flattening nodes")
            
            lst.append((idx, attachment.data))


class ModelPayload(Serializable):
    TYPECODE = 0x00010003
         
    APPROVED_VERSIONS = set([
        #0x01104920,
        #0x01105000,
        #0x01105010,
        #0x01105020,
        #0x01105030,
        #0x01105040,
        #0x01105060,
        #0x01105070,
        #0x01105080,
        #0x01105090,
        0x01105100
    ])
    
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags           = ModelFlags(endianness)
        self.skinning_data   = SkinningDataBinary(endianness)
        self.bounding_box_max_dims  = None
        self.bounding_box_min_dims  = None
        self.bounding_sphere_centre = None
        self.bounding_sphere_radius = None
        self.root_node = SceneNodeBinary()
        
    def __repr__(self):
        return f"[GFD::SceneContainer] {safe_format(self.flags._value, hex32_format)}"

    def read_write(self, rw, version):
        self.flags = rw.rw_obj(self.flags)
        
        if self.flags.has_skin_data:
            rw.rw_obj(self.skinning_data)
        if self.flags.has_bounding_box:
            self.bounding_box_max_dims = rw.rw_float32s(self.bounding_box_max_dims, 3)
            self.bounding_box_min_dims = rw.rw_float32s(self.bounding_box_min_dims, 3)
        if self.flags.has_bounding_sphere:
            self.bounding_sphere_centre = rw.rw_float32s(self.bounding_sphere_centre, 3)
            self.bounding_sphere_radius = rw.rw_float32(self.bounding_sphere_radius)
            
        rw.rw_obj(self.root_node, version)
        
    def walk_nodes(self, node, operator):
        operator(node)
        for child in node.children[::-1]:
            self.walk_nodes(child, operator)
    
    def fetch_attachment(self, node, attachment_type):
        ag = AttachmentGetter(attachment_type)
        self.walk_nodes(node, ag)
        return ag.attachments
    
    def get_meshes(self):
        return self.fetch_attachment(self.root_node, 4)
    
    def get_cameras(self):
        return self.fetch_attachment(self.root_node, 5)
    
    def get_lights(self):
        return self.fetch_attachment(self.root_node, 6)
    
    def get_epls(self):
        return self.fetch_attachment(self.root_node, 7)
    
    def get_morphs(self):
        return self.fetch_attachment(self.root_node, 9)
    
    def flattened(self):
        fn = FlatNodesWalker()
        self.walk_nodes(self.root_node, fn)
        return fn.flat_nodes
