def make_uv_map_name(idx):
    return f"UV{idx}"

def is_valid_uv_map(name):
    return (name[:2] == "UV") and (name[2:].isdigit())

def get_uv_idx_from_name(name):
    return int(name[2:])


def make_color_map_name(idx):
    return f"Map{idx}"

def is_valid_color_map(name):
    return (name[:3] == "Map") and (name[3:].isdigit())

def get_color_idx_from_name(name):
    return int(name[3:])
