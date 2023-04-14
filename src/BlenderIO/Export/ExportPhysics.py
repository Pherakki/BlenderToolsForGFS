import io

from ...serialization.BinaryTargets import Reader
from ...FileFormats.GFS.SubComponents.Physics.Binary.ContainerPayload import PhysicsPayload
from ...FileFormats.GFS.SubComponents.Physics.Binary.PhysicsBoneBinary import PhysicsBoneBinary
from ...FileFormats.GFS.SubComponents.Physics.Binary.ColliderBinary import ColliderBinary
from ...FileFormats.GFS.SubComponents.Physics.Binary.BoneLinkBinary import PhysicsBoneLinkBinary
from ..Utils.Maths import upY_to_upZ_matrix, boneY_to_boneX_matrix, colY_to_colX_matrix


def export_physics(gfs, bpy_obj, errorlog):
    props = bpy_obj.data.GFSTOOLS_ModelProperties.physics  
    if not props.has_physics:
        return

    bone_names = set([node.name for node in gfs.bones])
    physics = PhysicsPayload()

    # Export physics 
    physics.unknown_0x00 = props.unknown_0x00
    physics.unknown_0x04 = props.unknown_0x04
    physics.unknown_0x08 = props.unknown_0x08
    physics.unknown_0x0C = props.unknown_0x0C
    physics.unknown_0x10 = props.unknown_0x10
    
    # Export bone chains
    for b_bone in props.bones:
        bone = PhysicsBoneBinary()
        bone.has_name = b_bone.has_name
        bone.name = bone.name.from_name(b_bone.name)
        bone.unknown_0x00 = b_bone.unknown_0x00
        bone.unknown_0x04 = b_bone.unknown_0x04
        bone.unknown_0x08 = b_bone.unknown_0x08
        bone.unknown_0x0C = b_bone.unknown_0x0C
        bone.unknown_0x14 = b_bone.nameless_data
        physics.physics_bones.append(bone)
    physics.physics_bone_count = len(physics.physics_bones)
    
    for i, b_link in enumerate(props.links):
        link = PhysicsBoneLinkBinary()
        link.parent_physics_bone = b_link.parent
        link.child_physics_bone  = b_link.child
        link.mass                = b_link.mass
        link.unknown_0x04        = b_link.unknown_0x04
        link.radius              = b_link.radius
        physics.physics_bone_links.append(link)
        
        if link.parent_physics_bone == -1:
            errorlog.log_error_message(f"Armature '{bpy_obj.name}' has a parent bone index of -1 on physics link {i}. Either remove this link from the GFS Physics or set the index to a valid physics bone index")
        if link.child_physics_bone == -1:
            errorlog.log_error_message(f"Armature '{bpy_obj.name}' has a child bone index of -1 on physics link {i}. Either remove this link from the GFS Physics or set the index to a valid physics bone index")
        
        if link.parent_physics_bone >= physics.physics_bone_count:
            errorlog.log_warning_message(f"Armature '{bpy_obj.name}' has a parent bone index that exceeds the total number of physics bones ({physics.physics_bone_count}) on physics link {i}")
        if link.child_physics_bone >= physics.physics_bone_count:
            errorlog.log_warning_message(f"Armature '{bpy_obj.name}' has a child bone index that exceeds the total number of physics bones ({physics.physics_bone_count}) on physics link {i}")
    physics.physics_bone_link_count = len(physics.physics_bone_links)

    # Export colliders
    for obj in bpy_obj.children:
        if obj.type == "MESH":
            if obj.data.GFSTOOLS_MeshProperties.is_collider():
                col_props = obj.data.GFSTOOLS_ColliderProperties
                cldr = ColliderBinary()
                if obj.parent_type == "BONE" and obj.parent_bone != '':
                    has_name = True
                    bone_name = obj.parent_bone
                    parent_matrix = bpy_obj.matrix_world @ bpy_obj.data.bones[bone_name].matrix_local @ boneY_to_boneX_matrix.inverted()
                else:
                    has_name = not col_props.detached
                    bone_name = gfs.bones[0].name
                    parent_matrix = upY_to_upZ_matrix @ bpy_obj.matrix_world
                
                cldr.has_name = has_name
                cldr.name = cldr.name.from_name(bone_name)
                cldr.collider_type = 0 if col_props.dtype == "Sphere" else 1
                cldr.capsule_radius = col_props.radius*max(obj.scale)
                cldr.capsule_height = col_props.height*max(obj.scale)*2
                
                ibpm = (parent_matrix.inverted() @ obj.matrix_world @ colY_to_colX_matrix.inverted()).transposed()
                cldr.unknown_0x0A = [*ibpm[0], *ibpm[1], *ibpm[2], *ibpm[3]]
                
                physics.colliders.append(cldr)
    physics.collider_count = len(physics.colliders)

    # Remove physics bones for which the bone no longer exists
    for i, pbone in reversed(list(enumerate(physics.physics_bones))):
        if pbone.has_name:
            if pbone.name.string not in bone_names:
                errorlog.log_warning_message(f"Armature '{bpy_obj.name}' has bone physics attached to the non-existent bone '{pbone.name.string}'. This has not been exported")
                # OK to delete at index because we're traversing the list backwards
                del physics.physics_bones[i]
                physics.physics_bone_count -= 1
                for j, blink in reversed(list(enumerate(physics.physics_bone_links))):
                    if blink.parent_physics_bone == i or blink.child_physics_bone == i:
                        del physics.physics_bone_links[j]
                        physics.physics_bone_link_count -= 1
                        
                    if blink.parent_physics_bone >= i:
                        blink.parent_physics_bone -= 1
                    if blink.child_physics_bone >= i:
                        blink.child_physics_bone -= 1

    # Remove colliders for which the bone no longer exists
    for i, collider in reversed(list(enumerate(physics.colliders))):
        if collider.has_name:
            if collider.name.string not in bone_names:
                errorlog.log_warning_message(f"Armature '{bpy_obj.name}' has collider physics attached to the non-existent bone '{collider.name.string}'. This has not been exported")
                # OK to delete at index because we're traversing the list backwards
                del physics.colliders[i]
                physics.collider_count -= 1
                
    # If there's any physics to export, put it on the container
    if physics.physics_bone_count or physics.collider_count or physics.physics_bone_link_count:
        gfs.physics_data = physics
