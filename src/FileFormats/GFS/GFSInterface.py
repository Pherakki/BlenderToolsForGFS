import copy

from ...serialization.BinaryTargets import OffsetTracker
from .GFSBinary import GFS0Binary
from .GFSBinary.CommonStructures import ObjectName, PropertyBinary
from .GFSBinary.GFS0ContainerBinary import GFS0ContainerBinary, SizedObjArray
from .GFSBinary.ModelBinary import ModelBinary
from .GFSBinary.ModelBinary.SceneNodeBinary import SceneNodeBinary
from .GFSBinary.ModelBinary.SceneNodeBinary.MeshBinary import MeshBinary
from .GFSBinary.ModelBinary.SceneNodeBinary.NodeAttachmentBinary import NodeAttachmentBinary
from .Utils.Matrices import transforms_to_matrix, multiply_transform_matrices, are_matrices_close, invert_transform_matrix

from .MaterialInterface import MaterialInterface, MaterialBinary
from .GFSBinary.Textures import TextureInterface, TextureBinary
from .AnimationInterface import AnimationInterface


class GFSInterface:
    def __init__(self):
        self.keep_bounding_box = False
        self.keep_bounding_sphere = False
        self.meshes = []
        self.cameras = []
        self.lights = []
        self.bones = []
        self.materials = []
        self.textures = []
        self.animations = []
        
        # Things that need to be removed eventually
        self.animation_data  = None
        self.data_0x000100F8 = None
        self.physics_data    = None


    @classmethod
    def from_file(cls, filepath):
        binary = GFS0Binary()
        binary.read(filepath)
        return cls.from_binary(binary, duplicate_data=False)

    @classmethod
    def from_binary(cls, binary, duplicate_data=True):
        instance = cls()
        
        for ctr in binary.containers:
            if ctr.type == 0x000100FC:
                instance.textures = [TextureInterface.from_binary(tx) for tx in ctr.data]
            elif ctr.type == 0x000100FB:
                instance.materials = [MaterialInterface.from_binary(mb) for mb in ctr.data]
            elif ctr.type == 0x00010003:
                # Wrong but it will do as an approximation for now
                # Need to include other data types in export
                instance.bones,             \
                instance.meshes,            \
                instance.cameras,           \
                instance.lights,            \
                instance.keep_bounding_box, \
                instance.keep_bounding_sphere = ModelInterface.from_binary(ctr.data, duplicate_data)
            elif ctr.type == 0x000100FD:
                instance.animation_data = ctr.data
                instance.animations = [AnimationInterface.from_binary(anim) for anim in ctr.data.animations]
            elif ctr.type == 0x000100F8:
                instance.data_0x000100F8 = ctr.data
            elif ctr.type == 0x000100F9:
                instance.physics_data = ctr.data
        
        return instance
    
    def to_binary(self, duplicate_data=False):
        binary = GFS0Binary()
        
        ot = OffsetTracker()
        
        # Start container
        start_ctr = GFS0ContainerBinary()
        start_ctr.version = 0x01105100
        start_ctr.type = 0x00000001
        ot.rw_obj(start_ctr)
        start_ctr.size = 0
        binary.containers.append(start_ctr)
        
        # Textures container
        if len(self.materials): # Unless textures are stored externally?
            offset = ot.tell()
            tex_ctr = GFS0ContainerBinary()
            tex_ctr.version = 0x01105100
            tex_ctr.type = 0x000100FC
            
            tex_array = SizedObjArray(TextureBinary)
            tex_array.data = [ti.to_binary() for ti in self.textures]
            tex_array.count = len(tex_array.data)
            tex_ctr.data = tex_array
            ot.rw_obj(tex_ctr)
            tex_ctr.size = ot.tell() - offset
            binary.containers.append(tex_ctr)
            
        # Materials container
        if len(self.materials):
            offset = ot.tell()
            mat_ctr = GFS0ContainerBinary()
            mat_ctr.version = 0x01105100
            mat_ctr.type = 0x000100FB
            
            mat_array = SizedObjArray(MaterialBinary)
            mat_array.data = [mi.to_binary() for mi in self.materials]
            mat_array.count = len(mat_array.data)
            mat_ctr.data = mat_array
            ot.rw_obj(mat_ctr)
            mat_ctr.size = ot.tell() - offset
            binary.containers.append(mat_ctr)
            
        # Model container
        if len(self.bones):
            offset = ot.tell()
            mdl_ctr = GFS0ContainerBinary()
            mdl_ctr.version = 0x01105100
            mdl_ctr.type = 0x00010003
            
            model_binary = ModelInterface.to_binary(self.bones, self.meshes, self.cameras, self.lights, self.keep_bounding_box, self.keep_bounding_sphere, copy_verts=duplicate_data)
            mdl_ctr.data = model_binary
            ot.rw_obj(mdl_ctr)
            mdl_ctr.size = ot.tell() - offset
            binary.containers.append(mdl_ctr)
                    
        # Animation container
        if self.animation_data is not None:
            offset = ot.tell()
            anm_ctr = GFS0ContainerBinary()
            anm_ctr.version = 0x01105100
            anm_ctr.type = 0x000100FD
            
            anm_ctr.data = self.animation_data
            ot.rw_obj(anm_ctr)
            anm_ctr.size = ot.tell() - offset
            binary.containers.append(anm_ctr)
            
        # Physics container
        if self.physics_data is not None:
            offset = ot.tell()
            physics_ctr = GFS0ContainerBinary()
            physics_ctr.version = 0x01105100
            physics_ctr.type = 0x000100F9
            
            physics_ctr.data = self.physics_data
            ot.rw_obj(physics_ctr)
            physics_ctr.size = ot.tell() - offset
            binary.containers.append(physics_ctr)
            
        # Unknown container
        if self.data_0x000100F8 is not None:
            offset = ot.tell()
            unk_ctr = GFS0ContainerBinary()
            unk_ctr.version = 0x01105100
            unk_ctr.type = 0x000100F8
            
            unk_ctr.data = self.data_0x000100F8
            unk_ctr.size = len(self.data_0x000100F8.data) + 0x10
            # ot.rw_obj(unk_ctr)
            # unk_ctr.size = ot.tell() - offset
            binary.containers.append(unk_ctr)
        
        # End container
        if not (len(binary.containers) == 2 and binary.containers[-1].type == 0x000100FD):
            end_ctr = GFS0ContainerBinary()
            end_ctr.version = 0x01105100
            end_ctr.type = 0x00000000
            
            end_ctr.size = 0
            binary.containers.append(end_ctr)
            
        return binary
    
    def add_node(self, parent_idx, name, position, rotation, scale, unknown_float, properties):
        node = NodeInterface()
        node.parent_idx = parent_idx
        node.name = name
        node.position = position
        node.rotation = rotation
        node.scale = scale
        node.unknown_float = unknown_float
        node.properties = properties
        self.bones.append(node)
        
    def add_mesh(self, node_id, vertices, material_name, indices, morphs, unknown_0x12, unknown_float_1, unknown_float_2, keep_bounding_box, keep_bounding_sphere):
        mesh = MeshInterface()
        mesh.node            = node_id
        mesh.vertices        = vertices
        mesh.material_name   = material_name
        mesh.indices         = indices
        #mesh.morphs = morphs
        mesh.unknown_0x12    = unknown_0x12
        mesh.unknown_float_1 = unknown_float_1
        mesh.unknown_float_2 = unknown_float_2
        
        mesh.index_type = 2 if max(indices) >= 2**16 else 1
        mesh.keep_bounding_box    = keep_bounding_box
        mesh.keep_bounding_sphere = keep_bounding_sphere
        
        self.meshes.append(mesh)



