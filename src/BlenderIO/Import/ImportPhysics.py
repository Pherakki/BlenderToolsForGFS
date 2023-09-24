from ..Utils.PhysicsGen import make_collider


collider_types = {0: "Sphere", 1: "Capsule"}


def import_physics(gfs, bpy_obj):
    if gfs.physics_data is not None:
        props = bpy_obj.data.GFSTOOLS_ModelProperties.physics
        gfs_phys = gfs.physics_data
        
        props.has_physics = True
        props.unknown_0x00 = gfs_phys.unknown_0x00
        props.unknown_0x04 = gfs_phys.unknown_0x04
        props.unknown_0x08 = gfs_phys.unknown_0x08
        props.unknown_0x0C = gfs_phys.unknown_0x0C
        props.unknown_0x10 = gfs_phys.unknown_0x10
        
        for bone in gfs_phys.physics_bones:
            b_bone = props.bones.add()
            b_bone.has_name = bone.has_name
            b_bone.name = bone.name.string if bone.name.string is not None else ""
            b_bone.unknown_0x00 = bone.unknown_0x00
            b_bone.unknown_0x04 = bone.unknown_0x04
            b_bone.unknown_0x08 = bone.unknown_0x08
            b_bone.unknown_0x0C = bone.unknown_0x0C
            if bone.unknown_0x14 is not None:
                b_bone.nameless_data = bone.unknown_0x14
            
        for cldr in gfs_phys.colliders:
            # Create collider meshes
            # Remove this later...
            c = make_collider(cldr.has_name,
                             collider_types[cldr.collider_type],
                              cldr.capsule_height/2 if cldr.capsule_height is not None else 0.,
                              cldr.capsule_radius,
                              cldr.unknown_0x0A, # ibpm
                              cldr.name.string,  # bone name
                              bpy_obj) # armature
            c.hide_set(True)
            
            # Gonna keep this around though
            b_col = props.colliders.add()
            b_col.bone   = "" if cldr.name.string is None else cldr.name.string
            b_col.ibpm_0 = cldr.unknown_0x0A[0:4]
            b_col.ibpm_1 = cldr.unknown_0x0A[4:8]
            b_col.ibpm_2 = cldr.unknown_0x0A[8:12]
            b_col.ibpm_3 = cldr.unknown_0x0A[12:16]
            b_col.props.detached = cldr.has_name
            b_col.props.dtype  = collider_types[cldr.collider_type]
            b_col.props.radius = cldr.capsule_radius
            b_col.props.height = cldr.capsule_height/2 if cldr.capsule_height is not None else 0.
        
        for link in gfs_phys.physics_bone_links:
            b_link = props.links.add()
            b_link.parent = link.parent_physics_bone
            b_link.child  = link.child_physics_bone
            b_link.mass   = link.mass
            b_link.unknown_0x04 = link.unknown_0x04
            b_link.radius = link.radius if link.radius is not None else 0.

