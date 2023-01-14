from ...serialization.BinaryTargets import OffsetTracker
from .Binary import GFSBinary
from .SubComponents.GFS0ContainerBinary import GFS0ContainerBinary

from .SubComponents.Materials.Interface import MaterialInterface
from .SubComponents.Materials.Binary import MaterialPayload
from .SubComponents.Textures.Interface import TextureInterface
from .SubComponents.Textures.Binary import TexturePayload
from .SubComponents.Animations.Interface import AnimationInterface
from .SubComponents.Model.Interface import ModelInterface
from .SubComponents.CommonStructures import NodeInterface, MeshInterface


class UnknownAnimations:
    def __init__(self):
        self.anim_1 = None
        self.anim_1_float = None
        self.anim_2 = None
        self.anim_2_float = None
        self.anim_3 = None
        self.anim_3_float = None
        self.anim_4 = None
        self.anim_4_float = None

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
        self.blend_animations = []
        self.unknown_animations = UnknownAnimations()
        
        # Things that need to be removed eventually
        self.animation_data  = None
        self.data_0x000100F8 = None
        self.physics_data    = None


    @classmethod
    def from_file(cls, filepath):
        binary = GFSBinary()
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
                instance.blend_animations = [AnimationInterface.from_binary(anim) for anim in ctr.data.blend_animations]
                if ctr.data.flags.has_unknown_chunk:
                    instance.unknown_animations.anim_1       = AnimationInterface.from_binary(ctr.data.unknown_anim_chunk.anim_1)
                    instance.unknown_animations.anim_1_float = ctr.data.unknown_anim_chunk.unknown_1
                    instance.unknown_animations.anim_2       = AnimationInterface.from_binary(ctr.data.unknown_anim_chunk.anim_2)
                    instance.unknown_animations.anim_2_float = ctr.data.unknown_anim_chunk.unknown_2
                    instance.unknown_animations.anim_3       = AnimationInterface.from_binary(ctr.data.unknown_anim_chunk.anim_3)
                    instance.unknown_animations.anim_3_float = ctr.data.unknown_anim_chunk.unknown_3
                    instance.unknown_animations.anim_4       = AnimationInterface.from_binary(ctr.data.unknown_anim_chunk.anim_4)
                    instance.unknown_animations.anim_4_float = ctr.data.unknown_anim_chunk.unknown_4
            elif ctr.type == 0x000100F8:
                instance.data_0x000100F8 = ctr.data
            elif ctr.type == 0x000100F9:
                instance.physics_data = ctr.data
        
        return instance
    
    def to_binary(self, version, duplicate_data=False):
        binary = GFSBinary()
        
        ot = OffsetTracker()
        
        # Start container
        start_ctr = GFS0ContainerBinary()
        start_ctr.version = version
        start_ctr.type = 0x00000001
        ot.rw_obj(start_ctr)
        start_ctr.size = 0
        binary.containers.append(start_ctr)
        
        # Textures container
        if len(self.materials): # Unless textures are stored externally?
            offset = ot.tell()
            tex_ctr = GFS0ContainerBinary()
            tex_ctr.version = version
            tex_ctr.type = 0x000100FC
            
            tex_array = TexturePayload()
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
            mat_ctr.version = version
            mat_ctr.type = 0x000100FB
            
            mat_array = MaterialPayload()
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
            mdl_ctr.version = version
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
            anm_ctr.version = version
            anm_ctr.type = 0x000100FD
            
            anm_ctr.data = self.animation_data
            ot.rw_obj(anm_ctr)
            anm_ctr.size = ot.tell() - offset
            binary.containers.append(anm_ctr)
            
        # Physics container
        if self.physics_data is not None:
            offset = ot.tell()
            physics_ctr = GFS0ContainerBinary()
            physics_ctr.version = version
            physics_ctr.type = 0x000100F9
            
            physics_ctr.data = self.physics_data
            ot.rw_obj(physics_ctr)
            physics_ctr.size = ot.tell() - offset
            binary.containers.append(physics_ctr)
            
        # Unknown container
        if self.data_0x000100F8 is not None:
            offset = ot.tell()
            unk_ctr = GFS0ContainerBinary()
            unk_ctr.version = version
            unk_ctr.type = 0x000100F8
            
            unk_ctr.data = self.data_0x000100F8
            unk_ctr.size = len(self.data_0x000100F8.data) + 0x10
            # ot.rw_obj(unk_ctr)
            # unk_ctr.size = ot.tell() - offset
            binary.containers.append(unk_ctr)
        
        # End container
        if not (len(binary.containers) == 2 and binary.containers[-1].type == 0x000100FD):
            end_ctr = GFS0ContainerBinary()
            end_ctr.version = version
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
