from ...serialization.parsers import GFSOffsetTracker
from .Binary import GFSBinary, EPLFileBinary
from .SubComponents.GFS0ContainerBinary import GFS0ContainerBinary

from .SubComponents.Materials.Interface import MaterialInterface
from .SubComponents.Materials.Binary import MaterialPayload
from .SubComponents.Textures.Interface import TextureInterface
from .SubComponents.Textures.Binary import TexturePayload
from .SubComponents.Animations import AnimationPayload, AnimationInterface, LookAtAnimationsInterface
from .SubComponents.Model.Interface import ModelInterface
from .SubComponents.CommonStructures import NodeInterface, MeshInterface, LightInterface, CameraInterface, EPLInterface

from .SubComponents.GFS0ContainerBinary import UnsupportedVersionError
from .SubComponents.Animations.Binary.AnimationBinary import ParticlesError


class GFSInterface:
    def __init__(self):
        self.version              = 0x01105100
        self.keep_bounding_box    = False
        self.keep_bounding_sphere = False
        
        self.flag_3    = False
        self.meshes    = []
        self.cameras   = []
        self.lights    = []
        self.epls      = []
        self.bones     = []
        self.materials = []
        self.textures  = []
        
        self.anim_flag_0 = False
        self.anim_flag_1 = False
        self.anim_flag_3 = True
        self.anim_flag_4 = False
        self.anim_flag_5 = False
        self.anim_flag_6 = False
        self.anim_flag_7 = False
        self.anim_flag_8 = False
        self.anim_flag_9 = False
        self.anim_flag_10 = False
        self.anim_flag_11 = False
        self.anim_flag_12 = False
        self.anim_flag_13 = False
        self.anim_flag_14 = False
        self.anim_flag_15 = False
        self.anim_flag_16 = False
        self.anim_flag_17 = False
        self.anim_flag_18 = False
        self.anim_flag_19 = False
        self.anim_flag_20 = False
        self.anim_flag_21 = False
        self.anim_flag_22 = False
        self.anim_flag_23 = False
        self.anim_flag_24 = False
        self.anim_flag_25 = False
        self.anim_flag_26 = False
        self.anim_flag_27 = False
        self.anim_flag_28 = False
        self.anim_flag_29 = False
        self.anim_flag_30 = False
        self.anim_flag_31 = False
        self.animations        = []
        self.blend_animations  = []
        self.lookat_animations = None
        
        self.overrides = ModelOverrides()
        
        # Things that need to be removed eventually
        self.has_end_container = True
        self.animation_data  = None
        self.data_0x000100F8 = None
        self.physics_data    = None


    @classmethod
    def from_file(cls, filepath, warnings=None):
        binary = GFSBinary()
        binary.read(filepath, warnings=warnings)
        return cls.from_binary(binary, duplicate_data=False, warnings=warnings)

    @classmethod
    def from_bytes(cls, bytes_, warnings=None):
        binary = GFSBinary()
        binary.frombytes(bytes_, warnings=warnings)
        return cls.from_binary(binary, duplicate_data=False, warnings=warnings)

    @classmethod
    def from_binary(cls, binary, duplicate_data=True, warnings=None):
        instance = cls()
        
        instance.has_end_container = False
        for ctr in binary.containers:
            if ctr.type == 0x00000001 or ctr.type == 0x00000008:
                # All blocks must have a version, but this is always the same
                # and the "start" block must always exist... so get it from here
                instance.version = ctr.version
            elif ctr.type == 0x000100FC:
                instance.textures = [TextureInterface.from_binary(tx) for tx in ctr.data]
            elif ctr.type == 0x000100FB:
                instance.materials = [MaterialInterface.from_binary(mb) for mb in ctr.data]
            elif ctr.type == 0x00010003:
                instance.bones,                 \
                instance.meshes,                \
                instance.cameras,               \
                instance.lights,                \
                instance.epls,                  \
                bounding_box_min_dims, \
                bounding_box_max_dims, \
                bounding_sphere_centre,\
                bounding_sphere_radius,\
                instance.flag_3 = ModelInterface.from_binary(ctr.data, duplicate_data, warnings)
                instance.keep_bounding_box    = (bounding_box_min_dims  is not None) or (bounding_box_max_dims  is not None)
                instance.keep_bounding_sphere = (bounding_sphere_centre is not None) or (bounding_sphere_radius is not None)
                
                if instance.keep_bounding_box:
                    instance.overrides.bounding_box.min_dims  = bounding_box_min_dims
                    instance.overrides.bounding_box.max_dims  = bounding_box_max_dims
                if instance.keep_bounding_sphere:
                    instance.overrides.bounding_sphere.center = bounding_sphere_centre
                    instance.overrides.bounding_sphere.radius = bounding_sphere_radius
            elif ctr.type == 0x000100FD:
                instance.animation_data = ctr.data
                instance.anim_flag_0    = ctr.data.flags.flag_0
                instance.anim_flag_1    = ctr.data.flags.flag_1
                instance.anim_flag_3    = ctr.data.flags.flag_3
                instance.anim_flag_4    = ctr.data.flags.flag_4
                instance.anim_flag_5    = ctr.data.flags.flag_5
                instance.anim_flag_6    = ctr.data.flags.flag_6
                instance.anim_flag_7    = ctr.data.flags.flag_7
                instance.anim_flag_8    = ctr.data.flags.flag_8
                instance.anim_flag_9    = ctr.data.flags.flag_9
                instance.anim_flag_10   = ctr.data.flags.flag_10
                instance.anim_flag_11   = ctr.data.flags.flag_11
                instance.anim_flag_12   = ctr.data.flags.flag_12
                instance.anim_flag_13   = ctr.data.flags.flag_13
                instance.anim_flag_14   = ctr.data.flags.flag_14
                instance.anim_flag_15   = ctr.data.flags.flag_15
                instance.anim_flag_16   = ctr.data.flags.flag_16
                instance.anim_flag_17   = ctr.data.flags.flag_17
                instance.anim_flag_18   = ctr.data.flags.flag_18
                instance.anim_flag_19   = ctr.data.flags.flag_19
                instance.anim_flag_20   = ctr.data.flags.flag_20
                instance.anim_flag_21   = ctr.data.flags.flag_21
                instance.anim_flag_22   = ctr.data.flags.flag_22
                instance.anim_flag_23   = ctr.data.flags.flag_23
                instance.anim_flag_24   = ctr.data.flags.flag_24
                instance.anim_flag_25   = ctr.data.flags.flag_25
                instance.anim_flag_26   = ctr.data.flags.flag_26
                instance.anim_flag_27   = ctr.data.flags.flag_27
                instance.anim_flag_28   = ctr.data.flags.flag_28
                instance.anim_flag_29   = ctr.data.flags.flag_29
                instance.anim_flag_30   = ctr.data.flags.flag_30
                instance.anim_flag_31   = ctr.data.flags.flag_31
                instance.animations = [AnimationInterface.from_binary(anim) for anim in ctr.data.animations]
                instance.blend_animations = [AnimationInterface.from_binary(anim) for anim in ctr.data.blend_animations]
                if ctr.data.flags.has_lookat_anims:
                    instance.lookat_animations = LookAtAnimationsInterface.from_binary(ctr.data.lookat_animations)
            elif ctr.type == 0x000100F8:
                instance.data_0x000100F8 = ctr.data
            elif ctr.type == 0x000100F9:
                instance.physics_data = ctr.data
            elif ctr.type == 0x00000000:
                instance.has_end_container = True
        
        return instance

    def to_file(self, filepath, endianness, anim_model_binary=None):
        binary = self.to_binary(duplicate_data=True, anim_model_binary=anim_model_binary)
        binary.write(filepath, endianness)

    def to_bytes(self, endianness, anim_model_binary=None):
        binary = self.to_binary(duplicate_data=True, anim_model_binary=anim_model_binary)
        return binary.tobytes(endianness)

    def to_binary(self, duplicate_data=False, anim_model_binary=None):
        binary = GFSBinary()
        
        ot = GFSOffsetTracker()
        
        # Start container
        start_ctr = GFS0ContainerBinary()
        start_ctr.version = self.version
        if self.version >= 0x02000000:
            start_ctr.type = 0x00000008
        else:
            start_ctr.type = 0x00000001
        ot.rw_obj(start_ctr)
        start_ctr.size = 0
        binary.containers.append(start_ctr)
        
        # Textures container
        if len(self.materials): # Unless textures are stored externally?
            offset = ot.tell()
            tex_ctr = GFS0ContainerBinary()
            tex_ctr.version = self.version
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
            mat_ctr.version = self.version
            mat_ctr.type = 0x000100FB
            
            mat_array = MaterialPayload()
            mat_array.data = [mi.to_binary() for mi in self.materials]
            mat_array.count = len(mat_array.data)
            mat_ctr.data = mat_array
            ot.rw_obj(mat_ctr)
            mat_ctr.size = ot.tell() - offset
            binary.containers.append(mat_ctr)
            
        # Model container
        old_node_id_to_new_node_id_map = None
        if len(self.bones):
            offset = ot.tell()
            mdl_ctr = GFS0ContainerBinary()
            mdl_ctr.version = self.version
            mdl_ctr.type = 0x00010003
            
            model_binary, old_node_id_to_new_node_id_map = ModelInterface.to_binary(self.bones, self.meshes, self.cameras, self.lights, self.epls, self.keep_bounding_box, self.keep_bounding_sphere, self.overrides, self.flag_3, copy_verts=duplicate_data)
            mdl_ctr.data = model_binary
            ot.rw_obj(mdl_ctr)
            mdl_ctr.size = ot.tell() - offset
            binary.containers.append(mdl_ctr)
        
        if ((len(self.animations) > 0) or
            (len(self.blend_animations) > 0) or 
            (self.lookat_animations is not None)):
            offset = ot.tell()
            anm_ctr = GFS0ContainerBinary()
            anm_ctr.version = self.version
            anm_ctr.type = 0x000100FD
            
            #anm_ctr.data = self.animation_data
            anm_ctr.data = AnimationPayload()
            anm_ctr.data.flags.flag_0  = self.anim_flag_0
            anm_ctr.data.flags.flag_1  = self.anim_flag_1
            anm_ctr.data.flags.has_lookat_anims = self.lookat_animations is not None
            anm_ctr.data.flags.flag_3  = self.anim_flag_3
            anm_ctr.data.flags.flag_4  = self.anim_flag_4
            anm_ctr.data.flags.flag_5  = self.anim_flag_5
            anm_ctr.data.flags.flag_6  = self.anim_flag_6
            anm_ctr.data.flags.flag_7  = self.anim_flag_7
            anm_ctr.data.flags.flag_8  = self.anim_flag_8
            anm_ctr.data.flags.flag_9  = self.anim_flag_9
            anm_ctr.data.flags.flag_10 = self.anim_flag_10
            anm_ctr.data.flags.flag_11 = self.anim_flag_11
            anm_ctr.data.flags.flag_12 = self.anim_flag_12
            anm_ctr.data.flags.flag_13 = self.anim_flag_13
            anm_ctr.data.flags.flag_14 = self.anim_flag_14
            anm_ctr.data.flags.flag_15 = self.anim_flag_15
            anm_ctr.data.flags.flag_16 = self.anim_flag_16
            anm_ctr.data.flags.flag_17 = self.anim_flag_17
            anm_ctr.data.flags.flag_18 = self.anim_flag_18
            anm_ctr.data.flags.flag_19 = self.anim_flag_19
            anm_ctr.data.flags.flag_20 = self.anim_flag_20
            anm_ctr.data.flags.flag_21 = self.anim_flag_21
            anm_ctr.data.flags.flag_22 = self.anim_flag_22
            anm_ctr.data.flags.flag_23 = self.anim_flag_23
            anm_ctr.data.flags.flag_24 = self.anim_flag_24
            anm_ctr.data.flags.flag_25 = self.anim_flag_25
            anm_ctr.data.flags.flag_26 = self.anim_flag_26
            anm_ctr.data.flags.flag_27 = self.anim_flag_27
            anm_ctr.data.flags.flag_28 = self.anim_flag_28
            anm_ctr.data.flags.flag_29 = self.anim_flag_29
            anm_ctr.data.flags.flag_30 = self.anim_flag_30
            anm_ctr.data.flags.flag_31 = self.anim_flag_31
            
            if anim_model_binary is None:
                anim_model_binary = model_binary
            anm_ctr.data.animations.count = len(self.animations)
            anm_ctr.data.animations.data  = [a.to_binary(anim_model_binary, old_node_id_to_new_node_id_map, self.version) for a in self.animations]
            anm_ctr.data.blend_animations.count = len(self.blend_animations)
            anm_ctr.data.blend_animations.data  = [a.to_binary(anim_model_binary, old_node_id_to_new_node_id_map, self.version) for a in self.blend_animations]
            if anm_ctr.data.flags.has_lookat_anims:
                anm_ctr.data.lookat_animations = self.lookat_animations.to_binary(anim_model_binary, old_node_id_to_new_node_id_map, self.version)
  
            ot.rw_obj(anm_ctr)
            anm_ctr.size = ot.tell() - offset
            binary.containers.append(anm_ctr)
            
            
        # Physics container
        if self.physics_data is not None:
            offset = ot.tell()
            physics_ctr = GFS0ContainerBinary()
            physics_ctr.version = self.version
            physics_ctr.type = 0x000100F9
            
            physics_ctr.data = self.physics_data
            ot.rw_obj(physics_ctr)
            physics_ctr.size = ot.tell() - offset
            binary.containers.append(physics_ctr)
            
        # Unknown container
        if self.data_0x000100F8 is not None:
            offset = ot.tell()
            unk_ctr = GFS0ContainerBinary()
            unk_ctr.version = self.version
            unk_ctr.type = 0x000100F8
            
            unk_ctr.data = self.data_0x000100F8
            unk_ctr.size = len(self.data_0x000100F8.data) + 0x10
            # ot.rw_obj(unk_ctr)
            # unk_ctr.size = ot.tell() - offset
            binary.containers.append(unk_ctr)
        
        # End container
        if self.has_end_container:
            end_ctr = GFS0ContainerBinary()
            end_ctr.version = self.version
            end_ctr.type = 0x00000000
            
            end_ctr.size = 0
            binary.containers.append(end_ctr)
            
        return binary
    
    def add_node(self, parent_idx, name, position, rotation, scale, unknown_float, bind_pose_matrix):
        node = NodeInterface()
        node.parent_idx = parent_idx
        node.name = name
        node.position = position
        node.rotation = rotation
        node.scale = scale
        node.unknown_float = unknown_float
        node.bind_pose_matrix = bind_pose_matrix
        node.properties = []
        self.bones.append(node)
        return node
        
    def add_mesh(self, node_id, vertices, material_name, indices, morphs, unknown_0x12, stride_type, unknown_float_1, unknown_float_2, keep_bounding_box, keep_bounding_sphere):
        mesh = MeshInterface()
        mesh.node            = node_id
        mesh.vertices        = vertices
        mesh.material_name   = material_name
        mesh.indices         = indices
        mesh.morphs = morphs
        mesh.unknown_0x12    = unknown_0x12
        mesh.stride_type     = stride_type
        mesh.unknown_float_1 = unknown_float_1
        mesh.unknown_float_2 = unknown_float_2
        
        if len(indices): mesh.index_type = 2 if len(vertices) >= 2**16 else 1
        else:            mesh.index_type = 1
        mesh.keep_bounding_box    = keep_bounding_box
        mesh.keep_bounding_sphere = keep_bounding_sphere
        
        self.meshes.append(mesh)
        return mesh
    
    def add_material(self, name):
        material = MaterialInterface()
        material.name = name
        self.materials.append(material)
        return material

    def add_texture(self, name, data, unknown_1, unknown_2, unknown_3, unknown_4):
        texture = TextureInterface()
        texture.name = name
        texture.image_data = data
        texture.unknown_1 = unknown_1
        texture.unknown_2 = unknown_2
        texture.unknown_3 = unknown_3
        texture.unknown_4 = unknown_4
        self.textures.append(texture)
        return texture
    
    def add_light(self, node_id, type, color_1, color_2, color_3):
        li = LightInterface()
        
        li.node        = node_id
        li.binary.type = type
        li.binary.color_1 = color_1
        li.binary.color_2 = color_2
        li.binary.color_3 = color_3
        self.lights.append(li)
        return li.binary

    def add_camera(self, node_id, view_matrix, zNear, zFar, fov, aspect_ratio, unknown_0x50, unknown_0x54, unknown_0x55, unknown_0x59):
        cam = CameraInterface()
        
        cam.node                = node_id
        cam.binary.view_matrix  = view_matrix
        cam.binary.zNear        = zNear
        cam.binary.zFar         = zFar
        cam.binary.fov          = fov
        cam.binary.aspect_ratio = aspect_ratio
        cam.binary.unknown_0x50 = unknown_0x50
        cam.binary.unknown_0x54 = unknown_0x54
        cam.binary.unknown_0x55 = unknown_0x55
        cam.binary.unknown_0x59 = unknown_0x59
        self.cameras.append(cam)
        return cam
    
    def add_epl(self, node_id, binary):
        epl = EPLInterface()
        epl.node   = node_id
        epl.binary = binary
        self.epls.append(epl)
        return epl

    def add_animation(self):
        anim = AnimationInterface()
        self.animations.append(anim)
        return anim
    
    def add_blend_animation(self):
        anim = AnimationInterface()
        self.blend_animations.append(anim)
        return anim
    
    def add_lookat_animations(self, up_factor, down_factor, left_factor, right_factor):
        self.lookat_animations = LookAtAnimationsInterface()
        la_a = self.lookat_animations
        la_a.up    = AnimationInterface()
        la_a.down  = AnimationInterface()
        la_a.left  = AnimationInterface()
        la_a.right = AnimationInterface()
        
        la_a.up_factor    = up_factor
        la_a.down_factor  = down_factor
        la_a.left_factor  = left_factor
        la_a.right_factor = right_factor
        
        return la_a.up, la_a.down, la_a.left, la_a.right


