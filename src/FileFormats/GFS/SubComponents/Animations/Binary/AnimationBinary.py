from ......serialization.formatters import HEX32_formatter
from ....Utils.Matrices import transforms_to_matrix, multiply_transform_matrices, transform_vector
from ...CommonStructures.SceneNode.EPL import EPLBinary
from ...CommonStructures.ObjectNameModule import ObjectName
from ...CommonStructures.CustomProperty   import PropertyBinary
from ...CommonStructures.BitVectorModule  import  BitVector0x20
from ...CommonStructures.SizedObjArrayModule import SizedObjArray
from .AnimController import AnimationControllerBinary
from .AnimTrack import AnimationTrackBinary
from ..NodeAnimation import NodeAnimation


class ParticlesError(Exception):
    pass


class AnimationFlags(BitVector0x20):
    has_node_anims     = BitVector0x20.DEF_FLAG(0x00) # USED (Normal, Blend, Unk)
    has_material_anims = BitVector0x20.DEF_FLAG(0x01) # USED (Normal, Blend, Unk)
    has_camera_anims   = BitVector0x20.DEF_FLAG(0x02) # USED (Normal)
    has_morph_anims    = BitVector0x20.DEF_FLAG(0x03) # USED (Normal, Blend)
    has_type_5_anims   = BitVector0x20.DEF_FLAG(0x04) # USED
    has_properties     = BitVector0x20.DEF_FLAG(0x17) # USED (Normal)
    has_speed          = BitVector0x20.DEF_FLAG(0x19) # USED (Normal, Blend)
    flag_26            = BitVector0x20.DEF_FLAG(0x1A) # USED (Blend)
    has_epls           = BitVector0x20.DEF_FLAG(0x1C)
    has_lookat_anims   = BitVector0x20.DEF_FLAG(0x1D) # USED (Normal)
    has_bounding_box   = BitVector0x20.DEF_FLAG(0x1E) # USED (Normal, Blend, Unk)
    has_extra_data     = BitVector0x20.DEF_FLAG(0x1F) # USED (Normal)


