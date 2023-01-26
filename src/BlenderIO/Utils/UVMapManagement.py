def make_uv_map_name(idx):
    return f"UV{idx}"

def is_valid_uv_map(name):
    return (name[:2].upper() == "UV") and (name[2:].isdigit())

def get_uv_idx_from_name(name):
    return int(name[2:])
