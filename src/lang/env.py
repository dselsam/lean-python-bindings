import lean


class DeclView(lean.declaration):
    def __init__(self, decl):
        self.decl = decl

    def destruct(self):
        # type: DeclView -> (lean.name, ?, ?, lean.expr, lean.expr)
        return (self.decl.get_name(),
                self.decl.get_univ_params(),
                self.decl.get_num_univ_params(),
                self.decl.get_type(),
                self.decl.get_value())

    def mentions(self, env):
        self.decl.get_value()


class EnvView(lean.environment):
    def __init__(self, env):
        self.env = env

    def gather_decls(self):
        # type: EnvView -> [lean.declaration]
        decls = []
        self.env.for_each_declaration(lambda decl: decls.append(decl))
        return decls