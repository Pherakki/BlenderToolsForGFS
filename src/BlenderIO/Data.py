import os

import bpy

dummy_image_data = \
b'DDS |\x00\x00\x00\x07\x10\x00\x00\x08\x00\x00\x00'\
b'\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00'\
b'\x04\x00\x00\x00DXT5\x00\x00\x00\x00\x00\x00\x00\x00'\
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00'\
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
b'\x00\x05\xff\xff\xff\xff\xff\xffx\xfd\x89%\x05\x05PP'\
b'\x00\x05\xff\xff\xff\xff\xff\xffx\xfd\x89%\x05\x05PP'\
b'\x00\x05\xff\xff\xff\xff\xff\xffx\xfd\x89%\x05\x05PP'\
b'\x00\x05\xff\xff\xff\xff\xff\xffx\xfd\x89%\x05\x05PP'


def get_root_path():
    current_path = os.path.realpath(__file__)
    path = os.path.join(current_path, 
                             os.path.pardir,
                             os.path.pardir,
                             os.path.pardir)
    return os.path.realpath(path)


def get_package_name():
    return os.path.basename(get_root_path())


def version_override_options():
    return [
        ("DEFAULT", "Default", "Use the version specin the Custom Properties of the exported data"),
        ("P5R",     "P5R",     "Export to a version compatible with Persona 5 Royal (0x01105100)"),
        ("CUSTOM",  "Custom",  "Use a custom version number")
    ]


def bone_pose_enum_options():
    return [
        ("bindpose", "Reconstruct",         "Reconstruct the bind pose"),
        ("restpose", "Scaleless Rest Pose", "Define the bind pose as the rest pose, without scales. As a side-effect, this bakes the mesh transforms into the vertices"),    
    ]

def anim_boundbox_policy_options():
    return [
        ("MANUAL", "Original", "Import all animation bounding boxes with their export policy set to 'Manual'. This can be changed for each animation inside Blender. Animations will be exported with fixed bounding boxes set within Blender, which are initially set to the imported bounding box. This means that if you need to change a bounding box, you must do it manually in the properties for that animation, and the box will not automatically update to reflect changes to the animation. However, this guarantees that bounding boxes will not be modified when you re-export the model unless you explicitly edit them yourself"),
        ("AUTO",   "Auto",     "Import all animation bounding boxes with their export policy set to 'Auto'. This can be changed for each animation inside Blender. Animations will exported with automatically-calculated bounding boxes. The automatically calculated bounding boxes will not exactly match the vanilla bounding boxes, but will be more accurate")
    ]

def too_many_vertices_policy_options():
    return [
            ('IGNORE', 'Ignore',      ''),
            ('WARN',   'Warn',        ''),
            ("ERROR",  'Throw Error', '')
    ]

def too_many_vertex_groups_policy_options():
    return [
            ('WARN',   'Warn',        'Issue a warning if there are vertices with more than 4 vertex groups, and automatically strip the least influential groups'),
            ("ERROR",  'Throw Error', 'Throw an error and show the vertices which have more than 4 vertex groups')
    ]

def multiple_materials_policy_options():
    return [
            ('WARN',                  'Warn',                      'Issue a warning if a mesh contains more than one material. The material with the most faces using it will be exported'),
            ("ERROR",                 'Throw Error',               'Prevent export if a mesh contains more than one material'),
            ('AUTOSPLIT_DESTRUCTIVE', 'Auto-Split (Destructive)',  'Automatically split the Blender mesh into submeshes before export, where each submesh has a single material')
    ]

def missing_uv_maps_policy_options():
    return [
            ('WARN',      'Warn',        'Issue a warning if a mesh has missing UV maps, and replace them with blank maps'),
            ("ERROR",     'Throw Error', 'Prevent export if a mesh has missing UV maps')
    ]

def triangulate_mesh_policy_options():
    return [
            ("ERROR",                   'Throw Error',               'Prevent export if a mesh has non-triangular faces'),
            ("TRIANGULATE_DESTRUCTIVE", "Triangulate (Destructive)", "Triangulate Blender meshes before export")
    ]