class NodeInterface:
    def __init__(self):
        self.parent_idx = None
        self.name = None
        self.position = None
        self.rotation = None
        self.scale = None
        self.unknown_float = None
        self.properties = [] # Property interfaces?
    
    @classmethod
    def binary_node_tree_to_list(cls, binary):
        node_list = []
        mesh_list = []
        camera_list = []
        light_list = []
        cls._fetch_node_from_tree(binary, -1, node_list, mesh_list, camera_list, light_list)
        return node_list, mesh_list, camera_list, light_list
        
    @classmethod
    def _fetch_node_from_tree(cls, node, parent, node_list, mesh_list, camera_list, light_list):
        node_idx = len(node_list)
        node_list.append(cls.from_binary(node, parent))
        for attachment in node.attachments:
            if attachment.type == 4:
                mesh_list.append(MeshInterface.from_binary(node_idx, attachment.data))
            elif attachment.type == 5:
                camera_list.append(CameraInterface.from_binary(node_idx, attachment.data))
            elif attachment.type == 6:
                light_list.append(LightInterface.from_binary(node_idx, attachment.data))
            else:
                raise NotImplementedError("No Interface exists for attachment type '{attachment.type}'")
        for child in node.children[::-1]:
            cls._fetch_node_from_tree(child, node_idx, node_list, mesh_list, camera_list, light_list)
    
    @classmethod
    def list_to_binary_node_tree(cls, node_list, mesh_list, camera_list, light_list):
        node_children = {}
        # First not in list required to be root
        # Should probably throw in a check here to make sure...
        for i, node in enumerate(node_list[1:]):
            n_id = node.parent
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
                node = node_collection[elem.node]
                attachment = NodeAttachmentBinary()
                attachment.type = typevalue
                attachment.data = elem.to_binary()
                node.attachments.append(attachment)
                node.attachment_count += 1
                binaries.append((attachment.data, elem.node))
            return binaries
                
        mesh_binaries = add_attachments("Mesh",   4, mesh_list)
        add_attachments("Camera", 5, camera_list)
        add_attachments("Light",  6, light_list)
        
        return node_collection[0], id_map, mesh_binaries
    
    @classmethod
    def _push_node_into_tree(cls, node_idx, node_children, node_collection, id_map):
        child_node_idxs = node_children.get(node_idx, [])
        for cn_id in child_node_idxs:
            id_map[cn_id] = len(id_map)
            node_collection[node_idx].children.insert(0, node_collection[cn_id])
            cls._push_node_into_tree(cn_id, node_children, node_collection, id_map)

    @classmethod
    def from_binary(cls, binary, parent_idx):
        instance = cls()
        
        instance.parent = parent_idx
        instance.name = binary.name.string
        instance.position = binary.position
        instance.rotation = binary.rotation
        instance.scale = binary.scale
        instance.unknown_float = binary.float
        instance.properties = binary.properties.data # Interface?!?
        
        return instance
    
    def to_binary(self):
        binary = SceneNodeBinary()
        
        binary.name = ObjectName.from_name(self.name)
        binary.position = self.position
        binary.rotation = self.rotation
        binary.scale = self.scale
        binary.float = self.unknown_float
        binary.has_properties = len(self.properties) > 0
        binary.properties.data = self.properties  # Interface?!?
        binary.properties.count = len(self.properties)
        
        return binary
    
