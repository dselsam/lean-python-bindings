import lean

import lang.expr as expr


# =========================================================
# Declaration Views

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

    def mentions(self, d_thm):
        v = self.decl.get_value()
        return expr.gather_theorem(d_thm, v)


# =========================================================
# Environment Views

class EnvView(lean.environment):
    def __init__(self, env):
        # type: lean.environment -> None
        self.env = env

    def get_decls(self, f=None):
        # type: (lean.declaration -> bool) -> [lean.declaration]
        decls = []
        self.env.for_each_declaration(lambda decl: decls.append(decl))

        if f:
            decls = filter(lambda decl: f(decl), decls)

        return decls

    def get_theorems(self):
        # type: (lean.declaration -> bool) -> [lean.declaration]
        return self.get_decls(lambda decl: decl.is_theorem())

    def thm_dict_of_decls(self, decls):
        # type: [lean.declaration] -> dict<lean.name, lean.expr>
        d_thm = {}
        for decl in decls:
            if decl.is_theorem():
                n, up, nup, t, v = DeclView(decl).destruct()
                d_thm[n] = v
        return d_thm
