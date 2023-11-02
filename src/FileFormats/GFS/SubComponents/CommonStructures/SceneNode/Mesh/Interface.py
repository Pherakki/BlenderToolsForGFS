from .MeshBinary import MeshBinary


class MeshInterface:
    def __init__(self):
        self.node    = None
        
        self.flag_5  = None
        self.flag_7  = None
        self.flag_8  = None
        self.flag_9  = None
        self.flag_10 = None
        self.flag_11 = None
        self.flag_13 = None
        self.flag_14 = None
        self.flag_15 = None
        self.flag_16 = None
        self.flag_17 = None
        self.flag_18 = None
        self.flag_19 = None
        self.flag_20 = None
        self.flag_21 = None
        self.flag_22 = None
        self.flag_23 = None
        self.flag_24 = None
        self.flag_25 = None
        self.flag_26 = None
        self.flag_27 = None
        self.flag_28 = None
        self.flag_29 = None
        self.flag_30 = None
        self.flag_31 = None
    
        self.vertices = None
        self.material_name = None
        self.indices = None
        self.morphs = []
        self.unknown_0x12 = None
        self.unknown_float_1 = None
        self.unknown_float_2 = None
        
        self._overrides = MeshOverrides()
        
        # THINGS THAT COULD BE REMOVABLE
        self.index_type = None
        self.keep_bounding_box = None
        self.keep_bounding_sphere = None
        
    @property
    def overrides(self):
        return self._overrides
    
    @classmethod
    def from_binary(cls, node_idx, binary):
        instance = cls()
        
        # Deal with unpacking later...
        instance.node = node_idx
        
        # Can get rid of some of these in a minute
        # 0x00000001 says if weights are used
        # 0x00000002 says if a material is used
        # 0x00000004 says if indices are present
        instance.keep_bounding_box    = binary.flags.has_bounding_box
        instance.keep_bounding_sphere = binary.flags.has_bounding_sphere
        instance.flag_5               = binary.flags.flag_5
        # 0x00000040 says if any morphs are present
        instance.flag_7               = binary.flags.flag_7
        instance.flag_8               = binary.flags.flag_8
        instance.flag_9               = binary.flags.flag_9
        instance.flag_10              = binary.flags.flag_10
        instance.flag_11              = binary.flags.flag_11
        # 0x00001000 says if unknown floats are present
        instance.flag_13              = binary.flags.flag_13
        instance.flag_14              = binary.flags.flag_14
        instance.flag_15              = binary.flags.flag_15
        instance.flag_16              = binary.flags.flag_16
        instance.flag_17              = binary.flags.flag_17
        instance.flag_18              = binary.flags.flag_18
        instance.flag_19              = binary.flags.flag_19
        instance.flag_20              = binary.flags.flag_20
        instance.flag_21              = binary.flags.flag_21
        instance.flag_22              = binary.flags.flag_22
        instance.flag_23              = binary.flags.flag_23
        instance.flag_24              = binary.flags.flag_24
        instance.flag_25              = binary.flags.flag_25
        instance.flag_26              = binary.flags.flag_26
        instance.flag_27              = binary.flags.flag_27
        instance.flag_28              = binary.flags.flag_28
        instance.flag_29              = binary.flags.flag_29
        instance.flag_30              = binary.flags.flag_30
        instance.flag_31              = binary.flags.flag_31
        
        instance.vertices        = binary.vertices
        instance.material_name   = binary.material_name.string
        instance.indices         = binary.indices
        instance.index_type      = binary.index_type # Can probably remove this...
        instance.morphs          = [t.position_deltas for t in binary.morph_data.targets]
        instance.unknown_0x12    = binary.unknown_0x12
        instance.unknown_float_1 = binary.unknown_float_1
        instance.unknown_float_2 = binary.unknown_float_2
        
        instance.overrides.bounding_box.max_dims  = binary.bounding_box_max_dims
        instance.overrides.bounding_box.min_dims  = binary.bounding_box_min_dims
        instance.overrides.bounding_sphere.center = binary.bounding_sphere_centre
        instance.overrides.bounding_sphere.radius = binary.bounding_sphere_radius
        
        return instance
        
    def to_binary(self):
        binary = MeshBinary()
        
        if len(self.vertices):
            # Assume that if something is true for the first vertex
            # Empty - 0x00000001 # << 0
            binary.vertex_format.has_positions  = (self.vertices[0].position  is not None) # 0x00000002
            # Empty - 0x00000004 # << 2
            # Empty - 0x00000008 # << 3
            binary.vertex_format.has_normals    = (self.vertices[0].normal    is not None) # 0x00000010
            # Empty - 0x00000020 # << 5
            binary.vertex_format.has_color1     = (self.vertices[0].color1    is not None) # 0x00000040
            # Empty - 0x00000080 # << 7
            binary.vertex_format.has_texcoord_0 = (self.vertices[0].texcoord0 is not None) # 0x00000100
            binary.vertex_format.has_texcoord_1 = (self.vertices[0].texcoord1 is not None) # 0x00000200
            binary.vertex_format.has_texcoord_2 = (self.vertices[0].texcoord2 is not None) # 0x00000400
            binary.vertex_format.has_texcoord_3 = (self.vertices[0].texcoord3 is not None) # 0x00000800
            binary.vertex_format.has_texcoord_4 = (self.vertices[0].texcoord4 is not None) # 0x00001000
            binary.vertex_format.has_texcoord_5 = (self.vertices[0].texcoord5 is not None) # 0x00002000
            binary.vertex_format.has_texcoord_6 = (self.vertices[0].texcoord6 is not None) # 0x00004000
            binary.vertex_format.has_texcoord_7 = (self.vertices[0].texcoord7 is not None) # 0x00008000
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
            binary.vertex_format.has_tangents    = (self.vertices[0].tangent  is not None) # 0x10000000
            binary.vertex_format.has_binormals   = (self.vertices[0].binormal is not None) # 0x20000000
            binary.vertex_format.has_color2      = (self.vertices[0].color2   is not None) # 0x40000000
            # Empty - 0x80000000 # << 31
            
            binary.flags.has_weights = (self.vertices[0].indices is not None)
        
        binary.flags.has_material        = (self.material_name is not None)
        binary.flags.has_indices         = (len(self.indices) > 0)
        binary.flags.has_bounding_box    = self.keep_bounding_box
        binary.flags.has_bounding_sphere = self.keep_bounding_sphere
        binary.flags.flag_5              = self.flag_5
        if len(self.morphs):
            binary.flags.has_morphs      = not (self.morphs.count is None or self.morphs.count == 0)
        else:
            binary.flags.has_morphs = False
        binary.flags.flag_7              = self.flag_7
        binary.flags.flag_8              = self.flag_8
        binary.flags.flag_9              = self.flag_9
        binary.flags.flag_10             = self.flag_10
        binary.flags.flag_11             = self.flag_11
        if self.unknown_float_1 is None and self.unknown_float_2 is None:
            pass
        else:
            binary.flags.has_unknown_floats = True
            binary.unknown_float_1 = self.unknown_float_1
            binary.unknown_float_2 = self.unknown_float_2
            if self.unknown_float_1 is None:
                binary.unknown_float_1 = 0.
            if self.unknown_float_2 is None:
                binary.unknown_float_2 = 0.
        binary.flags.flag_13 = self.flag_13
        binary.flags.flag_14 = self.flag_14
        binary.flags.flag_15 = self.flag_15
        binary.flags.flag_16 = self.flag_16
        binary.flags.flag_17 = self.flag_17
        binary.flags.flag_18 = self.flag_18
        binary.flags.flag_19 = self.flag_19
        binary.flags.flag_20 = self.flag_20
        binary.flags.flag_21 = self.flag_21
        binary.flags.flag_22 = self.flag_22
        binary.flags.flag_23 = self.flag_23
        binary.flags.flag_24 = self.flag_24
        binary.flags.flag_25 = self.flag_25
        binary.flags.flag_26 = self.flag_26
        binary.flags.flag_27 = self.flag_27
        binary.flags.flag_28 = self.flag_28
        binary.flags.flag_29 = self.flag_29
        binary.flags.flag_30 = self.flag_30
        binary.flags.flag_31 = self.flag_31
        
        if len(self.indices) % 3:
            raise ValueError("Mesh contains {len(self.indices)} indices; must be a multiple of 3")
        binary.tri_count     = len(self.indices) // 3
        binary.index_type    = self.index_type
        binary.vertex_count  = len(self.vertices)
        binary.unknown_0x12  = self.unknown_0x12
        binary.vertices      = self.vertices
        if len(self.morphs):
            binary.morph_data.flags = 2
            binary.morph_data.count = 0
            for position_deltas in self.morphs:
                binary.morph_data.add_target(2, position_deltas)
        binary.indices       = self.indices
        if self.material_name is not None:
            binary.material_name = binary.material_name.from_name(self.material_name)
        
        ####################
        # BOUNDING VOLUMES #
        ####################
        if self.keep_bounding_box:
            box = self.overrides.bounding_box
            if box.enabled:
                binary.bounding_box_min_dims = box.min_dims
                binary.bounding_box_max_dims = box.max_dims
            else:
                if binary.vertex_format.has_positions:
                    binary.autocalc_bounding_box()
                else:
                    raise ValueError("Mesh is marked for bounding box export, but has no vertex position data")
        
        if self.keep_bounding_sphere:
            sph = self.overrides.bounding_sphere
            if sph.enabled:
                binary.bounding_sphere_centre = sph.center
                binary.bounding_sphere_radius = sph.radius
            else:
                if binary.vertex_format.has_positions:
                    binary.autocalc_bounding_sphere()
                else:
                    raise ValueError("Mesh is marked for bounding sphere export, but has no vertex position data")
        
        return binary
    
    def calc_bounding_box(self):
        return MeshBinary.calc_bounding_box(self)
    
    def calc_bounding_sphere(self):
        return MeshBinary.calc_bounding_sphere(self)


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


class MeshOverrides:
    def __init__(self):
        self._bounding_box    = BoundingBoxOverride()
        self._bounding_sphere = BoundingSphereOverride()
    
    @property
    def bounding_box(self):
        return self._bounding_box
    
    @property
    def bounding_sphere(self):
        return self._bounding_sphere
