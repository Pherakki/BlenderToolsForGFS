from ..modelUtilsTest.Mesh.Prebuilts import make_cuboid, make_capsule
from .PhysicsGen import get_col_material


def update_box(props, context, bpy_mesh_object):
    bpy_mesh = bpy_mesh_object.data
    
    dims = [mx - mn for mx, mn in zip(props.max_dims, props.min_dims)]
    ctr = [(mx + mn)/2 for mx, mn in zip(props.max_dims, props.min_dims)]
    bpy_mesh_object.location = ctr
    bpy_mesh_object.data.from_pydata(*make_cuboid(*dims, [1, 1, 1]))

    bpy_mesh.GFSTOOLS_MeshProperties.is_dummy = True
    bpy_mesh_object.active_material = get_col_material()

def update_sphere(props, context, bpy_mesh_object):
    bpy_mesh = bpy_mesh_object.data
    bpy_mesh_object.location = props.center
    r = props.radius
    bpy_mesh.from_pydata(*make_capsule(16, r, 0, [1, 1, 1]))
    bpy_mesh.use_auto_smooth = True
    for poly in bpy_mesh.polygons:
        poly.use_smooth = True
        
    bpy_mesh.GFSTOOLS_MeshProperties.is_dummy = True
    bpy_mesh_object.active_material = get_col_material()
