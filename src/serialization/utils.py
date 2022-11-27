def chunk_list(lst, chunksize):
    return [lst[i:i + chunksize] for i in range(0, len(lst), chunksize)]


def flatten_list(lst):
    return [subitem for item in lst for subitem in item]

def safe_format(obj, formatter):
    return f"{obj if obj is None else formatter(obj)}"

hex8_format = '0x{0:>02x}'.format
hex16_format = '0x{0:>04x}'.format
hex32_format = '0x{0:>08x}'.format
hex64_format = '0x{0:>016x}'.format
