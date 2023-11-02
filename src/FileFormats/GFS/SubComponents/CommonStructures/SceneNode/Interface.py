from ..CustomProperty import PropertyInterface
from .NodeAttachmentBinary import NodeAttachmentBinary
from .NodeBinary import SceneNodeBinary
from .Mesh   import MeshInterface
from .Light  import LightInterface
from .Camera import CameraInterface
from .Morph  import MorphInterface, MorphBinary


def generate_morphs(node_list, mesh_list):
    out = []
    for mesh in mesh_list:
        if len(mesh.morphs):
            mi = MorphInterface()
            mi.node = mesh.node
            binary = MorphBinary(endianness='>')
            binary.target_count = len(mesh.morphs)
            binary.targets      = [0]*binary.target_count  # Always seems to be 0...
            binary.parent_name  = binary.parent_name.from_name(node_list[mi.node].name)
            mi.binary = binary
            out.append(mi)
    return out

        
class NodeInterface:
    def __init__(self):
        self.parent_idx       = None
        self.name             = None
        self.position         = None
        self.rotation         = None
        self.scale            = None
        self.bind_pose_matrix = None
        self.unknown_float    = None
        self.properties       = [] # Property interfaces?
    
    @classmethod
    def binary_node_tree_to_list(cls, binary):
        node_list        = []
        mesh_list        = []
        camera_list      = []
        light_list       = []
        #morph_list       = []
        epl_list         = []
        cls._fetch_node_from_tree(binary, -1, node_list, mesh_list, camera_list, light_list, epl_list)
        
        return node_list, mesh_list, camera_list, light_list, epl_list
        
    @classmethod
    def _fetch_node_from_tree(cls, node, parent, node_list, mesh_list, camera_list, light_list, epl_list):
        node_idx = len(node_list)
        node_list.append(cls.from_binary(node, parent))
        for attachment in node.attachments:
            if attachment.type == 4:
                mesh_list.append(MeshInterface.from_binary(node_idx, attachment.data))
            elif attachment.type == 5:
                camera_list.append(CameraInterface.from_binary(node_idx, attachment.data))
            elif attachment.type == 6:
                light_list.append(LightInterface.from_binary(node_idx, attachment.data))
            elif attachment.type == 7:
                epl_list.append(EPLInterface.from_binary(node_idx, attachment.data))
            elif attachment.type == 9:
                pass
            #     morph_list.append(MorphInterface.from_binary(node_idx, attachment.data))
            else:
                raise NotImplementedError("No Interface exists for attachment type '{attachment.type}'")
        for child in node.children[::-1]:
            cls._fetch_node_from_tree(child, node_idx, node_list, mesh_list, camera_list, light_list, epl_list)
    
    @classmethod
    def list_to_binary_node_tree(cls, node_list, mesh_list, camera_list, light_list, epl_list):
        node_children = {}
        # First not in list required to be root
        # Should probably throw in a check here to make sure...
        # Although, frankly, it's probably smarter to remove root from the list
        # and have an implicit root node.
        for i, node in enumerate(node_list[1:]):
            n_id = node.parent_idx
            if n_id not in node_children:
                node_children[n_id] = []
            node_children[n_id].append(i+1)
        id_map = {0: 0}
        node_collection = [node.to_binary() for node in node_list]
        
        # Need to clear the node children for now, until every node is actually
        # built from scratch
        for node in node_collection:
            node.children.clear()
            node.attachments.clear()
        cls._push_node_into_tree(0, node_children, node_collection, id_map)
        
        def add_attachments(typename, typevalue, element_list):
            binaries = []
            for i, elem in enumerate(element_list):
                if elem.node < 0:
                    raise ValueError(f"{typename} {i} has an invalid node parent: {elem.node} must be >= 0")

                # Don't remap the nodes since node_collection is in the
                # Interface order, not the Binary order.
                #remapped_node = id_map[elem.node]
                node = node_collection[elem.node]
                attachment = NodeAttachmentBinary()
                attachment.type = typevalue
                attachment.data = elem.to_binary()
                node.attachments.append(attachment)
                node.attachment_count += 1
                binaries.append((attachment.data, elem.node))
            return binaries
                
        add_attachments("Morph",  9, generate_morphs(node_list, mesh_list))
        mesh_binaries = add_attachments("Mesh",   4, mesh_list)
        add_attachments("Camera", 5, camera_list)
        add_attachments("Light",  6, light_list)
        add_attachments("EPL",    7, epl_list)
        
        return node_collection[0], id_map, mesh_binaries
    
    @classmethod
    def _push_node_into_tree(cls, node_idx, node_children, node_collection, id_map):
        child_node_idxs = node_children.get(node_idx, [])
        for cn_id in child_node_idxs:
            id_map[cn_id] = len(id_map)
            node_collection[node_idx].children.insert(0, node_collection[cn_id])
            cls._push_node_into_tree(cn_id, node_children, node_collection, id_map)

    @classmethod
    def from_binary(cls, binary, parent_idx, bind_pose_matrix=None):
        instance = cls()
        
        instance.parent_idx = parent_idx
        instance.name = binary.name.string
        instance.position = binary.position
        instance.rotation = binary.rotation
        instance.scale = binary.scale
        instance.bind_pose_matrix = bind_pose_matrix
        instance.unknown_float = binary.float
        instance.properties = [PropertyInterface.from_binary(prop) for prop in binary.properties.data]
        
        return instance
    
    def to_binary(self):
        binary = SceneNodeBinary()
        
        binary.name = binary.name.from_name(self.name)
        binary.position = self.position
        binary.rotation = self.rotation
        binary.scale = self.scale
        binary.float = self.unknown_float
        binary.has_properties = len(self.properties) > 0
        binary.properties.data = [prop.to_binary() for prop in self.properties]
        binary.properties.count = len(self.properties)
        
        return binary
    
    def add_property(self, name, dtype, data):
        prop = PropertyInterface()
        prop.name = name
        prop.type = dtype
        prop.data = data
        self.properties.append(prop)
        return prop


class EPLInterface:
    def __init__(self):
        self.node = None
        self.binary = None
        
    @classmethod
    def from_binary(cls, node_idx, binary):
        instance = cls()
        
        instance.node = node_idx
        instance.binary = binary
        
        return instance
    
    def to_binary(self):
        return self.binary
