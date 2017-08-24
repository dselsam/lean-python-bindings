import gc
import lean

lean.initialize()

env = lean.import_modules(["/usr/local/lib/lean/library"], [lean.name("init")], 100000)
options = lean.options()

decl_name = lean.name("my_theorem")

lctx = lean.local_context()
mctx = lean.metavar_context()

goal_type = lean.mk_arrow(lean.mk_constant(lean.name("true")), lean.mk_constant(lean.name("false")))

goal = mctx.mk_metavar_decl(lctx, goal_type)
goals = lean.list_expr(goal, lean.list_expr()) # TODO(dhs): python lists

deq_state = lean.defeq_can_state()
tustate = lean.tactic_user_state()

tstate = lean.tactic_state(env, options, decl_name, mctx, goals, goal, deq_state, tustate)

ls = lean.list_name()

tac_intro1 = lean.mk_constant(lean.name(lean.name("tactic"), "intro1"))

print "about to run tactic..."
r = lean.run_tactic(tstate, tac_intro1, ls, [])
print "run_tactic returned"

print "result: ", r.is_some()
if r.is_some():
    print "value: ", lean.to_star(r.value()[0])
    
tstate2 = r.value()[1]

new_goal = tstate2.goals().head()

tac_infer_type = lean.mk_constant(lean.name(lean.name("tactic"), "infer_type"))

result2 = lean.run_tactic(tstate2, tac_infer_type, ls, [lean.to_obj(new_goal)])

ty = lean.to_expr(result2.value()[0])

print "should be 'false':"
print ty

