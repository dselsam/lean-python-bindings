from nose.tools import assert_equals, assert_not_equals, assert_false, assert_true

import lean
import os

from lang.expr import *
from lang.env import *

MY_PATH_TO_LEAN_STDLIB = os.environ['MY_PATH_TO_LEAN_STDLIB']

lean.initialize()

env = lean.import_modules([MY_PATH_TO_LEAN_STDLIB], [lean.name("init")], 100000)

assert_equals(env.get(lean.name("nat")).get_type(), lean.mk_Type())
assert_equals(str(env.get(lean.name(lean.name("tactic"), "intro1")).get_type()), "tactic.{0} (expr bool.tt)")

decls = []
add_to_list = lambda d: decls.append(d)
env.for_each_declaration(add_to_list)

# build theorem context
env_view = EnvView(env)

# TODO(danehuang): This is expensive -- is it necessary as a test?

# decls = env_view.get_decls()
# d_thm = env_view.thm_dict_of_decls(decls)
# for n, v in d_thm.items():
#     print(str(n))
#     mentioned_thms = gather_theorem(d_thm, v)
#     for thm in mentioned_thms:
#         print("   " + str(thm))
#     #print(unicode(n) + " -> " + to_expr_view(v).to_sexpr())
