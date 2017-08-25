from __future__ import unicode_literals

import lean
import os

from lang.expr import *
from lang.env import *

MY_PATH_TO_LEAN_STDLIB = os.environ['MY_PATH_TO_LEAN_STDLIB']

lean.initialize()

env = lean.import_modules([MY_PATH_TO_LEAN_STDLIB], [lean.name("init")], 100000)

print "should be 'Type':"
print env.get(lean.name("nat")).get_type()
print "should be 'tactic.{0} (expr bool.tt)':"
print env.get(lean.name(lean.name("tactic"), "intro1")).get_type()

decls = []
add_to_list = lambda d: decls.append(d)
env.for_each_declaration(add_to_list)

print len(decls)

# build theorem context
ctx = {}
for decl in decls:
    if decl.is_theorem():
        n, up, nup, t, v = DeclView(decl).destruct()
        ctx[n] = v

for decl in decls:
    if decl.is_theorem():
        n, up, nup, t, v = DeclView(decl).destruct()
        print("A: " + unicode(n) + ", " + unicode(up) + ", " + unicode(nup) + ", " + unicode(t) + ", " + unicode(type(v)))
        print("B: " + unicode(gather_theorem(ctx, v)))
        #print("A: " + unicode(n) + ", " + unicode(up) + ", " + unicode(nup) + ", " + unicode(t))
        #print("B: " + unicode(v))
    #print gather_constant(env, v)

    #print(unicode(n) + ", " + unicode(up) + ", " + unicode(nup) + ", " + unicode(t) + ", " + unicode(type(v)))