class MeshInterface:
    def __init__(self):
        self.node   = None
        
        self.flag_0x00000001 = None
        self.flag_0x00000020 = None
        self.flag_0x00000080 = None
        self.flag_0x00000100 = None
        self.flag_0x00000200 = None
        self.flag_0x00000400 = None
        self.flag_0x00000800 = None
        self.flag_0x00002000 = None
        self.flag_0x00004000 = None
        self.flag_0x00008000 = None
        self.flag_0x00010000 = None
        self.flag_0x00020000 = None
        self.flag_0x00040000 = None
        self.flag_0x00080000 = None
        self.flag_0x00100000 = None
        self.flag_0x00200000 = None
        self.flag_0x00400000 = None
        self.flag_0x00800000 = None
        self.flag_0x01000000 = None
        self.flag_0x02000000 = None
        self.flag_0x04000000 = None
        self.flag_0x08000000 = None
        self.flag_0x10000000 = None
        self.flag_0x20000000 = None
        self.flag_0x40000000 = None
        self.flag_0x80000000 = None
    
        self.vertices = None
        self.material_name = None
        self.indices = None
        self.morphs = None
        self.unknown_0x12 = None
        self.unknown_float_1 = None
        self.unknown_float_2 = None
        
        # THINGS THAT COULD BE REMOVABLE
        self.index_type = None
        self.keep_bounding_box = None
        self.keep_bounding_sphere = None
        
    
    @classmethod
    def from_binary(cls, node_idx, binary):
        instance = cls()
        
        # Deal with unpacking later...
        instance.node = node_idx
        
        # Can get rid of some of these in a minute
        instance.flag_0x00000001 = (binary.flags & 0x00000001) != 0
        # 0x00000004 says if indices are present
        instance.keep_bounding_box = (binary.flags & 0x00000008) != 0
        instance.keep_bounding_sphere = (binary.flags & 0x00000010) != 0
        instance.flag_0x00000020 = (binary.flags & 0x00000020) != 0
        # 0x00000040 says if any morphs are present
        instance.flag_0x00000080 = (binary.flags & 0x00000080) != 0
        instance.flag_0x00000100 = (binary.flags & 0x00000100) != 0
        instance.flag_0x00000200 = (binary.flags & 0x00000200) != 0
        instance.flag_0x00000400 = (binary.flags & 0x00000400) != 0
        instance.flag_0x00000800 = (binary.flags & 0x00000800) != 0
        # 0x00001000 says if unknown floats are present
        instance.flag_0x00002000 = (binary.flags & 0x00002000) != 0
        instance.flag_0x00004000 = (binary.flags & 0x00004000) != 0
        instance.flag_0x00008000 = (binary.flags & 0x00008000) != 0
        instance.flag_0x00010000 = (binary.flags & 0x00010000) != 0
        instance.flag_0x00020000 = (binary.flags & 0x00020000) != 0
        instance.flag_0x00040000 = (binary.flags & 0x00040000) != 0
        instance.flag_0x00080000 = (binary.flags & 0x00080000) != 0
        instance.flag_0x00100000 = (binary.flags & 0x00100000) != 0
        instance.flag_0x00200000 = (binary.flags & 0x00200000) != 0
        instance.flag_0x00400000 = (binary.flags & 0x00400000) != 0
        instance.flag_0x00800000 = (binary.flags & 0x00800000) != 0
        instance.flag_0x01000000 = (binary.flags & 0x01000000) != 0
        instance.flag_0x02000000 = (binary.flags & 0x02000000) != 0
        instance.flag_0x04000000 = (binary.flags & 0x04000000) != 0
        instance.flag_0x08000000 = (binary.flags & 0x08000000) != 0
        instance.flag_0x10000000 = (binary.flags & 0x10000000) != 0
        instance.flag_0x20000000 = (binary.flags & 0x20000000) != 0
        instance.flag_0x40000000 = (binary.flags & 0x40000000) != 0
        instance.flag_0x80000000 = (binary.flags & 0x80000000) != 0
        
        instance.vertices        = binary.vertices
        instance.material_name   = binary.material_name.string
        instance.indices         = binary.indices
        instance.index_type      = binary.index_type # Can probably remove this...
        instance.morphs          = binary.morph_data # NEEDS UNPACKING
        instance.unknown_0x12    = binary.unknown_0x12
        instance.unknown_float_1 = binary.unknown_float_1
        instance.unknown_float_2 = binary.unknown_float_2
        
        return instance
        
    def to_binary(self):
        binary = MeshBinary()
        binary.vertex_format = 0
        
        if len(self.vertices):
            # Assume that if something is true for the first vertex
            # Empty - 0x00000001 # << 0
            binary.vertex_format |= (self.vertices[0].position  is not None) <<  1 # 0x00000002
            # Empty - 0x00000004 # << 2
            # Empty - 0x00000008 # << 3
            binary.vertex_format |= (self.vertices[0].normal    is not None) <<  4 # 0x00000010
            # Empty - 0x00000020 # << 5
            binary.vertex_format |= (self.vertices[0].color1    is not None) <<  6 # 0x00000040
            # Empty - 0x00000080 # << 7
            binary.vertex_format |= (self.vertices[0].texcoord0 is not None) <<  8 # 0x00000100
            binary.vertex_format |= (self.vertices[0].texcoord1 is not None) <<  9 # 0x00000200
            binary.vertex_format |= (self.vertices[0].texcoord2 is not None) << 10 # 0x00000400
            binary.vertex_format |= (self.vertices[0].texcoord3 is not None) << 11 # 0x00000800
            binary.vertex_format |= (self.vertices[0].texcoord4 is not None) << 12 # 0x00001000
            binary.vertex_format |= (self.vertices[0].texcoord5 is not None) << 13 # 0x00002000
            binary.vertex_format |= (self.vertices[0].texcoord6 is not None) << 14 # 0x00004000
            binary.vertex_format |= (self.vertices[0].texcoord7 is not None) << 15 # 0x00008000
            # Empty - 0x00010000 # << 16
            # Empty - 0x00020000 # << 17
            # Empty - 0x00040000 # << 18
            # Empty - 0x00080000 # << 19
            # Empty - 0x00100000 # << 20
            # Empty - 0x00200000 # << 21
            # Empty - 0x00400000 # << 22
            # Empty - 0x00800000 # << 23
            # Empty - 0x01000000 # << 24
            # Empty - 0x02000000 # << 25
            # Empty - 0x04000000 # << 26
            # Empty - 0x08000000 # << 27
            binary.vertex_format |= (self.vertices[0].tangent  is not None) << 28 # 0x10000000
            binary.vertex_format |= (self.vertices[0].binormal is not None) << 29 # 0x20000000
            binary.vertex_format |= (self.vertices[0].color2   is not None) << 30 # 0x40000000
            # Empty - 0x80000000 # << 31
            
            binary.flags |= (self.vertices[0].indices is not None) << 0
        
        binary.flags |= self.flag_0x00000001 <<  0
        binary.flags |= (self.material_name is not None) << 1
        binary.flags |= (len(self.indices) > 0) << 2
        binary.flags |= self.keep_bounding_box << 3
        binary.flags |= self.keep_bounding_sphere << 4
        binary.flags |= self.flag_0x00000020 <<  5
        binary.flags |= (self.morphs.count is not None) << 6
        binary.flags |= self.flag_0x00000080 <<  7
        binary.flags |= self.flag_0x00000100 <<  8
        binary.flags |= self.flag_0x00000200 <<  9
        binary.flags |= self.flag_0x00000400 << 10
        binary.flags |= self.flag_0x00000800 << 11
        if self.unknown_float_1 is None and self.unknown_float_2 is None:
            pass
        else:
            binary.flags |= 0x00001000
            binary.unknown_float_1 = self.unknown_float_1
            binary.unknown_float_2 = self.unknown_float_2
            if self.unknown_float_1 is None:
                binary.unknown_float_1 = 0.
            if self.unknown_float_2 is None:
                binary.unknown_float_2 = 0.
        binary.flags |= self.flag_0x00002000 << 13
        binary.flags |= self.flag_0x00004000 << 14
        binary.flags |= self.flag_0x00008000 << 15
        binary.flags |= self.flag_0x00010000 << 16
        binary.flags |= self.flag_0x00020000 << 17
        binary.flags |= self.flag_0x00040000 << 18
        binary.flags |= self.flag_0x00080000 << 19
        binary.flags |= self.flag_0x00100000 << 20
        binary.flags |= self.flag_0x00200000 << 21
        binary.flags |= self.flag_0x00400000 << 22
        binary.flags |= self.flag_0x00800000 << 23
        binary.flags |= self.flag_0x01000000 << 24
        binary.flags |= self.flag_0x02000000 << 25
        binary.flags |= self.flag_0x04000000 << 26
        binary.flags |= self.flag_0x08000000 << 27
        binary.flags |= self.flag_0x10000000 << 28
        binary.flags |= self.flag_0x20000000 << 29
        binary.flags |= self.flag_0x40000000 << 30
        binary.flags |= self.flag_0x80000000 << 31
        
        if len(self.indices) % 3:
            raise ValueError("Mesh contains {len(self.indices)} indices; must be a multiple of 3")
        binary.tri_count     = len(self.indices) // 3
        binary.index_type    = self.index_type
        binary.vertex_count  = len(self.vertices)
        binary.unknown_0x12  = self.unknown_0x12
        binary.vertices      = self.vertices
        binary.morph_data.flags = self.morphs.flags        # NEEDS UNPACKING
        binary.morph_data.count = len(self.morphs.targets) # NEEDS UNPACKING
        binary.morph_data.targets = self.morphs.targets    # NEEDS UNPACKING
        binary.indices       = self.indices
        binary.material_name = ObjectName.from_name(self.material_name)
        
        ####################
        # BOUNDING VOLUMES #
        ####################
        if self.keep_bounding_sphere:
            if binary.vertex_format & 0x00000002:
                # This is WRONG but I can't get an iterative Welzl algorithm
                # working
                max_dims = [*self.vertices[0].position]
                min_dims = [*self.vertices[0].position]
                        
                for v in self.vertices:
                    pos = v.position
                    for i in range(3):
                        max_dims[i] = max(max_dims[i], pos[i])
                        min_dims[i] = min(min_dims[i], pos[i])
                
                if self.keep_bounding_box:
                    binary.bounding_box_max_dims = max_dims
                    binary.bounding_box_min_dims = min_dims
                centre = [.5*(mx + mn) for mx, mn in zip(max_dims, min_dims)]
                radius = 0.
                for v in self.vertices:
                    pos = v.position
                    dist = (p-c for p, c in zip(pos, centre))
                    radius = max(sum(d*d for d in dist), radius)
                binary.bounding_sphere_centre = centre
                binary.bounding_sphere_radius = radius
            else:
                raise ValueError("Mesh is marked for bounding sphere export, but has no vertex position data")
                
        return binary
    