class AnimationBinary:
    def __init__(self):
        self.flags       = AnimationFlags()
        self.duration    = None
        
        self.controller_count = 0
        self.track_count      = 0
        self.anim_buffer_size = 0
        self.controllers      = []
        
        self.epls = SizedObjArray(EPLEntry)
        self.lookat_animations = None
        self.extra_track_data   = None
        # Bounding boxes should probably go into a custom datatype
        self.bounding_box_max_dims = None
        self.bounding_box_min_dims = None
        self.speed = None
        self.properties = SizedObjArray(PropertyBinary)
        
    def __repr__(self):
        return f"[GFDBinary::Animation {HEX32_formatter(self.flags._value)}] {self.duration}"

    def exbip_rw(self, rw, version):
        if version > 0x01104110:
            self.flags   = rw.rw_obj(self.flags)
        self.duration    = rw.rw_float32(self.duration)
        self.controller_count = rw.rw_uint32(self.controller_count)
        if version >= 0x02000000:
            self.track_count      = rw.rw_uint32(self.track_count)
            self.anim_buffer_size = rw.rw_uint32(self.anim_buffer_size)
            
        self.controllers = rw.rw_dynamic_objs(self.controllers, AnimationControllerBinary, self.controller_count, version)
        # Only certain flags used for certain chunk versions..?
        if self.flags.has_epls:
            rw.rw_obj(self.epls, version)
        if self.flags.has_lookat_anims:
            self.lookat_animations = rw.rw_dynamic_obj(self.lookat_animations, LookAtAnimationsBinary, version)
        if self.flags.has_extra_data:
            self.extra_track_data = rw.rw_dynamic_obj(self.extra_track_data, ExtraTrackData, version)
        if self.flags.has_bounding_box:
            self.bounding_box_max_dims = rw.rw_float32s(self.bounding_box_max_dims, 3)
            self.bounding_box_min_dims = rw.rw_float32s(self.bounding_box_min_dims, 3)
        if self.flags.has_speed:
            self.speed = rw.rw_float32(self.speed)
        if self.flags.has_properties:
            rw.rw_obj(self.properties, version)
        
            
    def calc_bounding_box(self, model_binary):
        def get_frame(dct, frame):
            smaller_frames = [f for f in dct if f <= frame]
            smallest_frame = max(smaller_frames) if len(smaller_frames) else list(dct.keys())[0]
            return dct[smallest_frame]
            
        # Get all relevant frames
        all_frames = set()
        node_anims = []
        for controller in self.controllers:
            if controller.type != 1:
                continue
            for track in controller.tracks:
                all_frames.update(set(track.frames))
            node_anims.append(NodeAnimation.from_controller(controller))
        all_frames = sorted(all_frames)
        
        # Flatten the node structure
        flat_nodes = model_binary.root_node.flattened()
        
        # Collect all bounding box vertices
        mesh_verts = []
        for node_idx, mesh in flat_nodes.meshes:
            if not mesh.flags.has_bounding_box:
                continue
            min_dims = mesh.bounding_box_min_dims
            max_dims = mesh.bounding_box_max_dims
            mesh_verts.append((node_idx, min_dims, max_dims))
        
        # Now measure the bounding box of the model on each frame
        frame_minima = []
        frame_maxima = []
        for frame_idx, frame in enumerate(all_frames):
            bone_data = [[b.position, b.rotation, b.scale] for b in flat_nodes.nodes]
            # Do the animation without interpolation since that sounds like
            # what might have been done
            for anim in node_anims:
                if len(anim.positions): bone_data[anim.id][0] = get_frame(anim.positions, frame)
                if len(anim.rotations): bone_data[anim.id][1] = get_frame(anim.rotations, frame)
                if len(anim.scales):    bone_data[anim.id][2] = get_frame(anim.scales,    frame)
            
            # Build bone matrices for the frame
            bone_matrices = [None for _ in range(len(flat_nodes.nodes))]
            for i, (bone, bd) in enumerate(zip(flat_nodes.nodes, bone_data)):
                matrix = transforms_to_matrix(*bd)
                parent_idx = flat_nodes.node_parents[i]
                if parent_idx > -1:
                    bone_matrices[i] = multiply_transform_matrices(bone_matrices[parent_idx], matrix)
                else:
                    bone_matrices[i] = matrix
            
            # Now do bounding box transforms
            bbox_verts = [None for _ in range(len(mesh_verts)*2)]
            for i, (node_idx, min_v, max_v) in enumerate(mesh_verts):
                bbox_verts[2*i+0] = transform_vector(bone_matrices[node_idx], min_v)
                bbox_verts[2*i+1] = transform_vector(bone_matrices[node_idx], max_v)
            
            # Identify bounding box for this frame
            min_v = [0, 0, 0]
            max_v = [0, 0, 0]
            if len(bbox_verts) or len(bone_matrices):
                for pidx in range(3):
                    dataset = [*[m[3 + 4*pidx] for m in bone_matrices], *[v[pidx] for v in bbox_verts]]
                    min_v[pidx] = min(dataset)
                    max_v[pidx] = max(dataset)
            
            frame_minima.append(min_v)
            frame_maxima.append(max_v)
        
        # Export global min/max
        global_min = [0, 0, 0]
        global_max = [0, 0, 0]
        if len(frame_minima):
            for pidx in range(3):
                global_min[pidx] = min([v[pidx] for v in frame_minima])
                global_max[pidx] = max([v[pidx] for v in frame_maxima])
        return global_min, global_max

    def autocalc_bounding_box(self, model_binary):   
        self.bounding_box_min_dims, self.bounding_box_max_dims = self.calc_bounding_box(model_binary)
        if self.bounding_box_min_dims is not None:
            self.flags.has_bounding_box = True


class EPLEntry:
    def __init__(self):
        self.epl = EPLBinary.EPLBinary()
        self.name = ObjectName()
        
    def exbip_rw(self, rw, version):
        rw.rw_obj(self.epl, version)
        rw.rw_obj(self.name, version)


class LookAtAnimationsBinary:
    def __init__(self):
        self.right        = AnimationBinary()
        self.right_factor = None
        self.left         = AnimationBinary()
        self.left_factor  = None
        self.up           = AnimationBinary()
        self.up_factor    = None
        self.down         = AnimationBinary()
        self.down_factor  = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::LookAtAnimationsBinary] {self.right_factor} {self.left_factor} {self.up_factor} {self.down_factor}"
        
    def exbip_rw(self, rw, version):
        rw.rw_obj(self.right, version)
        self.right_factor = rw.rw_float32(self.right_factor)
        rw.rw_obj(self.left, version)
        self.left_factor  = rw.rw_float32(self.left_factor)
        rw.rw_obj(self.up, version)
        self.up_factor    = rw.rw_float32(self.up_factor)
        rw.rw_obj(self.down, version)
        self.down_factor  = rw.rw_float32(self.down_factor)


class ExtraTrackData:
    def __init__(self):
        self.flags = 0
        self.name = ObjectName()
        self.track = AnimationTrackBinary()
        
    def __repr__(self, version):
        return f"[GFDBinary::Animation::ExtraTrackData {HEX32_formatter(self.flags)}] {self.name}"
        
    def exbip_rw(self, rw, version):
        self.flags = rw.rw_uint32(self.flags)
        rw.rw_obj(self.name, version, version < 0x02000000)
        rw.rw_obj(self.track, version)
