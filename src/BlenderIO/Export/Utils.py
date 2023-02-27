def find_obj_parent_bone(obj, armature):
    # Check for child of constraints
    child_of_constraints          = [c for c in obj.constraints               if c.type        == "CHILD_OF"]
    child_of_armature_constraints = [c for c in child_of_constraints          if c.target.type == "ARMATURE"]
    child_of_bone_constraints     = [c for c in child_of_armature_constraints if c.subtarget   != ""]
    if len(child_of_bone_constraints):
        constraint = child_of_bone_constraints[0]
        if constraint.target == armature:
            return constraint.subtarget
        
    # Check if it's a child of a bone in the armature
    if obj.parent == armature:
        if obj.parent_type == "BONE":
            return obj.parent_bone
    
    return None
    