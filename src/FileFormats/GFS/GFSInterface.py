import copy

from ...serialization.BinaryTargets import OffsetTracker
from .GFSBinary import GFS0Binary
from .GFSBinary.CommonStructures import ObjectName, PropertyBinary
from .GFSBinary.GFS0ContainerBinary import GFS0ContainerBinary, SizedObjArray
from .GFSBinary.TextureBinary import TextureBinary
from .GFSBinary.MaterialBinary import MaterialBinary
from .GFSBinary.ModelBinary import ModelBinary
from .GFSBinary.ModelBinary.SceneNodeBinary import SceneNodeBinary
from .GFSBinary.ModelBinary.SceneNodeBinary.MeshBinary import MeshBinary
from .GFSBinary.ModelBinary.SceneNodeBinary.NodeAttachmentBinary import NodeAttachmentBinary


class GFSInterface:
    def __init__(self):
        self.meshes = []
        self.cameras = []
        self.lights = []
        self.bones = []
        self.materials = []
        self.textures = []
        self.animations = []
        
        # Things that need to be removed eventually
        self.model = None
        self.animation_data = None
        self.data_0x000100F8 = None
        self.data_0x000100F9 = None


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
                instance.bones,   \
                instance.meshes,  \
                instance.cameras, \
                instance.lights,  \
                instance.model = ModelInterface.from_binary(ctr.data, duplicate_data)
            elif ctr.type == 0x000100FD:
                instance.animation_data = ctr.data
            elif ctr.type == 0x000100F8:
                instance.data_0x000100F8 = ctr.data
            elif ctr.type == 0x000100F9:
                instance.data_0x000100F9 = ctr.data
        
        return instance
    
    def to_binary(self):
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
            
            model_binary = self.model.to_binary(self.bones, self.meshes, self.cameras, self.lights)
            mdl_ctr.data = model_binary
            ot.rw_obj(mdl_ctr)
            mdl_ctr.size = ot.tell() - offset
            binary.containers.append(mdl_ctr)
                    
        # Model container
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
        if self.data_0x000100F9 is not None:
            offset = ot.tell()
            unk_ctr = GFS0ContainerBinary()
            unk_ctr.version = 0x01105100
            unk_ctr.type = 0x000100F9
            
            unk_ctr.data = self.data_0x000100F9
            unk_ctr.size = len(self.data_0x000100F9.data) + 0x10
            # ot.rw_obj(unk_ctr)
            # unk_ctr.size = ot.tell() - offset
            binary.containers.append(unk_ctr)
            
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

class TextureInterface:
    def __init__(self):
        self.name = None
        self.image_data = None
        
    @classmethod
    def from_binary(cls, binary):
        instance = cls()
        
        instance.name = binary.name
        instance.image_data = binary.data
        
        return instance
    
    def to_binary(self):
        binary = TextureBinary()
        
        binary.name = self.name
        binary.pixel_format = 1 # Shouldn't this depend on the DXT compression..?!
        binary.data_size = len(self.image_data)
        binary.data = self.image_data
        
        return binary

