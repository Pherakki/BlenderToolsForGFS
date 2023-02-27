def lock_obj_transforms(obj):
    obj.lock_location[0] = True
    obj.lock_location[1] = True
    obj.lock_location[2] = True
    
    obj.lock_rotation[0] = True
    obj.lock_rotation[1] = True
    obj.lock_rotation[2] = True
    obj.lock_rotation_w  = True
    
    obj.lock_scale[0]    = True
    obj.lock_scale[1]    = True
    obj.lock_scale[2]    = True
