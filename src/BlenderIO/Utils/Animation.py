ANIM_DELIMITER = "|"


def gapnames_from_nlatrack(nla_track):
    gap_name, _, anim_name = nla_track.name.rpartition(ANIM_DELIMITER)
    gap_name, _, anim_type = gap_name.rpartition(ANIM_DELIMITER)
    return gap_name, anim_type, anim_name


def gapnames_to_nlatrack(gap_name, anim_type, anim_name):
    return f"{gap_name}{ANIM_DELIMITER}{anim_type}{ANIM_DELIMITER}{anim_name}"


def is_anim_restpose(nla_track):
    return nla_track.name == "Rest Pose"