class CameraInterface:
    def __init__(self):
        self.node   = None
        self.binary = None
        
    @classmethod
    def from_binary(cls, node_idx, binary):
        instance = cls()
        # Deal with unpacking later...
        instance.node = node_idx
        instance.binary = binary
        
        return instance
        
    def to_binary(self):
        return self.binary
    
class LightInterface:
    def __init__(self):
        self.node   = None
        self.binary = None
        
    @classmethod
    def from_binary(cls, node_idx, binary):
        instance = cls()
        
        # Deal with unpacking later...
        instance.node = node_idx
        instance.binary = binary
        
        return instance
        
    def to_binary(self):
        return self.binary

class PropertyInterface:
    def __init__(self):
        self.name = None
        self.type = None
        self.contents = None
        
    @classmethod
    def from_binary(cls, binary):
        instance = cls()
        instance.name = binary.name.string
        instance.type = binary.type
        instance.contents = binary.contents
        return instance
    
    def to_binary(self):
        binary = PropertyBinary()
        binary.name = ObjectName.from_name(self.name)
        binary.type = self.type
        binary.data = self.contents
        
        # Move these checks into the binary..?
        if binary.type == 1:
            if type(binary.data) != int:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected int")
            binary.size = 4
            
        elif binary.type == 2:
            if type(binary.data) != int and type(binary.data) != float:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected int or float")
            binary.size = 4
            
        elif binary.type == 3:
            if type(binary.data) != int:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected int")
            binary.size = 1
            
        elif binary.type == 4:
            if type(binary.data) != str:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected str")
            binary.size = len(binary.data.encode(PropertyBinary.ENCODING)) - 1
            
        elif binary.type == 5:
            if not hasattr(binary.data, "__len__"):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected an iterable object")
            if not len(binary.data) == 3:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents has length {len(self.contents)}: expected 3")
            if not all([type(t) is int for t in self.contents]):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents have types {[type(t) for t in self.contents]}: expected all ints")
                
            binary.size = 3
        
        elif binary.type == 6:
            if not hasattr(binary.data, "__len__"):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected an iterable object")
            if not len(binary.data) == 4:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents has length {len(self.contents)}: expected 4")
            if not all([type(t) is int for t in self.contents]):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents have types {[type(t) for t in self.contents]}: expected all ints")
                
            binary.size = 4
        
        elif binary.type == 7:
            if not hasattr(binary.data, "__len__"):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected an iterable object")
            if not len(binary.data) == 3:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents has length {len(self.contents)}: expected 3")
            if not all([type(t) is int for t in self.contents]):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents have types {[type(t) for t in self.contents]}: expected all ints or floats")
                
            binary.size = 9
        
        elif binary.type == 8:
            if not hasattr(binary.data, "__len__"):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected an iterable object")
            if not len(binary.data) == 4:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents has length {len(self.contents)}: expected 4")
            if not all([type(t) is int for t in self.contents]):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents have types {[type(t) for t in self.contents]}: expected all ints or floats")
                
            binary.size = 12
                    
        elif binary.type == 9:
            if type(binary.data) != bytes:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected bytes")
            binary.size = len(binary.data)
            
        else:
            raise NotImplementedError(f"Unknown property type '{self.type}'")
            
