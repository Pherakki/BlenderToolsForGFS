import math

import bpy
from mathutils import Matrix, Quaternion

from ..Utils.Maths import convert_rotation_to_quaternion


def export_lights(gfs, armature):
    bpy_lights = [obj for obj in armature.children if obj.type == "LIGHT"]
    
    for bpy_light in bpy_lights:
        if bpy_light.parent_type != "BONE":
            continue
        
        node_idx = armature.data.bones.index(bpy_light.parent_bone.name)
        props = bpy_light.GFSTOOLS_LightProperties
        
        if props.dtype == "TYPE1":
            type_id = 1
        elif props.dtype == "SPHERE":
            type_id = 2
        elif props.dtype == "HEMISPHERE":
            type_id = 3
        else:
            raise NotImplementedError("Internal error: did not recognise light type '{props.type}'")
        light = gfs.add_light(node_idx, type_id, props.color_1, list(bpy_light.color), props.color_3)
        
        light.unknown_0x28 = props.unknown_0x28
        light.unknown_0x2C = props.unknown_0x2C
        light.unknown_0x30 = props.unknown_0x30
        light.unknown_0x34 = props.unknown_0x34
        light.unknown_0x38 = props.unknown_0x38
        light.unknown_0x3C = props.unknown_0x3C
        light.inner_radius = props.inner_radius
        light.outer_radius = props.outer_radius
        light.unknown_0x48 = props.unknown_0x48
        light.unknown_0x4C = props.unknown_0x4C
        light.unknown_0x50 = props.unknown_0x50
        light.unknown_0x54 = props.unknown_0x54
        light.unknown_0x58 = props.unknown_0x58
        light.unknown_0x5C = props.unknown_0x5C
        light.unknown_0x60 = props.unknown_0x60
        light.unknown_0x64 = props.unknown_0x64
        light.unknown_0x68 = props.unknown_0x68
        light.unknown_0x6C = props.unknown_0x6C
        light.unknown_0x70 = props.unknown_0x70
        light.unknown_0x74 = props.unknown_0x74
        light.unknown_0x78 = props.unknown_0x78
        light.unknown_0x7C = props.unknown_0x7C
        light.unknown_0x80 = props.unknown_0x80
        light.unknown_0x84 = props.unknown_0x84
        
        light.flags.flag_0  = props.flag_0
        light.flags.unk_setting = props.unk_setting
        light.flags.flag_2  = props.flag_2
        light.flags.flag_3  = props.flag_3
        light.flags.flag_4  = props.flag_4
        light.flags.flag_5  = props.flag_5
        light.flags.flag_6  = props.flag_6
        light.flags.flag_7  = props.flag_7
        light.flags.flag_8  = props.flag_8
        light.flags.flag_9  = props.flag_9
        light.flags.flag_10 = props.flag_10
        light.flags.flag_11 = props.flag_11
        light.flags.flag_12 = props.flag_12
        light.flags.flag_13 = props.flag_13
        light.flags.flag_14 = props.flag_14
        light.flags.flag_15 = props.flag_15
        light.flags.flag_16 = props.flag_16
        light.flags.flag_17 = props.flag_17
        light.flags.flag_18 = props.flag_18
        light.flags.flag_19 = props.flag_19
        light.flags.flag_20 = props.flag_20
        light.flags.flag_21 = props.flag_21
        light.flags.flag_22 = props.flag_22
        light.flags.flag_23 = props.flag_23
        light.flags.flag_24 = props.flag_24
        light.flags.flag_25 = props.flag_25
        light.flags.flag_26 = props.flag_26
        light.flags.flag_27 = props.flag_27
        light.flags.flag_28 = props.flag_28
        light.flags.flag_29 = props.flag_29
        light.flags.flag_30 = props.flag_30
        light.flags.flag_31 = props.flag_31
        