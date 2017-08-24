import lean

lean.initialize()

env = lean.import_modules(["/usr/local/lib/lean/library"], [lean.name("init")], 100000)

print "should be 'Type':"
print env.get(lean.name("nat")).get_type()
print "should be 'tactic.{0} (expr bool.tt)':"
print env.get(lean.name(lean.name("tactic"), "intro1")).get_type()

decls = []
add_to_list = lambda d: decls.append(d)
env.for_each_declaration(add_to_list)

print len(decls)

