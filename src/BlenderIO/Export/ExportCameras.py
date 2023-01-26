import math

import bpy
from mathutils import Matrix, Quaternion

from ..Utils.Maths import convert_rotation_to_quaternion


def export_cameras(gfs, armature):
    bpy_cams = [obj for obj in armature.children if obj.type == "CAMERA"]
    
    for bpy_camera_object in bpy_cams:
        if bpy_camera_object.parent_type != "BONE":
            continue
        
        node_idx = armature.data.bones.index(bpy_camera_object.parent_bone.name)
        props = bpy_camera_object.GFSTOOLS_CameraProperties
        
        if bpy_camera_object.lens_unit != "FOV":
            raise NotImplementedError("Cameras must currently be exported with FOV units")
        
        gfs.add_camera(node_idx, 
                       [elem for row in bpy_camera_object.matrix_local for elem in row],
                       bpy_camera_object.clip_start,
                       bpy_camera_object.clip_end,
                       bpy_camera_object.lens,
                       bpy_camera_object.get("aspect_ratio", 1.),
                       bpy_camera_object.get("unknown_0x50", 0))
        
