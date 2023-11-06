from . import NodeAttachmentBinary
from . import Interface
from . import Mesh
from . import Camera
from . import Light
from . import EPL
from . import EPLLeaf
from . import Morph


class SceneGraphInterface:
    def __init__(self):
        self.nodes      = []
        self.meshes     = []
        self.cameras    = []
        self.lights     = []
        self.epls       = []
        self.epl_leaves = []
    
    @classmethod
    def flattened(cls, binary):
        fn = binary.flattened()
        instance = cls()
        
        instance.nodes      = [Interface.NodeInterface   .from_binary(nb,  p) for p,  nb in zip(fn.node_parents, fn.nodes)]
        instance.meshes     = [Mesh     .MeshInterface   .from_binary(ni,  m) for ni,  m in fn.meshes]
        instance.cameras    = [Camera   .CameraInterface .from_binary(ni,  c) for ni,  c in fn.cameras]
        instance.lights     = [Light    .LightInterface  .from_binary(ni,  l) for ni,  l in fn.lights]
        instance.epls       = [EPL      .EPLInterface    .from_binary(ni,  e) for ni,  e in fn.epls]
        instance.epl_leaves = [EPLLeaf  .EPLLeafInterface.from_binary(ni, el) for ni, el in fn.epl_leaves]
        
        return instance
    
    def packed(self):
        node_list       = self.nodes
        mesh_list       = self.meshes
        camera_list     = self.cameras 
        light_list      = self.lights
        epl_list        = self.epls
        epl_leaves_list = self.epl_leaves
        
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
        node_list[0]._push_node_into_tree(0, node_children, node_collection, id_map)
        
        def add_attachments(typename, typevalue, element_list):
            binaries = []
            for i, elem in enumerate(element_list):
                if elem.node < 0:
                    raise ValueError(f"{typename} {i} has an invalid node parent: {elem.node} must be >= 0")

                # Don't remap the nodes since node_collection is in the
                # Interface order, not the Binary order.
                #remapped_node = id_map[elem.node]
                node = node_collection[elem.node]
                attachment = NodeAttachmentBinary.NodeAttachmentBinary()
                attachment.type = typevalue
                attachment.data = elem.to_binary()
                node.attachments.append(attachment)
                node.attachment_count += 1
                binaries.append((attachment.data, elem.node))
            return binaries
                
        add_attachments("Morph",  9, generate_morphs(node_list, mesh_list))
        mesh_binaries = add_attachments("Mesh",   4, mesh_list)
        add_attachments("Camera",   5, camera_list)
        add_attachments("Light",    6, light_list)
        add_attachments("EPL",      7, epl_list)
        add_attachments("EPLeaves", 8, epl_leaves_list)
        
        return node_collection[0], id_map, mesh_binaries


def generate_morphs(node_list, mesh_list):
    out = []
    for mesh in mesh_list:
        if len(mesh.morphs):
            mi = Morph.MorphInterface()
            mi.node = mesh.node
            binary = Morph.MorphBinary(endianness='>')
            binary.target_count = len(mesh.morphs)
            binary.targets      = [0]*binary.target_count  # Always seems to be 0...
            binary.parent_name  = binary.parent_name.from_name(node_list[mi.node].name)
            mi.binary = binary
            out.append(mi)
    return out
