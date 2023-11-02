import bpy
from ...FileFormats.GFS.SubComponents.CommonStructures.SceneNode.Mesh.MeshBinary import MeshBinary
from ..modelUtilsTest.Mesh.Managed import define_managed_mesh
from ..Utils.BoundingVolumes import update_box
from ..Utils.BoundingVolumes import update_sphere
from .BoundingVolumes import define_bounding_box
from .BoundingVolumes import define_bounding_sphere
from .Nodes import make_node_props_class
    

def get_box_props(context):
    return context.active_object.data.GFSTOOLS_MeshProperties.bounding_box.mesh


def calculate_box(context):
    bpy_mesh_object = context.active_object
    bpy_mesh = bpy_mesh_object.data
    boxprops = bpy_mesh.GFSTOOLS_MeshProperties.bounding_box
    boxprops.min_dims, boxprops.max_dims = calculate_mesh_box(bpy_mesh)


def calculate_mesh_box(bpy_mesh):
    class Vertex:
        __slots__ = ("position",)
        
        def __init__(self, p):
            self.position = p
    
    class MeshWrapper:
        def __init__(self, bpy_mesh):
            self.vertices = [Vertex(p.co) for p in bpy_mesh.vertices]
    
    mesh_wrapper = MeshWrapper(bpy_mesh)
    
    return MeshBinary.calc_bounding_box(mesh_wrapper)


def get_sphere_props(context):
    return context.active_object.data.GFSTOOLS_MeshProperties.bounding_sphere.mesh


def calculate_sphere(context):
    bpy_mesh_object = context.active_object
    bpy_mesh = bpy_mesh_object.data
    
    class Vertex:
        __slots__ = ("position",)
        
        def __init__(self, p):
            self.position = p
    
    class MeshWrapper:
        def __init__(self, bpy_mesh):
            self.vertices = [Vertex(p.co) for p in bpy_mesh.vertices]
            self.indices  = [v for p in bpy_mesh.polygons for v in p.vertices]
    
    mesh_wrapper = MeshWrapper(bpy_mesh)
    
    sphprops = bpy_mesh.GFSTOOLS_MeshProperties.bounding_sphere
    sphprops.center, sphprops.radius = MeshBinary.calc_bounding_sphere(mesh_wrapper)


MeshBoundingBox    = define_managed_mesh(lambda mesh: f".GFSTOOLS_{mesh.name}Box",    lambda mesh, ctx, obj: update_box   (mesh.GFSTOOLS_MeshProperties.bounding_box,    ctx, obj), get_box_props,    "gfstools.showmeshboundingbox"   , calculate_box,    "gfstools.calcmeshboundingbox"   )
MeshBoundingSphere = define_managed_mesh(lambda mesh: f".GFSTOOLS_{mesh.name}Sphere", lambda mesh, ctx, obj: update_sphere(mesh.GFSTOOLS_MeshProperties.bounding_sphere, ctx, obj), get_sphere_props, "gfstools.showmeshboundingsphere", calculate_sphere, "gfstools.calcmeshboundingsphere")
MeshBoundingBoxProps    = define_bounding_box   (MeshBoundingBox)
MeshBoundingSphereProps = define_bounding_sphere(MeshBoundingSphere)


GFSToolsMeshNodeProperties = make_node_props_class("GFSToolsMeshNodeProperties")


class GFSToolsMeshProperties(bpy.types.PropertyGroup):
    # Binary properties
    has_unknown_floats:  bpy.props.BoolProperty(name="Has Unknown Floats")
    
    permit_unrigged_export: bpy.props.BoolProperty(name="Permit Export as Unrigged", description="Allow the mesh to be exported as an unrigged mesh if all vertices are rigged to one or zero vertex groups. This will lower the rigged bone count by 1 if no other mesh is rigged to that bone, freeing up more of the 256 rigging slots for use elsewhere", default=True)
    
    unknown_0x12:    bpy.props.IntProperty(name="unknown 0x12")
    unknown_float_1: bpy.props.FloatProperty(name="Unknown Float 1")
    unknown_float_2: bpy.props.FloatProperty(name="Unknown Float 2")
    
    bounding_box:    bpy.props.PointerProperty(type=MeshBoundingBoxProps)
    bounding_sphere: bpy.props.PointerProperty(type=MeshBoundingSphereProps)
    
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
    is_dummy: bpy.props.BoolProperty(default=False)
    
    def is_mesh(self):
        return self.dtype == "MESH" and not self.is_dummy
    
    def is_collider(self):
        return self.dtype == "COLLIDER" and not self.is_dummy
