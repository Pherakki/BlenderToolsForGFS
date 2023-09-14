import bpy
from .Nodes import make_node_props_class
from .Physics import GFSToolsPhysicsProperties
from ..modelUtilsTest.Mesh.Managed import define_managed_mesh
from ..modelUtilsTest.Mesh.Prebuilts import make_cuboid, make_capsule
from ..Utils.PhysicsGen import get_col_material


# Should be able to unify create_mesh and update_mesh
def update_box(bpy_armature, context, bpy_mesh_object):
    props = bpy_armature.GFSTOOLS_ModelProperties
    bpy_mesh = bpy_mesh_object.data
    
    dims = [mx - mn for mx, mn in zip(props.bounding_box_max, props.bounding_box_min)]
    ctr = [(mx + mn)/2 for mx, mn in zip(props.bounding_box_max, props.bounding_box_min)]
    bpy_mesh_object.location = ctr
    bpy_mesh_object.data.from_pydata(*make_cuboid(*dims, [1, 1, 1]))

    bpy_mesh.GFSTOOLS_MeshProperties.is_dummy = True
    bpy_mesh_object.active_material = get_col_material()
    
def get_box_props(context):
    return context.active_object.data.GFSTOOLS_ModelProperties.bounding_box_mesh

def update_sphere(bpy_armature, context, bpy_mesh_object):
    props = bpy_armature.GFSTOOLS_ModelProperties
    bpy_mesh = bpy_mesh_object.data
    bpy_mesh_object.location = props.bounding_sphere_centre
    r = props.bounding_sphere_radius
    bpy_mesh.from_pydata(*make_capsule(16, r, 0, [1, 1, 1]))
    bpy_mesh.use_auto_smooth = True
    for poly in bpy_mesh.polygons:
        poly.use_smooth = True
        
    bpy_mesh.GFSTOOLS_MeshProperties.is_dummy = True
    bpy_mesh_object.active_material = get_col_material()

def get_sphere_props(context):
    return context.active_object.data.GFSTOOLS_ModelProperties.bounding_sphere_mesh

ModelBoundingBox    = define_managed_mesh(lambda arm: f".GFSTOOLS_{arm.name}Box",    update_box,    get_box_props,    "gfstools.showmodelboundingbox"   )
ModelBoundingSphere = define_managed_mesh(lambda arm: f".GFSTOOLS_{arm.name}Sphere", update_sphere, get_sphere_props, "gfstools.showmodelboundingsphere")

GFSToolsModelNodeProperties = make_node_props_class("GFSToolsModelNodeProperties")


class GFSToolsModelProperties(bpy.types.PropertyGroup):
    # Bounding box
    export_bounding_box: bpy.props.EnumProperty(items=[("NONE",   "None",   "Do not export a bounding box"),
                                                       ("MANUAL", "Manual", "Manually create bounding box"),
                                                       ("AUTO",   "Auto",   "Auto-calculate a bounding box on export")],
                                                name="Bounding Box", default="AUTO")
    bounding_box_mesh: bpy.props.PointerProperty(type=ModelBoundingBox)
    bounding_box_min:  bpy.props.FloatVectorProperty(name="Bounding Box Min", 
                                                     size=3,
                                                     default=(0, 0, 0),
                                                     update=lambda self, ctx: ModelBoundingBox.update(self, ctx, self.bounding_box_mesh))
    bounding_box_max:  bpy.props.FloatVectorProperty(name="Bounding Box Max",
                                                     size=3, 
                                                     default=(0, 0, 0),
                                                     update=lambda self, ctx: ModelBoundingBox.update(self, ctx, self.bounding_box_mesh))
    
    # Bounding sphere
    export_bounding_sphere: bpy.props.EnumProperty(items=[("NONE",   "None",   "Do not export a bounding box"),
                                                          ("MANUAL", "Manual", "Manually create bounding box"),
                                                          ("AUTO",   "Auto",   "Auto-calculate a bounding box on export")],
                                                   name="Bounding Sphere", default="AUTO")
    bounding_sphere_mesh:   bpy.props.PointerProperty(type=ModelBoundingSphere)
    bounding_sphere_centre: bpy.props.FloatVectorProperty(name="Bounding Sphere Centre", 
                                                          size=3,
                                                          default=(0, 0, 0),
                                                          update=lambda self, ctx: ModelBoundingSphere.update(self, ctx, self.bounding_sphere_mesh))
    bounding_sphere_radius: bpy.props.FloatProperty(name="Bounding Sphere Radius",
                                                    default=0,
                                                    update=lambda self, ctx: ModelBoundingSphere.update(self, ctx, self.bounding_sphere_mesh))
    
    # Remaining stuff
    flag_3:           bpy.props.BoolProperty(name="Unknown Flag 3", default=False) 
    root_node_name:   bpy.props.StringProperty(name="Root Node Name", default="RootNode")
    has_external_emt: bpy.props.BoolProperty(name="External EMT", default=False)    
    physics:          bpy.props.PointerProperty(name="Physics", type=GFSToolsPhysicsProperties)
    physics_blob:     bpy.props.StringProperty(name="SECRET PHYSICS BLOB - DO NOT TOUCH", default='', options={'HIDDEN'})
