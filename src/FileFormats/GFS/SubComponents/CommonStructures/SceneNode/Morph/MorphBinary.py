from ....CommonStructures import ObjectName


class MorphBinary:
    def __init__(self):
        self.target_count = 0
        self.targets = []
        self.parent_name = ObjectName()
                   
    def __repr__(self):
        return f"[GFSBinary::Scene::Node::Morph] '{self.parent_name.string}', {self.target_count} targets"
            
    def exbip_rw(self, rw, version):
        self.target_count = rw.rw_uint32(self.target_count)
        self.targets      = rw.rw_uint32s(self.targets, self.target_count)
        rw.rw_obj(self.parent_name, version)
