import math

import bpy
from mathutils import Matrix, Quaternion

from ..Utils.Maths import convert_YDirBone_to_XDirBone, convert_Zup_to_Yup, BlenderBoneToMayaBone
from ..Utils.RestPose import get_rest_pose

def export_node_tree(gfs, bpy_armature_object, errorlog):
    bind_pose_matrices = []
    # Export the bounding box/sphere flags when doing the meshes
    gfs.flag_3 = bpy_armature_object.data.GFSTOOLS_ModelProperties.flag_3
    
    # Get the rest pose if it exists
    rest_pose_matrices, armature_rest_pose = get_rest_pose(bpy_armature_object)
    
    # Add root node
    rn_props = bpy_armature_object.data.GFSTOOLS_NodeProperties
    t, r, s = armature_rest_pose.decompose()
    bm = Matrix.Translation(t) @ r.to_matrix().to_4x4()
    root_node = gfs.add_node(-1, bpy_armature_object.data.GFSTOOLS_ModelProperties.root_node_name,
                              [t.x, t.y, t.z], [r.x, r.y, r.z, r.w],  [s.x, s.y, s.z], 
                              rn_props.unknown_float,
                              [
                                  bm[0][0], bm[0][1], bm[0][2], bm[0][3],
                                  bm[1][0], bm[1][1], bm[1][2], bm[1][3],
                                  bm[2][0], bm[2][1], bm[2][2], bm[2][3],
                              ])
    for prop in rn_props.properties:
        root_node.add_property(*prop.extract_data(prop))
    
    bind_pose_matrices.append(bm)
    bone_list = {bone.name: i for i, bone in enumerate([root_node, *bpy_armature_object.data.bones])}
    # Export each bone as a node
    for bone in bpy_armature_object.data.bones:
        # Reconstruct the rest pose transform
        bone_parent = bone.parent
        bind_matrix = bone.matrix_local
        if bone_parent is None:
            parent_id = 0
            local_bind_matrix = convert_Zup_to_Yup(bind_matrix)
        else:
            parent_id = bone_list[bone_parent.name]
            local_bind_matrix = (convert_YDirBone_to_XDirBone(bone_parent.matrix_local)).inverted() @ bind_matrix
        
        bind_relative_pose = rest_pose_matrices[bone.name]
        parent_relative_pose = local_bind_matrix @ convert_YDirBone_to_XDirBone(bind_relative_pose)
        p, r, s = parent_relative_pose.decompose()
        position = [p.x, p.y, p.z]
        rotation = [r.x, r.y, r.z, r.w]
        scale    = [s.x, s.y, s.z]
        
        bm = BlenderBoneToMayaBone(bind_matrix)
        export_bm = [
            bm[0][0], bm[0][1], bm[0][2], bm[0][3],
            bm[1][0], bm[1][1], bm[1][2], bm[1][3],
            bm[2][0], bm[2][1], bm[2][2], bm[2][3],
        ]
        
        # Export the node object
        unknown_float = bone.GFSTOOLS_NodeProperties.unknown_float
        node = gfs.add_node(parent_id, bone.name, position, rotation, scale, unknown_float, export_bm)
        
        # Export the custom properties
        for prop in bone.GFSTOOLS_NodeProperties.properties:
            node.add_property(*prop.extract_data(prop))
            
        bind_pose_matrices.append(bm)
    return bone_list, bind_pose_matrices
