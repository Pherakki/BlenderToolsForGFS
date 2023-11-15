def gapnames_from_nlatrack(nla_track):
    gap_name, _, anim_name = nla_track.name.rpartition("_")
    return gap_name, anim_name


def gapnames_to_nlatrack(gap_name, anim_name):
    return f"{gap_name}_{anim_name}"