class MaterialInterface:
    def __init__(self):
        
        # Flags
        self.flag_0            = None
        self.flag_1            = None
        self.flag_2            = None
        self.flag_3            = None
        self.use_vertex_colors = None
        self.flag_5            = None
        self.flag_6            = None
        self.use_light_1       = None
        self.flag_8            = None
        self.flag_9            = None
        self.flag_10           = None
        self.use_light_2       = None
        self.purple_wireframe  = None
        self.flag_13           = None
        self.receive_shadow    = None
        self.cast_shadow       = None
        self.flag_17           = None
        self.flag_18           = None
        self.disable_bloom     = None
        self.flag_29           = None
        self.flag_30           = None
        self.flag_31           = None
        
        # Presumably some of these can be removed...
        self.ambient = None
        self.diffuse = None
        self.specular = None
        self.emissive = None
        self.unknown_0x48 = None
        self.unknown_0x4C = None
        self.draw_method  = None
        self.unknown_0x51 = None
        self.unknown_0x52 = None
        self.unknown_0x53 = None
        self.unknown_0x54 = None
        self.unknown_0x55 = None
        self.unknown_0x56 = None
        self.unknown_0x58 = None
        self.unknown_0x5A = None
        self.unknown_0x5C = None
        self.unknown_0x5E = None
        self.unknown_0x60 = None
        self.unknown_0x64 = None
        self.disable_backface_culling = None
        self.unknown_0x6A = None
        
        # Need to come up with a better way of assigning the extra data to these
        self.diffuse_texture    = None
        self.normal_texture     = None
        self.specular_texture   = None
        self.reflection_texture = None
        self.highlight_texture  = None
        self.glow_texture       = None
        self.night_texture      = None
        self.detail_texture     = None
        self.shadow_texture     = None
        
        self.attributes = []
    
    @classmethod
    def from_binary(cls, binary):
        instance = cls()
        
        instance.name = binary.name.string
        instance.flags = binary.flags
        # Can at least remove the flags for now
        instance.ambient = binary.ambient
        instance.diffuse = binary.diffuse
        instance.specular = binary.specular
        instance.emissive = binary.emissive
        instance.unknown_0x48 = binary.unknown_0x48
        instance.unknown_0x4C = binary.unknown_0x4C
        instance.draw_method  = binary.draw_method
        instance.unknown_0x51 = binary.unknown_0x51
        instance.unknown_0x52 = binary.unknown_0x52
        instance.unknown_0x53 = binary.unknown_0x53
        instance.unknown_0x54 = binary.unknown_0x54
        instance.unknown_0x55 = binary.unknown_0x55
        instance.unknown_0x56 = binary.unknown_0x56
        instance.unknown_0x58 = binary.unknown_0x58
        instance.unknown_0x5A = binary.unknown_0x5A
        instance.unknown_0x5C = binary.unknown_0x5C
        instance.unknown_0x5E = binary.unknown_0x5E
        instance.unknown_0x60 = binary.unknown_0x60
        instance.unknown_0x64 = binary.unknown_0x64
        instance.disable_backface_culling = binary.disable_backface_culling
        instance.unknown_0x6A = binary.unknown_0x6A
        
        # Need to come up with a better way of assigning the extra data to these
        # Since it's unclear what this extra data does... leave it for now
        instance.diffuse_texture    = binary.diffuse_texture
        instance.normal_texture     = binary.normal_texture
        instance.specular_texture   = binary.specular_texture
        instance.reflection_texture = binary.reflection_texture
        instance.highlight_texture  = binary.highlight_texture
        instance.glow_texture       = binary.glow_texture
        instance.night_texture      = binary.night_texture
        instance.detail_texture     = binary.detail_texture
        instance.shadow_texture     = binary.shadow_texture
        
        # Attributes
        instance.attributes = binary.attributes.data
        
        # Deal with other flags
        instance.flag_0            = (binary.flags & 0x00000001) != 0
        instance.flag_1            = (binary.flags & 0x00000002) != 0
        instance.flag_2            = (binary.flags & 0x00000004) != 0
        instance.flag_3            = (binary.flags & 0x00000008) != 0
        instance.use_vertex_colors = (binary.flags & 0x00000010) != 0
        instance.flag_5            = (binary.flags & 0x00000020) != 0
        instance.flag_6            = (binary.flags & 0x00000040) != 0
        instance.use_light_1       = (binary.flags & 0x00000080) != 0
        instance.flag_8            = (binary.flags & 0x00000100) != 0
        instance.flag_9            = (binary.flags & 0x00000200) != 0
        instance.flag_10           = (binary.flags & 0x00000400) != 0
        instance.use_light_2       = (binary.flags & 0x00000800) != 0
        instance.purple_wireframe  = (binary.flags & 0x00001000) != 0
        instance.flag_13           = (binary.flags & 0x00002000) != 0
        instance.receive_shadow    = (binary.flags & 0x00004000) != 0
        instance.cast_shadow       = (binary.flags & 0x00008000) != 0
        instance.flag_17           = (binary.flags & 0x00020000) != 0
        instance.flag_18           = (binary.flags & 0x00040000) != 0
        instance.disable_bloom     = (binary.flags & 0x00080000) != 0
        instance.flag_29           = (binary.flags & 0x20000000) != 0
        instance.flag_30           = (binary.flags & 0x40000000) != 0
        instance.flag_31           = (binary.flags & 0x80000000) != 0
        
        return instance
    
    def to_binary(self):
        binary = MaterialBinary()
        
        binary.flags = 0
        if self.flag_0:                         binary.flags |= 0x00000001
        if self.flag_1:                         binary.flags |= 0x00000002
        if self.flag_2:                         binary.flags |= 0x00000004
        if self.flag_3:                         binary.flags |= 0x00000008
        if self.use_vertex_colors:              binary.flags |= 0x00000010
        if self.flag_5:                         binary.flags |= 0x00000020
        if self.flag_6:                         binary.flags |= 0x00000040
        if self.use_light_1:                    binary.flags |= 0x00000080
        if self.flag_8:                         binary.flags |= 0x00000100
        if self.flag_9:                         binary.flags |= 0x00000200
        if self.flag_10:                        binary.flags |= 0x00000400
        if self.use_light_2:                    binary.flags |= 0x00000800
        if self.purple_wireframe:               binary.flags |= 0x00001000
        if self.flag_13:                        binary.flags |= 0x00002000
        if self.receive_shadow:                 binary.flags |= 0x00004000
        if self.cast_shadow:                    binary.flags |= 0x00008000
        if len(self.attributes):                binary.flags |= 0x00010000
        if self.flag_17:                        binary.flags |= 0x00020000
        if self.flag_18:                        binary.flags |= 0x00040000
        if self.disable_bloom:                  binary.flags |= 0x00080000
        if self.diffuse_texture    is not None: binary.flags |= 0x00100000
        if self.normal_texture     is not None: binary.flags |= 0x00200000
        if self.specular_texture   is not None: binary.flags |= 0x00400000
        if self.reflection_texture is not None: binary.flags |= 0x00800000
        if self.highlight_texture  is not None: binary.flags |= 0x01000000
        if self.glow_texture       is not None: binary.flags |= 0x02000000
        if self.night_texture      is not None: binary.flags |= 0x04000000
        if self.detail_texture     is not None: binary.flags |= 0x08000000
        if self.shadow_texture     is not None: binary.flags |= 0x10000000
        if self.flag_29:                        binary.flags |= 0x20000000
        if self.flag_30:                        binary.flags |= 0x40000000
        if self.flag_31:                        binary.flags |= 0x80000000
        
        binary.name                     = ObjectName.from_name(self.name)
        binary.ambient                  = self.ambient
        binary.diffuse                  = self.diffuse
        binary.specular                 = self.specular
        binary.emissive                 = self.emissive
        binary.unknown_0x48             = self.unknown_0x48
        binary.unknown_0x4C             = self.unknown_0x4C
        binary.draw_method              = self.draw_method # 0 - opaque, 1 - translucent
        binary.unknown_0x51             = self.unknown_0x51
        binary.unknown_0x52             = self.unknown_0x52
        binary.unknown_0x53             = self.unknown_0x53
        binary.unknown_0x54             = self.unknown_0x54
        binary.unknown_0x55             = self.unknown_0x55
        binary.unknown_0x56             = self.unknown_0x56
        binary.unknown_0x58             = self.unknown_0x58
        binary.unknown_0x5A             = self.unknown_0x5A
        binary.unknown_0x5C             = self.unknown_0x5C
        binary.unknown_0x5E             = self.unknown_0x5E
        binary.unknown_0x60             = self.unknown_0x60
        binary.unknown_0x64             = self.unknown_0x64
        binary.disable_backface_culling = self.disable_backface_culling
        binary.unknown_0x6A             = self.unknown_0x6A
        
        binary.diffuse_texture    = self.diffuse_texture
        binary.normal_texture     = self.normal_texture
        binary.specular_texture   = self.specular_texture
        binary.reflection_texture = self.reflection_texture
        binary.highlight_texture  = self.highlight_texture
        binary.glow_texture       = self.glow_texture
        binary.night_texture      = self.night_texture
        binary.detail_texture     = self.detail_texture
        binary.shadow_texture     = self.shadow_texture
        
        binary.attributes.data = self.attributes
        binary.attributes.count = len(self.attributes)
        
        return binary


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
                binaries.append(attachment.data)
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
        
        self.flag_0x00000008 = None
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
        self.vertex_format = None
    
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
        
        # THINGS THAT SHOULD BE REMOVABLE
        self.bounding_box_max_dims = None
        self.bounding_box_min_dims = None
        self.bounding_sphere_centre = None
        self.bounding_sphere_radius = None
        
    
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
        # 0x00000010 says if unknown floats are present
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
        
        # THINGS TO REMOVE
        instance.bounding_box_max_dims  = list(binary.bounding_box_max_dims)
        instance.bounding_box_min_dims  = list(binary.bounding_box_min_dims)
        instance.bounding_sphere_centre = binary.bounding_sphere_centre
        instance.bounding_sphere_radius = binary.bounding_sphere_radius
        
        return instance
        
    def to_binary(self):
        binary = MeshBinary()
        binary.flags = 0
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
        
        binary.flags |= (self.material_name is not None) << 1
        binary.flags |= (len(self.indices) > 0) << 2
        binary.flags |= self.keep_bounding_box << 3
        binary.flags |= self.keep_bounding_sphere << 4
        binary.flags |= self.flag_0x00000020 <<  5
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
        
        # if binary.vertex_format & 0x00000002: # If there is position data,
        #     max_dims = [*self.vertices[0].position]
        #     min_dims = [*self.vertices[0].position]
            
        #     for v in self.vertices:
        #         pos = v.position
        #         for i in range(3):
        #             max_dims[i] = max(max_dims[i], pos[i])
        #             min_dims[i] = min(min_dims[i], pos[i])
            
        #     binary.bounding_box_max_dims = max_dims
        #     binary.bounding_box_min_dims = min_dims
            
        # Bounding boxes don't always agree with vertices...
        # print(self.bounding_box_max_dims, max_dims)
        # print(self.bounding_box_min_dims, min_dims)
        # assert self.bounding_box_max_dims == max_dims
        # assert self.bounding_box_min_dims == min_dims
        # Bounding spheres are more complicated
        
        binary.bounding_box_max_dims = self.bounding_box_max_dims
        binary.bounding_box_min_dims = self.bounding_box_min_dims
        binary.bounding_sphere_centre = self.bounding_sphere_centre
        binary.bounding_sphere_radius = self.bounding_sphere_radius
        
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
    def __init__(self):
        self.skinning_data = None
        self.bounding_box_max_dims = None
        self.bounding_box_min_dims = None
        self.bounding_sphere_centre = None
        self.bounding_sphere_radius = None
        
        self.keep_bounding_box = False
        self.keep_bounding_sphere = False
        
    @classmethod
    def from_binary(cls, binary, copy_verts=True):
        instance = cls()
        
        instance.skinning_data = binary.skinning_data
        instance.bounding_box_max_dims = binary.bounding_box_max_dims
        instance.bounding_box_min_dims = binary.bounding_box_min_dims
        instance.bounding_sphere_centre = binary.bounding_sphere_centre
        instance.bounding_sphere_radius = binary.bounding_sphere_radius
        instance.keep_bounding_box = binary.flags & 0x00000001 != 0
        instance.keep_bounding_sphere = binary.flags & 0x00000002 != 0
        
        bones,   \
        meshes,  \
        cameras, \
        lights = NodeInterface.binary_node_tree_to_list(binary.root_node)
        
        if instance.skinning_data.matrix_palette is not None:
            for mesh in meshes:
                if copy_verts:
                    mesh.vertices = copy.deepcopy(mesh.vertices)
                if mesh.vertices[0].indices is not None:
                    for v in mesh.vertices:
                        v.indices = v.indices[::-1]
                        #v.indices = [instance.skinning_data.matrix_palette[idx] for idx in v.indices[::-1]]
        return bones, meshes, cameras, lights, instance
        
    def to_binary(self, bones, meshes, cameras, lights, copy_verts=True):
        binary = ModelBinary()

        binary.flags = 0
        if self.skinning_data.bone_count is not None:
            binary.flags |= 0x00000004
        if self.keep_bounding_box:
            binary.flags |= 0x00000001
        if self.keep_bounding_sphere:
            binary.flags |= 0x00000002
        
        binary.skinning_data = self.skinning_data
        binary.bounding_box_max_dims = self.bounding_box_max_dims
        binary.bounding_box_min_dims = self.bounding_box_min_dims
        binary.bounding_sphere_centre = self.bounding_sphere_centre
        binary.bounding_sphere_radius = self.bounding_sphere_radius
        
        # Need to return mesh binary list here too!
        binary.root_node, old_node_id_to_new_node_id_map, mesh_binaries = NodeInterface.list_to_binary_node_tree(bones, meshes, cameras, lights)

        # Settle for just creating same matrix palette, don't care about order...
        # matrix_palette = set()
        # for mesh in meshes:
        #     if mesh.vertices[0].indices is not None:
        #         for v in mesh.vertices:
        #             for idx, wgt in zip(v.indices, v.weights):
        #                 if wgt > 0 and idx:
        #                     matrix_palette.add(idx)
        
        # if matrix_palette != set(self.skinning_data.matrix_palette):
        #     assert 0
    
        if binary.skinning_data.matrix_palette is not None:
            # This loses duplicates...
            #idx_lookup = {global_idx: palette_idx for palette_idx, global_idx in enumerate(binary.skinning_data.matrix_palette)}
            for mesh in mesh_binaries:
                if copy_verts:
                    mesh.vertices = copy.deepcopy(mesh.vertices)
                if mesh.vertices[0].indices is not None:
                    for v in mesh.vertices:
                        #v.indices = [idx_lookup[idx] for idx in v.indices]
                        # for i, (idx, wgt) in enumerate(zip(v.indices, v.weights)):
                        #     if wgt == 0:
                        #         v.indices[i] = 0
                        # Need to apply node ID map in here too, but can't
                        # because the skinning matrix affects it
                        v.indices = [idx for idx in v.indices[::-1]]
        return binary
        