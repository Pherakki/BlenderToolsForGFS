import bpy
from .Nodes import make_node_props_class


GFSToolsMeshNodeProperties = make_node_props_class("GFSToolsMeshNodeProperties")


class GFSToolsMeshProperties(bpy.types.PropertyGroup):
    # Binary properties
    has_unknown_floats:  bpy.props.BoolProperty(name="Active")
    
    permit_unrigged_export: bpy.props.BoolProperty(name="Permit Export as Unrigged", description="Allow the mesh to be exported as a bone child if all vertices are rigged to a single vertex group. This will lower the rigged bone count by 1 if no other mesh is rigged to that bone, freeing up more of the 256 rigging slots for use elsewhere. This may cause errors if the mesh node loads animation data", default=False)
    
    unknown_0x12:    bpy.props.IntProperty(name="unknown 0x12")
    unknown_float_1: bpy.props.FloatProperty(name="unknown 1")
    unknown_float_2: bpy.props.FloatProperty(name="unknown 2")
    
    export_bounding_box:    bpy.props.BoolProperty(name="Export Bounding Box",    default=True)
    export_bounding_sphere: bpy.props.BoolProperty(name="Export Bounding Sphere", default=True)
    
    flag_5:  bpy.props.BoolProperty(name="Unknown Flag 5", default=False)
    flag_7:  bpy.props.BoolProperty(name="Unknown Flag 7", default=True)
    flag_8:  bpy.props.BoolProperty(name="Unknown Flag 8", default=False)
    flag_9:  bpy.props.BoolProperty(name="Unknown Flag 9", default=False)
    flag_10: bpy.props.BoolProperty(name="Unknown Flag 10", default=False)
    flag_11: bpy.props.BoolProperty(name="Unknown Flag 11", default=False)
    flag_13: bpy.props.BoolProperty(name="Unknown Flag 13", default=False)
    flag_14: bpy.props.BoolProperty(name="Unknown Flag 14", default=False)
    flag_15: bpy.props.BoolProperty(name="Unknown Flag 15", default=False)
    flag_16: bpy.props.BoolProperty(name="Unknown Flag 16", default=False)
    flag_17: bpy.props.BoolProperty(name="Unknown Flag 17", default=False)
    flag_18: bpy.props.BoolProperty(name="Unknown Flag 18", default=False)
    flag_19: bpy.props.BoolProperty(name="Unknown Flag 19", default=False)
    flag_20: bpy.props.BoolProperty(name="Unknown Flag 20", default=False)
    flag_21: bpy.props.BoolProperty(name="Unknown Flag 21", default=False)
    flag_22: bpy.props.BoolProperty(name="Unknown Flag 22", default=False)
    flag_23: bpy.props.BoolProperty(name="Unknown Flag 23", default=False)
    flag_24: bpy.props.BoolProperty(name="Unknown Flag 24", default=False)
    flag_25: bpy.props.BoolProperty(name="Unknown Flag 25", default=False)
    flag_26: bpy.props.BoolProperty(name="Unknown Flag 26", default=False)
    flag_27: bpy.props.BoolProperty(name="Unknown Flag 27", default=False)
    flag_28: bpy.props.BoolProperty(name="Unknown Flag 28", default=False)
    flag_29: bpy.props.BoolProperty(name="Unknown Flag 29", default=False)
    flag_30: bpy.props.BoolProperty(name="Unknown Flag 30", default=False)
    flag_31: bpy.props.BoolProperty(name="Unknown Flag 31", default=True)
    
    # Helper properties for Blender I/O
    dtype: bpy.props.EnumProperty(items=[("MESH", "Mesh", ""),
                                         ("COLLIDER", "Collider", "")],
                                  default="MESH")
    
    def is_mesh(self):
        return self.dtype == "MESH"
    
    def is_collider(self):
        return self.dtype == "COLLIDER"
