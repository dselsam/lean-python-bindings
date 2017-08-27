import lean

"""
lean/src/util/name.h
"""


class NameView(lean.name):
    def __init__(self, name):
        self.name = name

    def destruct(self):
        # type: lean.name -> (string, string, int)
        return (self.name.get_prefix(),
                self.name.get_string(),
                self.name.get_numeral())


# -------------------------------------
# Utility

def to_name_view(name):
    return NameView(name)
