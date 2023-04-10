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


def available_versions_property():
    return bpy.props.EnumProperty(items=(
            ("0x01104920", "0x01104920", ""),
            ("0x01104950", "0x01104950", ""),
            ("0x01105000", "0x01105000", ""),
            ("0x01105010", "0x01105010", ""),
            ("0x01105020", "0x01105020", ""),
            ("0x01105030", "0x01105030", ""),
            ("0x01105040", "0x01105040", ""),
            ("0x01105050", "0x01105050", ""),
            ("0x01105060", "0x01105060", ""),
            ("0x01105070", "0x01105070", ""),
            ("0x01105080", "0x01105080", ""),
            ("0x01105090", "0x01105090", ""),
            ("0x01105100", "0x01105100", "")
        ),
        name="Version",
        default="0x01105100"
    )

def bone_pose_enum_options():
    return [
        ("bindpose", "Reconstruct",         "Reconstruct the bind pose"),
        ("restpose", "Scaleless Rest Pose", "Define the bind pose as the rest pose, without scales. As a side-effect, this bakes the mesh transforms into the vertices"),    
    ]

def too_many_vertices_policy_options():
    return [
            ('IGNORE', 'Ignore',      ''),
            ('WARN',   'Warn',        ''),
            ("ERROR",  'Throw Error', '')
    ]
