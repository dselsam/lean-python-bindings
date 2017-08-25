from __future__ import unicode_literals

import lean

import lang.level as level
"""
Python wrapper for Lean expressions

Taken from lean/src/kernel/expr.h
expr ::=   Var           idx
       |   Sort          level
       |   Constant      name [levels]
       |   Meta          name expr
       |   Local         name expr
       |   App           expr expr
       |   Lambda        name expr expr
       |   Pi            name expr expr
       |   Let           name expr expr expr
       |   Macro         macro
"""


# =========================================================
# Expression Views

class ExprView(lean.expr):
    def __init__(self, expr):
        self.expr = expr

    def destruct(self):
        """Pull's out all of the contents of the expression
        """
        raise NameError("Should not call.")

    def to_sexpr(self):
        raise NameError("Should not call.")


# -------------------------------------
# Cases

class VarView(ExprView):
    def __init__(self, expr):
        assert expr.kind() == lean.Var
        super(VarView, self).__init__(expr)

    def destruct(self):
        # type: VarView -> int
        return self.expr.var_idx()

    def to_sexpr(self):
        x = self.destruct()
        return "Var(" + unicode(x) + ")"


class SortView(ExprView):
    def __init__(self, expr):
        assert expr.kind() == lean.Sort
        super(SortView, self).__init__(expr)

    def destruct(self):
        # type: SortView -> lean.level
        return self.expr.sort_level()

    def to_sexpr(self):
        lvl = self.destruct()
        return "Sort(" + unicode(lvl) + ")"


class ConstantView(ExprView):
    def __init__(self, expr):
        assert expr.kind() == lean.Constant
        super(ConstantView, self).__init__(expr)

    def destruct(self):
        # type: ConstView -> (lean.name, lean.list_level)
        return (self.expr.const_name(), self.expr.const_levels())

    def to_sexpr(self):
        c, lvl = self.destruct()
        return "Constant(" + unicode(c) + ", " + unicode(lvl) + ")"


class MetaView(ExprView):
    def __init__(self, expr):
        assert expr.kind() == lean.Meta
        super(MetaView, self).__init__(expr)

    def destruct(self):
        # type: MetaView -> (lean.name, lean.expr, lean.name)
        return (self.expr.mlocal_name(),
                self.expr.mlocal_type(),
                self.expr.mlocal_pp_name())

    def to_sexpr(self):
        x, t, ppx = self.destruct()
        return "Metavar(" + unicode(x) + ", " + to_expr_view(t).to_sexpr() + ", " + unicode(ppx) + ")"


class LocalView(ExprView):
    def __init__(self, expr):
        assert expr.kind() == lean.LocalView
        super(LocalView, self).__init__(expr)

    def destruct(self):
        # type: LocalView -> ??
        return self.expr.local_info()

    def to_sexpr(self):
        li = self.destruct()
        return "Local(" + unicode(li) + ")"


class AppView(ExprView):
    def __init__(self, expr):
        assert expr.kind() == lean.App
        super(AppView, self).__init__(expr)

    def destruct(self):
        # type: AppView -> (lean.expr, lean.expr)
        return (self.expr.app_fn(), self.expr.app_arg())

    def to_sexpr(self):
        e1, e2 = self.destruct()
        return "App(" + to_expr_view(e1).to_sexpr() + ", " + to_expr_view(e2).to_sexpr() + ")"


class LambdaView(ExprView):
    def __init__(self, expr):
        assert expr.kind() == lean.Lambda
        super(LambdaView, self).__init__(expr)

    def destruct(self):
        # type: LambdaView -> (lean.name, lean.expr, lean.expr, lean.binder_info, lean.tag)
        return (self.expr.binding_name(),
                self.expr.binding_domain(),
                self.expr.binding_body(),
                self.expr.binding_info(),
                self.expr.get_tag())

    def to_sexpr(self):
        n, t, e, bi, g = self.destruct()
        return "Lambda(" + unicode(n) + ", " + to_expr_view(t).to_sexpr() + ", " + to_expr_view(e).to_sexpr() + ", " + unicode(bi) + ", " + unicode(g) + ")"


class PiView(ExprView):
    def __init__(self, expr):
        assert expr.kind() == lean.Pi
        super(PiView, self).__init__(expr)

    def destruct(self):
        # type: PiView -> (lean.name, lean.expr, lean.expr, lean.binder_info, lean.tag)
        return (self.expr.binding_name(),
                self.expr.binding_domain(),
                self.expr.binding_body(),
                self.expr.binding_info(),
                self.expr.get_tag())

    def to_sexpr(self):
        n, t, e, bi, g = self.destruct()
        return "Pi(" +  ", " + to_expr_view(t).to_sexpr() + ", " + to_expr_view(e).to_sexpr() + ", " + unicode(bi) + ", " + unicode(g) + ")"


class LetView(ExprView):
    def __init__(self, expr):
        assert expr.kind() == lean.Let
        super(LetView, self).__init__(expr)

    def destruct(self):
        # type: LetView -> lean.expr -> lean.expr -> lean.expr -> lean.tag -> lean.expr
        return (self.expr.let_name(),
                self.expr.let_type(),
                self.expr.let_value(),
                self.expr.let_body())

    def to_sexpr(self):
        x, t, v, e = self.destruct()
        return "Let(" + unicode(x) + ", " + to_expr_view(t).to_sexpr() + ", " + to_expr_view(v).to_sexpr() + ", " + to_expr_view(e).to_sexpr() + ")"


class MacroView(ExprView):
    def __init__(self, expr):
        assert expr.kind() == lean.Macro
        super(MacroView, self).__init__(expr)

    def destruct(self):
        # type: ? -> ? -> ? -> lean.expr
        acc = []
        for arg in range(0, self.expr.macro_num_args()):
            acc += self.expr.macro_arg()
        # TODO: expose macro_def??
        # return (self.expr.macro_def(), self.expr.macro_num_args(), acc)
        return (self.expr.macro_num_args(), acc)

    def to_sexpr(self):
        #e, nargs, args = self.destruct()
        nargs, args = self.destruct()
        return "Macro(" + unicode(nargs) + ", " + unicode(args) + ")"


# -------------------------------------
# Utility

def to_expr_view(expr):
    ek = expr.kind()
    if ek == lean.Var:
        return VarView(expr)
    elif ek == lean.Sort:
        return SortView(expr)
    elif ek == lean.Constant:
        return ConstantView(expr)
    elif ek == lean.Meta:
        return MetaView(expr)
    elif ek == lean.Local:
        return LocalView(expr)
    elif ek == lean.App:
        return AppView(expr)
    elif ek == lean.Lambda:
        return LambdaView(expr)
    elif ek == lean.Pi:
        return PiView(expr)
    elif ek == lean.Let:
        return LetView(expr)
    elif ek == lean.Macro:
        return MacroView(expr)
    else:
        raise NameError("Unexpected lean.expr kind: " + unicode(ek))
