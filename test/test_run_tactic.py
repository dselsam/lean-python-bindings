from nose.tools import assert_equals, assert_not_equals, assert_false, assert_true
import lean
import os

def print_local_decl(d):
    print("\n", d.get_pp_name(), " : ", d.get_type())

def print_main_goal(tstate):
    goal_expr = tstate.goals().head()
    goal_decl = tstate.mctx().get_metavar_decl(goal_expr)
    lctx_for_goal_decl = goal_decl.get_context()
    print("\nGoal:",)
    lctx_for_goal_decl.for_each(print_local_decl)
    print("\n-----------------------")
    print(goal_decl.get_type(), "\n")

def create_tactic_state(env, goal_type):
  options = lean.options()
  decl_name = lean.name("my_theorem")

  lctx = lean.local_context()
  mctx = lean.metavar_context()

  goal = mctx.mk_metavar_decl(lctx, goal_type)
  goals = lean.list_expr(goal, lean.list_expr()) # TODO(dhs): python lists

  deq_state = lean.defeq_can_state()
  tustate = lean.tactic_user_state()

  tstate = lean.tactic_state(env, options, decl_name, mctx, goals, goal, deq_state, tustate)
  return tstate

def run_tactic(tstate, tactic, args):
  ls = lean.list_name()
  r = lean.run_tactic(tstate, tactic, ls, args)
  if r.is_some(): return r.value()
  else: return None

lean.initialize()

MY_PATH_TO_LEAN_STDLIB = os.environ['MY_PATH_TO_LEAN_STDLIB']

env = lean.import_modules([MY_PATH_TO_LEAN_STDLIB], [lean.name("init")], 100000)

goal_type = lean.mk_arrow(lean.mk_constant(lean.name("true")), lean.mk_constant(lean.name("false")))

tstate = create_tactic_state(env, goal_type)

print_main_goal(tstate)

tac_intro1 = lean.mk_constant(lean.name(lean.name("tactic"), "intro1"))

(_, tstate2) = run_tactic(tstate, tac_intro1, [])

print_main_goal(tstate2)

new_goal = tstate2.goals().head()
tac_infer_type = lean.mk_constant(lean.name(lean.name("tactic"), "infer_type"))

(result, tstate3) = run_tactic(tstate2, tac_infer_type, [lean.to_obj(new_goal)])

ty = lean.to_expr(result)
assert_equals(str(ty), "false")