class ModelInterface:
    @classmethod
    def from_binary(cls, binary, copy_verts=True):
        #instance.skinning_data = binary.skinning_data
        keep_bounding_box = binary.flags & 0x00000001 != 0
        keep_bounding_sphere = binary.flags & 0x00000002 != 0
        
        bones,   \
        meshes,  \
        cameras, \
        lights = NodeInterface.binary_node_tree_to_list(binary.root_node)
        
        if binary.skinning_data.matrix_palette is not None:
            for mesh in meshes:
                if copy_verts:
                    mesh.vertices = copy.deepcopy(mesh.vertices)
                if mesh.vertices[0].indices is not None:
                    for v in mesh.vertices:
                        #v.indices = v.indices[::-1]
                        v.indices = [binary.skinning_data.matrix_palette[idx] for idx in v.indices[::-1]]
        return bones, meshes, cameras, lights, keep_bounding_box, keep_bounding_sphere
        
    @staticmethod
    def to_binary(bones, meshes, cameras, lights, keep_bounding_box, keep_bounding_sphere, copy_verts=True):
        binary = ModelBinary()

        binary.flags = 0
        if keep_bounding_box:
            binary.flags |= 0x00000001
        if keep_bounding_sphere:
            binary.flags |= 0x00000002
        
        # Need to return mesh binary list here too!
        binary.root_node, old_node_id_to_new_node_id_map, mesh_binaries = NodeInterface.list_to_binary_node_tree(bones, meshes, cameras, lights)

        ####################
        # BOUNDING VOLUMES #
        ####################
        if keep_bounding_box or keep_bounding_sphere:
            verts = []
            for mesh_binary, mesh_node_id in mesh_binaries:
                if mesh_binary.flags & 0x00000008 != 0:  # Check if you need to do the others here too
                    mx = mesh_binary.bounding_box_max_dims
                    mn = mesh_binary.bounding_box_min_dims
                    verts.extend([
                        [mx[0], mx[1], mx[2]],
                        [mx[0], mx[1], mn[2]],
                        [mx[0], mn[1], mx[2]],
                        [mx[0], mn[1], mn[2]],
                        [mn[0], mn[1], mn[2]],
                        [mn[0], mn[1], mx[2]],
                        [mn[0], mx[1], mn[2]],
                        [mn[0], mx[1], mx[2]]
                    ])
                
            if not len(verts):
                if keep_bounding_box:
                    raise ValueError("Model is marked for bounding box export, but has no meshes with vertex position data")
                elif keep_bounding_sphere:
                    raise ValueError("Model is marked for bounding sphere export, but has no meshes with vertex position data")
            
            
            max_dims = [*verts[0]]
            min_dims = [*verts[0]]
                    
            for pos in verts:
                for i in range(3):
                    max_dims[i] = max(max_dims[i], pos[i])
                    min_dims[i] = min(min_dims[i], pos[i])
            
            # Do box
            if keep_bounding_box:
                binary.bounding_box_max_dims = max_dims
                binary.bounding_box_min_dims = min_dims
                
            # Do sphere
            # This is WRONG but I can't get an iterative Welzl algorithm working
            if keep_bounding_sphere:
                centre = [.5*(mx + mn) for mx, mn in zip(max_dims, min_dims)]
                radius = 0.
                for mesh_binary, mesh_node_id in mesh_binaries:
                    if mesh_binary.vertex_format & 0x00000002 == 0:
                        continue
                    for v in mesh_binary.vertices:
                        pos = v.position
                        dist = (p-c for p, c in zip(pos, centre))
                        radius = max(sum(d*d for d in dist), radius)
                binary.bounding_sphere_centre = centre
                binary.bounding_sphere_radius = radius
            
        #########################
        # CREATE MATRIX PALETTE #
        #########################
        found_indices = False
        for mesh_binary, mesh_node_id in mesh_binaries:
            if mesh_binary.flags & 0x00000001:
                found_indices = True
                break
            
        if found_indices:
            binary.flags |= 0x00000004
            
            # GENERATE SKINNING DATA STRUCTURE
            world_matrices = [None]*len(bones)
            for i, bone in enumerate(bones):
                local_matrix = transforms_to_matrix(bone.position, bone.rotation, bone.scale)
                if bone.parent > -1:
                    world_matrices[i] = multiply_transform_matrices(world_matrices[bone.parent], local_matrix)
                else:
                    world_matrices[i] = local_matrix
            
            ibpms = []
            matrix_palette = []
            matrix_cache = {}
            index_lookup = {}
            for mesh_binary, mesh_node_id in mesh_binaries:
                node_matrix = world_matrices[mesh_node_id]
                if mesh_binary.flags & 0x00000001:
                    indices = set()
                    for vertex in mesh_binary.vertices:
                        for idx, wgt in zip(vertex.indices[::-1], vertex.weights):
                            if wgt > 0:
                                indices.add(idx)
                                
                    for idx in sorted(indices):
                        inv_index_matrix = invert_transform_matrix(world_matrices[idx])
                        ibpm = multiply_transform_matrices(inv_index_matrix, node_matrix)
                        if idx not in matrix_cache:
                            matrix_cache[idx] = {}
                            
                        matching_matrix_found = False
                        for palette_idx, palette_ibpm in matrix_cache[idx].items():
                            if are_matrices_close(ibpm, palette_ibpm, atol=0.01, rtol=0.05):
                                index_lookup[(mesh_node_id, idx)] = palette_idx
                                matching_matrix_found = True
                                break
                            
                        if not matching_matrix_found:
                            palette_idx = len(matrix_palette)
                            matrix_cache[idx][palette_idx] = ibpm
                            matrix_palette.append(idx)
                            ibpms.append(ibpm)
                            index_lookup[(mesh_node_id, idx)] = palette_idx
            
            binary.skinning_data.matrix_palette = matrix_palette
            binary.skinning_data.ibpms = ibpms
            binary.skinning_data.bone_count = len(matrix_palette)
            
            # REMAP VERTEX INDICES
            for mesh, mesh_node_id in mesh_binaries:
                if copy_verts:
                    mesh.vertices = copy.deepcopy(mesh.vertices)
                if mesh.vertices[0].indices is not None:
                    for v in mesh.vertices:
                        # Need to factor in remapped nodes
                        #v.indices = [idx for idx in v.indices[::-1]]
                        indices = [index_lookup.get((mesh_node_id, idx), 0) for idx in v.indices]
                        for wgt_idx, wgt in enumerate(v.weights):
                            if wgt == 0:
                                indices[wgt_idx] = 0
                        v.indices = indices[::-1]
        return binary
        