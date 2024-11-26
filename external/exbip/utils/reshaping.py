def standardize_shape(shape):
    if not hasattr(shape, "__getitem__"):
        shape = (shape,)
    return shape


def total_length(shape):
    total_length = 1
    for elem in shape:
        total_length *= elem
    return total_length


def split_list(lst, chunksize):
    return [lst[i:i + chunksize] for i in range(0, len(lst), chunksize)]


def reshape_list(lst, shape):
    out = lst
    for subshape in shape[1::][::-1]:
        out = split_list(out, subshape)
    return out


def flatten_list_first_dimension(lst):
    return [subitem for item in lst for subitem in item]


def flatten_list(lst, shape):
    flat_list = lst
    for dim in shape[1:]:
        flat_list = flatten_list_first_dimension(flat_list)
    return flat_list


def iter_flatten_list(lst, shape):
    # There's probably a smarter way to do this without an 'if'.
    if len(shape[1:]):
        for elem in lst:
            for subelem in iter_flatten_list(elem, shape[1:]):
                yield subelem
    else:
        for elem in lst:
            yield elem
