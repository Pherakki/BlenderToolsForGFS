from .......serialization.formatters import list_formatter


class CameraBinary:
    def __init__(self):
        self.view_matrix = None
        self.zNear = None
        self.zFar = None
        self.fov = None
        self.aspect_ratio = None
        self.unknown_0x50 = None
        self.unknown_0x54 = 0
        self.unknown_0x55 = 0.
        self.unknown_0x59 = 0.
                   
    def __repr__(self):
        return f"[GFD::SceneContainer::SceneNode::Attachment::Camera] {list_formatter(self.transform)}" \
            f"{self.zNear} {self.zFar} {self.fov} {self.aspect_ratio} {self.unknown_0x50}"
    
    def exbip_rw(self, rw, version):
        self.view_matrix  = rw.rw_float32s(self.view_matrix, 16) # Always identity
        self.zNear        = rw.rw_float32(self.zNear) # 1, 10, 100
        self.zFar         = rw.rw_float32(self.zFar)  # 4000, 20000, 400000, 600000
        self.fov          = rw.rw_float32(self.fov)   # Degrees, 0 - 90
        self.aspect_ratio = rw.rw_float32(self.aspect_ratio) # 1, 4/3, 3/2, 16/9
        self.unknown_0x50 = rw.rw_float32(self.unknown_0x50) # Always 0 ( roll)
        if version > 0x02110050:
            self.unknown_0x54 = rw.rw_int8(self.unknown_0x54)
            self.unknown_0x55 = rw.rw_float32(self.unknown_0x55)
            self.unknown_0x59 = rw.rw_float32(self.unknown_0x59)
