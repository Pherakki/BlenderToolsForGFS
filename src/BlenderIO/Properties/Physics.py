import bpy
from ..Utils.PhysicsGen import rebuild_collider
from ..Utils.PhysicsGen import make_collider

def radius_getter(self):
    return self["radius"]


def radius_setter(self, value):
    self["radius"] = value
    rebuild_collider(self.id_data, self["radius"], self["height"], self.dtype == "Capsule")


def height_getter(self):
    return self["height"]


def height_setter(self, value):
    self["height"] = value
    rebuild_collider(self.id_data, self["radius"], self["height"], self.dtype == "Capsule")


def collider_update(self, context):
    rebuild_collider(self.id_data, self["radius"], self["height"], self.dtype == "Capsule")


collider_types = [("Sphere", "Sphere", "A sphere collider"), ("Capsule", "Capsule", "A capsule collider")]


class GFSToolsColliderProperties(bpy.types.PropertyGroup):
    detached: bpy.props.BoolProperty(name="Detached", description="Export the collider as 'detached' rather than attached to the root bone, if available", default=False)
    dtype: bpy.props.EnumProperty(items=collider_types, name="Type", default="Sphere", update=collider_update)
    radius: bpy.props.FloatProperty(name="Radius", default=1., get=radius_getter, set=radius_setter)
    height: bpy.props.FloatProperty(name="Height", default=0., get=height_getter, set=height_setter)


class GFSToolsBackendColliderProperties(bpy.types.PropertyGroup):
    detached: bpy.props.BoolProperty(name="Detached", default=False)
    bone:     bpy.props.StringProperty()
    dtype:    bpy.props.EnumProperty(items=collider_types, name="Type", default="Sphere")
    radius:   bpy.props.FloatProperty(name="Radius", default=1)
    height:   bpy.props.FloatProperty(name="Height", default=0.)
    ibpm_0:   bpy.props.FloatVectorProperty(size=4, default=(1., 0., 0., 0.))
    ibpm_1:   bpy.props.FloatVectorProperty(size=4, default=(0., 1., 0., 0.))
    ibpm_2:   bpy.props.FloatVectorProperty(size=4, default=(0., 0., 1., 0.))
    ibpm_3:   bpy.props.FloatVectorProperty(size=4, default=(0., 0., 0., 1.))
    
    def create_mesh(self, context):
        bpy_armature_object = context.active_object
        
        make_collider(self.detached,
                      self.dtype,
                      self.height/2,
                      self.radius,
                      [*self.ibpm_0, *self.ibpm_1, *self.ibpm_2, *self.ibpm_3],
                      self.bone,
                      bpy_armature_object)


class GFSToolsPhysicsBoneProperties(bpy.types.PropertyGroup):
    has_name: bpy.props.BoolProperty(name="Named", default=False)
    name:         bpy.props.StringProperty(name="Name", default="")
    nameless_data: bpy.props.FloatVectorProperty(name="Nameless Data", description="Unknown Nameless Data", size=6, default=(0., 0., 0., 0., 0., 0.))
    unknown_0x00: bpy.props.FloatProperty(name="Unknown 0x00", default=0)
    unknown_0x04: bpy.props.FloatProperty(name="Unknown 0x04", default=0)
    unknown_0x08: bpy.props.FloatProperty(name="Unknown 0x08", default=0)
    unknown_0x0C: bpy.props.FloatProperty(name="Unknown 0x0C", default=0)


class GFSToolsPhysicsLinkProperties(bpy.types.PropertyGroup):
    parent: bpy.props.IntProperty(name="Parent", min=-1, max=65535)
    child:  bpy.props.IntProperty(name="Child", min=-1, max=65535)
    
    mass: bpy.props.FloatProperty(name="Mass", default=0)
    unknown_0x04: bpy.props.FloatProperty(name="Unknown 0x04", default=0)
    radius: bpy.props.FloatProperty(name="Radius", default=0)


class GFSToolsPhysicsProperties(bpy.types.PropertyGroup):
    # Binary data
    has_physics:  bpy.props.BoolProperty(name="Has Physics", default=False)
    
    unknown_0x00: bpy.props.IntProperty(name="Unknown 0x00", default=0, subtype="UNSIGNED")
    unknown_0x04: bpy.props.FloatProperty(name="Unknown 0x04", default=0)
    unknown_0x08: bpy.props.FloatProperty(name="Unknown 0x08", default=0)
    unknown_0x0C: bpy.props.FloatProperty(name="Unknown 0x0C", default=0)
    unknown_0x10: bpy.props.FloatProperty(name="Unknown 0x10", default=0)
    
    active_bone_idx: bpy.props.IntProperty(options={'HIDDEN'}, default=0)
    active_link_idx: bpy.props.IntProperty(options={'HIDDEN'}, default=0)
    colliders:       bpy.props.CollectionProperty(type=GFSToolsBackendColliderProperties, name="Colliders")
    bones:           bpy.props.CollectionProperty(type=GFSToolsPhysicsBoneProperties,     name="Bones")
    links:           bpy.props.CollectionProperty(type=GFSToolsPhysicsLinkProperties,     name="Bone Links")

    # Helper data
    collider_editing_active:  bpy.props.BoolProperty(options={'HIDDEN'}, default=False)
    attach_colliders_to_bone: bpy.props.BoolProperty(name="Attach to Bone", default=False)
    active_bone: bpy.props.StringProperty(name="Bone")
