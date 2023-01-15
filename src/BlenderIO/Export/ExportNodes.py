import bpy


def export_node_tree(gfs, armature):
    # This is wrong, this just gets the bind pose...
    # Needs to get the rest pose, but that requires the rest pose import
    # to be settled first
    
    bone_list = {bone.name: i for i, bone in enumerate(armature.data.bones)}

    for bone in armature.data.bones:
        bone_parent = bone.parent
        bone_matrix = bone.matrix_local
        if bone_parent is None:
            parent_id = -1
            position, rotation, scale = bone_matrix.decompose()
        else:
            parent_id = bone_list[bone_parent.name]
            position, rotation, scale = (bone_parent.matrix_local.inverted() @ bone_matrix).decompose()

        bpm = [
            bone_matrix[0][0], bone_matrix[0][1], bone_matrix[0][2], bone_matrix[0][3],
            bone_matrix[1][0], bone_matrix[1][1], bone_matrix[1][2], bone_matrix[1][3],
            bone_matrix[2][0], bone_matrix[2][1], bone_matrix[2][2], bone_matrix[2][3],
        ]
        gfs.add_node(parent_id, bone.name, position, rotation, scale, 1.0, bpm, [])
        
    return bone_list
