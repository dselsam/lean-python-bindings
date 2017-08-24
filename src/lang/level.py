import lean

"""
lean/src/kernel/level.h
"""


# =========================================================
# lean.list_level constructor aliases

def mk_list_level_nil():
    # type: lean.list_level
    return lean.list_level()


def mk_list_level_cons(lvl, lls):
    # type: lean.level -> lean.list_level -> lean.list_level
    return lean.list_level(lvl, lls)


# =========================================================
# Utility

def mk_list_level_from_py_list(ls):
    # type: [lean.level] -> lean.list_level
    """Convert Python list to lean.list_level
    """

    # foldr
    acc = mk_list_level_nil()
    for lvl in ls[::-1]:
        acc = mk_list_level_cons(lvl, acc)
    return acc
