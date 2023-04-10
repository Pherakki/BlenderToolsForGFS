import bpy


class GFSToolsPhysicsBoneProperties(bpy.types.PropertyGroup):
    has_name: bpy.props.BoolProperty(name="Named", default=False)
    name:         bpy.props.StringProperty(name="Name", default="")
    nameless_data: bpy.props.FloatVectorProperty(name="Nameless Data", description="Unknown Nameless Data", size=6, default=(0., 0., 0., 0., 0., 0.))
    unknown_0x00: bpy.props.FloatProperty(name="Unknown 0x00", default=0)
    unknown_0x04: bpy.props.FloatProperty(name="Unknown 0x04", default=0)
    unknown_0x08: bpy.props.FloatProperty(name="Unknown 0x08", default=0)
    unknown_0x0C: bpy.props.FloatProperty(name="Unknown 0x0C", default=0)
    
    
class GFSToolsPhysicsColliderProperties(bpy.types.PropertyGroup):
    dtype: bpy.props.EnumProperty(items=[("Sphere", "Sphere", "Named Collider"), ("Capsule", "Capsule", "Unnamed Collider")], name="Type", default="Sphere")
    
    has_name: bpy.props.BoolProperty(name="Named", default=False)
    name:   bpy.props.StringProperty(name="Name", default="")
    radius: bpy.props.FloatProperty(name="Radius", default=1.)
    height: bpy.props.FloatProperty(name="Height", default=1.)
    r1: bpy.props.FloatVectorProperty(name="", size=4, default=(1., 0., 0., 0.))
    r2: bpy.props.FloatVectorProperty(name="", size=4, default=(0., 1., 0., 0.))
    r3: bpy.props.FloatVectorProperty(name="", size=4, default=(0., 0., 1., 0.))
    r4: bpy.props.FloatVectorProperty(name="", size=4, default=(0., 0., 0., 1.))

class GFSToolsPhysicsLinkProperties(bpy.types.PropertyGroup):
    parent: bpy.props.IntProperty(name="Parent", min=-1, max=65535)
    child:  bpy.props.IntProperty(name="Child", min=-1, max=65535)
    
    mass: bpy.props.FloatProperty(name="Mass", default=0)
    unknown_0x04: bpy.props.FloatProperty(name="Unknown 0x04", default=0)
    radius: bpy.props.FloatProperty(name="Radius", default=0)


class GFSToolsPhysicsProperties(bpy.types.PropertyGroup):
    has_physics:  bpy.props.BoolProperty(name="Has Physics", default=False)
    
    unknown_0x00: bpy.props.IntProperty(name="Unknown 0x00", default=0, subtype="UNSIGNED")
    unknown_0x04: bpy.props.FloatProperty(name="Unknown 0x04", default=0)
    unknown_0x08: bpy.props.FloatProperty(name="Unknown 0x08", default=0)
    unknown_0x0C: bpy.props.FloatProperty(name="Unknown 0x0C", default=0)
    unknown_0x10: bpy.props.FloatProperty(name="Unknown 0x10", default=0)
    
    
    active_bone_idx: bpy.props.IntProperty(options={'HIDDEN'}, default=0)
    active_cldr_idx: bpy.props.IntProperty(options={'HIDDEN'}, default=0)
    active_link_idx: bpy.props.IntProperty(options={'HIDDEN'}, default=0)
    bones:           bpy.props.CollectionProperty(type=GFSToolsPhysicsBoneProperties,     name="Bones")
    colliders:       bpy.props.CollectionProperty(type=GFSToolsPhysicsColliderProperties, name="Colliders")
    links:           bpy.props.CollectionProperty(type=GFSToolsPhysicsLinkProperties,     name="Bone Links")
