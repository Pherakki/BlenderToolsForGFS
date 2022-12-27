from .Binary import PhysicsBinary_0x1104130


PHYSICS_CONTAINER_MAP = {
    0x01105100: PhysicsBinary_0x1104130
}

def get_physics_container(version):
    if version not in PHYSICS_CONTAINER_MAP:
        raise NotImplementedError(f"Version {version:0>8X} does not have a PhysicsBinary type defined")
    return PHYSICS_CONTAINER_MAP[version]
