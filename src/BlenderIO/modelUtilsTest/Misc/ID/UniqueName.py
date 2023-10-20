import math


def new_unique_name(root, name_list, max_idx=999, separator="_"):
    new_name = root
    idx = 0
    max_digits = math.floor(math.log10(max_idx)) + 1
    while new_name in name_list:
        idx += 1
        if idx > max_idx:
            raise ValueError(f"Exceeded maximum name index '{max_idx}'")
        new_name = f"{root}{separator}{idx:0>{max_digits}}"

    return new_name
