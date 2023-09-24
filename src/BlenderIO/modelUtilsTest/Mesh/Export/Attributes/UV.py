from .Utils import empty_attr, fetch_data, make_blank


def get_uvs(bpy_mesh_obj, use_uv, map_name, sigfigs, errorlog=None, transform=None):
    bpy_mesh = bpy_mesh_obj.data
    loops = bpy_mesh.loops
    nloops = len(loops)
    if use_uv:
        if map_name in bpy_mesh.uv_layers:
            data  = fetch_data(bpy_mesh.uv_layers[map_name].data, "uv", sigfigs)
            
            if transform is None: return data
            else:                 return [transform(d, l) for d, l in zip(data, loops)]
        else:
            if errorlog is not None:
                errorlog.log_warning_message(f"Unable to locate UV Map '{map_name}' on mesh '{bpy_mesh_obj.name}'; exporting a fallback blank map")
            return make_blank(nloops, 2)
    else:
        return empty_attr(nloops)
