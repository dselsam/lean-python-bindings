import lean

print "importing modules...",
env1 = lean.import_modules(["/usr/local/lib/lean/library"], [lean.name("init")])
print "...done"

print "should be 'Type':"
print env1.get(lean.name("nat")).get_type()
print "should be 'tactic.{0} (expr bool.tt)':"
print env1.get(lean.name(lean.name("tactic"), "intro1")).get_type()


