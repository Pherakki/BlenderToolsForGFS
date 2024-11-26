import re

NATURAL_SORT_PATTERN = re.compile('([0-9]+)')

def get_name_string(nametype, name_bytes, encoding, errorlog):
    try:
        return name_bytes.decode(encoding)
    except UnicodeDecodeError:
        safename = name_bytes.decode(encoding, errors='replace')
        errorlog.log_warning_message(f"{nametype} has an undecodable name '{safename}'")
        return safename

def set_name_string(nametype, name, encoding, errorlog):
    try:
        return name.encode(encoding)
    except UnicodeEncodeError:
        safename = name.encode(encoding, errors='replace')
        errorlog.log_warning_message(f"{nametype} has a non-{encoding} name '{safename}'")
        return safename

def natural_sort(l, accessor=lambda x: x):
    """
    Adapted from https://stackoverflow.com/a/4836734
    """
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in NATURAL_SORT_PATTERN.split(key)]
    return sorted(l, key=lambda x: alphanum_key(accessor(x)))
