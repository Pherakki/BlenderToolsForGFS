import bpy


icon_lookup = {
    icon.identifier : icon.value 
    for (name, icon) 
    in bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.items()
}