class BoundingBoxOverride:
    def __init__(self):
        self.enabled = False
        self.min_dims = [0, 0, 0]
        self.max_dims = [0, 0, 0]


class BoundingSphereOverride:
    def __init__(self):
        self.enabled = False
        self.center = [0, 0, 0]
        self.radius = 0


class ModelOverrides:
    def __init__(self):
        self._bounding_box    = BoundingBoxOverride()
        self._bounding_sphere = BoundingSphereOverride()
    
    @property
    def bounding_box(self):
        return self._bounding_box
    
    @property
    def bounding_sphere(self):
        return self._bounding_sphere


# This needs to be replaced by the standard "EPLInterface"...
class EPLFileInterface(EPLInterface):
    def __init__(self):
        super().__init__()
        self.version = 0x01105100
    
    @classmethod
    def from_binary(cls, binary):
        instance = super().from_binary(None, binary.epl)
        instance.version = binary.start_block.version
        return instance
    
    @classmethod
    def from_file(cls, filepath):
        binary = EPLFileBinary()
        binary.read(filepath)
        return cls.from_binary(binary)

    def to_file(self, filepath, endianness):
        binary = self.to_binary()
        binary.write(filepath, endianness)

    def to_binary(self):
        if self.version is None:
            raise ValueError("EPL version is None. Ensure that this is set to an appropriate value, such as 0x01105100")
        
        binary = EPLFileBinary()
        binary.start_block.version = self.version
        binary.start_block.type    = 0x00000001
        binary.start_block.size    = 0
        binary.epl = super().to_binary()
        
        return binary
