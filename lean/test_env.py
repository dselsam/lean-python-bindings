from __future__ import unicode_literals

import lean
import os

from lang.expr import *
from lang.env import *

MY_PATH_TO_LEAN_STDLIB = os.environ['MY_PATH_TO_LEAN_STDLIB']


lean.initialize()

env = lean.import_modules([MY_PATH_TO_LEAN_STDLIB], [lean.name("init")], 100000)

print("should be 'Type':")
print(env.get(lean.name("nat")).get_type())
print("should be 'tactic.{0} (expr bool.tt)':")
print(env.get(lean.name(lean.name("tactic"), "intro1")).get_type())

decls = []
add_to_list = lambda d: decls.append(d)
env.for_each_declaration(add_to_list)

print(len(decls))

# build theorem context
env_view = EnvView(env)

decls = env_view.get_decls()
d_thm = env_view.thm_dict_of_decls(decls)
for n, v in d_thm.items():
    print(str(n))
    mentioned_thms = gather_theorem(d_thm, v)
    for thm in mentioned_thms:
        print("   " + str(thm))
    #print(unicode(n) + " -> " + to_expr_view(v).to_sexpr())
