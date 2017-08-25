import lean


class DeclView(lean.declaration):
    def __init__(self, decl):
        self.decl = decl

    def destruct(self):
        return (self.decl.get_name(),
                self.decl.get_univ_params(),
                self.decl.get_num_univ_params(),
                self.decl.get_type(),
                self.decl.get_value())


class EnvView(lean.environment):
    def __init__(self, env):
        self.env = env
