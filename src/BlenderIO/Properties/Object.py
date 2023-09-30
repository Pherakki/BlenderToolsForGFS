import bpy


def get_armature(bpy_mesh_object):
    if bpy_mesh_object.parent is None:
        return
    if bpy_mesh_object.parent.type != "ARMATURE":
        return
    return bpy_mesh_object.parent

    # for modifier in bpy_mesh_object.modifiers:
    #     if modifier.type == "ARMATURE":
    #         if modifier.object == bpy_mesh_object.parent:
    #             return modifier.object

def get_label(self):
    return self.mesh_rig_type()

def poll_merged_node(self, bpy_object):
    return bpy_object.type == "MESH"


class GFSToolsObjectProperties(bpy.types.PropertyGroup):    
    ############
    # ARMATURE #
    ############
    def is_armature(self):
        return self.id_data.type == "ARMATURE"
    
    def is_model(self):
        return self.is_armature()
    
    def is_epl(self):
        return False
    
    def get_model_meshes(self):
        if not self.is_model():
            raise ValueError("Is not a GFS Model")
            
        meshes = []
        for c in self.id_data.children:
            if not c.GFSTOOLS_ObjectProperties.is_mesh():
                continue
            if not c.data.GFSTOOLS_MeshProperties.is_mesh():
                continue
            meshes.append(c)
        return meshes
            
    ########
    # MESH #
    ########
    attach_mode_label: bpy.props.StringProperty(name="State", get=get_label)
    attach_mode: bpy.props.EnumProperty(items=[("NODE", "Node", "Attach to the specified node"),
                                               ("MESH", "Mesh", "Attach to the same node as another mesh")],
                                        name="Attach Mode",
                                        default="NODE")
    
    node:       bpy.props.StringProperty(name="Node", description="Attach to this node on export")
    merge_node: bpy.props.PointerProperty(type=bpy.types.Object, name="Merge Node", description="Attach to the node of the selected mesh on export", poll=poll_merged_node)
    
    UNRIGGED_ATTACHED       = "Unrigged [Attached]"
    UNRIGGED_NEW_NODE       = "Unrigged [New Node]"
    UNRIGGED_AMBIGUOUS      = "Unrigged [Ambiguous]"
    RIGGED_NEW_NODE         = "Rigged [New Node]"
    RIGGED_NEW_NODE_INVALID = "Rigged [New Node - Invalid Bone]"
    RIGGED_ATTACHED         = "Rigged [Attached]"
    RIGGED_MERGED           = "Rigged [Merged]"
    
    def is_mesh(self):
        return self.id_data.type == "MESH"
    
    # TODO: These functions are quite sloppy.
    # Need a less fragile way to do this rather than strings...
    def is_valid_mesh(self):
        if self.id_data.parent is None:
            return False
        if self.id_data.parent.type != "ARMATURE":
            return False
        # if get_armature(self.id_data) is None:
        #     return False
        if self.id_data.data is None:
            return False
        if not self.is_mesh():
            return False
        return True
    
    def get_armature(self):
        if not self.is_valid_mesh():
            return None
        return self.id_data.parent
    
    def is_rigged(self):
        return not self.is_unrigged()
    
    def is_unrigged(self):
        bpy_mesh_object = self.id_data
        return (len(bpy_mesh_object.vertex_groups) <= 1) and bpy_mesh_object.data.GFSTOOLS_MeshProperties.permit_unrigged_export
    
    def get_unrigged_type(self):
        if len(self.id_data.vertex_groups) == 1:
            return self.UNRIGGED_ATTACHED
        elif len(self.id_data.vertex_groups) == 0:
            return self.UNRIGGED_NEW_NODE
        else:
            return self.UNRIGGED_AMBIGUOUS
    
    def get_rigged_type(self):
        if self.attach_mode == "NODE":
            if self.node == "":
                return self.RIGGED_NEW_NODE
            elif self.node not in get_armature(self.id_data).data.bones:
                return self.RIGGED_NEW_NODE_INVALID
            else:
                return self.RIGGED_ATTACHED
        elif self.attach_mode == "MESH":
            if self.merged_node is None:
                return self.RIGGED_NEW_NODE
            else:
                return self.RIGGED_MERGED
        else:
            raise NotImplementedError("CRITICAL INTERNAL ERROR: COULD NOT DETERMINE RIGGED MESH TYPE")

    def mesh_rig_type(self):
        if not self.is_valid_mesh():
            return "Invalid"
        
        if self.is_rigged():
            return self.get_rigged_type()
        else:
            return self.get_unrigged_type()
        
    def requires_new_node(self):
        if self.is_rigged():
            return self.get_rigged_type() in (self.RIGGED_NEW_NODE, self.RIGGED_NEW_NODE_INVALID)
        else:
            return self.get_unrigged_type() in (self.UNRIGGED_NEW_NODE,)

    def get_node_name(self):
        if self.is_rigged():
            rig_type = self.get_rigged_type()
            if rig_type == self.RIGGED_ATTACHED:
                return self.node
            elif rig_type == self.RIGGED_NEW_NODE:
                raise Exception("CALLED get_node_name IN INVALID CONTEXT: RIGGED REQUIRES NEW NODE")
            elif rig_type == self.RIGGED_NEW_NODE_INVALID:
                raise Exception("CALLED get_node_name IN INVALID CONTEXT: RIGGED INVALID BONE")
            else:
                raise NotImplementedError(f"CRITICAL INTERNAL ERROR: UNIMPLEMENTED RIG TYPE '{rig_type}'")
        else:
            rig_type = self.get_unrigged_type()
            if rig_type == self.UNRIGGED_ATTACHED:
                return self.id_data.vertex_groups[0].name
            elif rig_type == self.UNRIGGED_NEW_NODE:
                return Exception("CALLED get_node_name IN INVALID CONTEXT: UNRIGGED REQUIRES NEW NODE")
            elif rig_type == self.UNRIGGED_AMBIGUOUS:
                return Exception("CALLED get_node_name IN INVALID CONTEXT: UNRIGGED AMBIGIOUS")
            else:
                raise NotImplementedError(f"CRITICAL INTERNAL ERROR: UNIMPLEMENTED RIG TYPE '{rig_type}'")
