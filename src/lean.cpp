#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

#include <sstream>

#include "init/init.h"
#include "util/name.h"
#include "util/list.h"
#include "util/optional.h"
#include "util/path.h"
#include "util/lean_path.h"
#include "kernel/level.h"
#include "kernel/expr.h"
#include "kernel/declaration.h"
#include "kernel/environment.h"
#include "kernel/standard_kernel.h"
#include "kernel/type_checker.h"
#include "library/module.h"
#include "library/util.h"
#include "library/eval_helper.h"
#include "library/metavar_context.h"
#include "library/defeq_canonizer.h"
#include "library/tactic/tactic_state.h"
#include "library/compiler/vm_compiler.h"
#include "library/vm/vm.h"
#include "library/vm/vm_expr.h"

namespace py = pybind11;

PYBIND11_PLUGIN(lean) {
  py::module m("lean", "pybind11 lean plugin");

  m.def("initialize", &lean::initialize);

  py::class_<lean::options>(m, "options")
    .def(py::init<>())
    .def("contains", [&](lean::options const & self, lean::name const & n) { return self.contains(n); })

    .def("get_bool", [&](lean::options const & self, lean::name const & n, bool default_value) {
	return self.get_bool(n, default_value); },
      py::arg("n"), py::arg("default_value") = false)

    .def("get_int", [&](lean::options const & self, lean::name const & n, int default_value) {
	return self.get_int(n, default_value); },
      py::arg("n"), py::arg("default_value") = 0)
    
    .def("get_unsigned", [&](lean::options const & self, lean::name const & n, unsigned default_value) {
	return self.get_unsigned(n, default_value); },
      py::arg("n"), py::arg("default_value") = 0)

    .def("get_double", [&](lean::options const & self, lean::name const & n, double default_value) {
	return self.get_double(n, default_value); },
      py::arg("n"), py::arg("default_value") = 0.0)

    .def("get_string", [&](lean::options const & self, lean::name const & n, std::string default_value) {
	return std::string(self.get_string(n, default_value.c_str())); },
      py::arg("n"), py::arg("default_value") = "")

    // TODO(dhs): sexprs

    .def("join", [&](lean::options const & self, lean::options const & other) {
	return join(self, other); })

    .def("__eq__", [&](lean::options const & self, lean::options const & other) { return self == other; })
    .def("__ne__", [&](lean::options const & self, lean::options const & other) { return !(self == other); })
    .def("__hash__", &lean::options::hash)
    ;

  py::class_<lean::name>(m, "name")
    .def(py::init<>())
    .def(py::init<std::string>())
    .def(py::init<lean::name const &, char const *>())
    .def(py::init<lean::name const &, unsigned>())

    .def("is_anonymous", &lean::name::is_anonymous)
    .def("is_string", &lean::name::is_string)
    .def("is_numeral", &lean::name::is_numeral)
    .def("is_atomic", &lean::name::is_atomic)
    .def("get_numeral", &lean::name::get_numeral)
    .def("get_string", &lean::name::get_string)
    .def("get_prefix", &lean::name::get_prefix)

    .def("__str__", [&](lean::name const & self) { return self.to_string(); })
    .def("__cmp__", [&](lean::name const & self, lean::name const & other) { return cmp(self, other); })
    .def("__hash__", &lean::name::hash)                    
  ;

  py::class_<lean::optional<lean::name> >(m, "optional_name")
    .def(py::init<>())
    .def(py::init<lean::name>())
    .def("is_some", [&](lean::optional<lean::name> const & self) { return self; })
    .def("value", [&](lean::optional<lean::name> const & self) { return self.value(); })

    .def("__eq__", [&](lean::optional<lean::name> const & self, lean::optional<lean::name> const & other) { return self == other; })
    .def("__ne__", [&](lean::optional<lean::name> const & self, lean::optional<lean::name> const & other) { return self != other; })
  ;

  py::class_<lean::list<lean::name> >(m, "list_name")
    .def(py::init<>())
    .def(py::init<lean::name const &, lean::list<lean::name> const &>())

    .def("is_nil", [&](lean::list<lean::name> const & self) { return is_nil(self); })
    .def("head", [&](lean::list<lean::name> const & self) { return head(self); })
    .def("tail", [&](lean::list<lean::name> const & self) { return tail(self); })

    .def("__str__", [&](lean::list<lean::name> const & self) { std::ostringstream os; os << self; return os.str(); })
    ;
  
  py::enum_<lean::level_kind>(m, "level_kind")
    .value("Zero", lean::level_kind::Zero)
    .value("Succ", lean::level_kind::Succ)
    .value("Max", lean::level_kind::Max)
    .value("IMax", lean::level_kind::IMax)
    .value("Param", lean::level_kind::Param)
    .value("Meta", lean::level_kind::Meta)    
    .export_values();
  
  py::class_<lean::level>(m, "level")
    .def(py::init<>())

    .def("kind", &lean::level::kind)                        

    .def("is_zero", [&](lean::level const & self) { return lean::is_zero(self); })
    .def("is_succ", [&](lean::level const & self) { return lean::is_succ(self); })
    .def("is_max", [&](lean::level const & self) { return lean::is_max(self); })
    .def("is_imax", [&](lean::level const & self) { return lean::is_imax(self); })
    .def("is_param", [&](lean::level const & self) { return lean::is_param(self); })
    .def("is_meta", [&](lean::level const & self) { return lean::is_meta(self); })

    .def("succ_of", [&](lean::level const & self) { return lean::succ_of(self); })
    .def("max_lhs", [&](lean::level const & self) { return lean::max_lhs(self); })
    .def("max_rhs", [&](lean::level const & self) { return lean::max_rhs(self); })
    .def("imax_lhs", [&](lean::level const & self) { return lean::imax_lhs(self); })
    .def("imax_rhs", [&](lean::level const & self) { return lean::imax_rhs(self); })
    .def("param_id", [&](lean::level const & self) { return lean::param_id(self); })
    .def("meta_id", [&](lean::level const & self) { return lean::meta_id(self); })

    .def("__hash__", &lean::level::hash)
    
    // TODO(dhs): I am currently assuming we are only using printing for sanity-checks and debugging.
    // We may need to add support for pretty-printing and formatting and such later on.
    .def("__str__", [&](lean::level const & self) { std::ostringstream os; os << self; return os.str(); })

    .def("__eq__", [&](lean::level const & self, lean::level const & other) { return self == other; })
    .def("__ne__", [&](lean::level const & self, lean::level const & other) { return self != other; })
    
    ;

  m.def("mk_level_zero", &lean::mk_level_zero);
  m.def("mk_level_one", &lean::mk_level_one);
  m.def("mk_succ", &lean::mk_succ);
  m.def("mk_max", &lean::mk_max);
  m.def("mk_imax", &lean::mk_imax);
  m.def("mk_param_univ", &lean::mk_param_univ);
  m.def("mk_meta_univ", &lean::mk_meta_univ);

  py::class_<lean::list<lean::level> >(m, "list_level")
    .def(py::init<>())
    .def(py::init<lean::level const &, lean::list<lean::level> const &>())

    .def("is_nil", [&](lean::list<lean::level> const & self) { return is_nil(self); })
    .def("head", [&](lean::list<lean::level> const & self) { return head(self); })
    .def("tail", [&](lean::list<lean::level> const & self) { return tail(self); })

    .def("__str__", [&](lean::list<lean::level> const & self) { std::ostringstream os; os << self; return os.str(); })
    ;

  py::class_<lean::binder_info>(m, "binder_info")
    .def(py::init<>())
    .def("is_implicit", &lean::binder_info::is_implicit)
    .def("is_strict_implicit", &lean::binder_info::is_strict_implicit)
    .def("is_inst_implicit", &lean::binder_info::is_inst_implicit)
    .def("is_explicit", [&](lean::binder_info const & self) {
	    return !self.is_implicit() && !self.is_strict_implicit() && !self.is_inst_implicit();
      })
    
    .def("__hash__", &lean::binder_info::hash)
    ;

  m.def("mk_implicit_binder_info", &lean::mk_implicit_binder_info);
  m.def("mk_strict_implicit_binder_info", &lean::mk_strict_implicit_binder_info);
  m.def("mk_inst_implicit_binder_info", &lean::mk_inst_implicit_binder_info);

  py::class_<lean::binder>(m, "binder")
    .def(py::init<lean::name const &, lean::expr const &, lean::binder_info const &>())

    .def("get_name", &lean::binder::get_name)
    .def("get_type", &lean::binder::get_type)
    .def("get_info", &lean::binder::get_info)

    ;
  
  py::enum_<lean::expr_kind>(m, "expr_kind")
    .value("Var", lean::expr_kind::Var)
    .value("Sort", lean::expr_kind::Sort)
    .value("Constant", lean::expr_kind::Constant)
    .value("Meta", lean::expr_kind::Meta)
    .value("Local", lean::expr_kind::Local)
    .value("App", lean::expr_kind::App)    
    .value("Lambda", lean::expr_kind::Lambda)
    .value("Pi", lean::expr_kind::Pi)
    .value("Let", lean::expr_kind::Let)
    .value("Macro", lean::expr_kind::Macro)    
    .export_values();

  py::class_<lean::expr>(m, "expr")
    .def(py::init<>())

    .def("kind", &lean::expr::kind)

    .def("is_var", [&](lean::expr const & self) { return lean::is_var(self); })
    .def("is_constant", [&](lean::expr const & self) { return lean::is_constant(self); })
    .def("is_local", [&](lean::expr const & self) { return lean::is_local(self); })
    .def("is_metavar", [&](lean::expr const & self) { return lean::is_metavar(self); })    
    .def("is_macro", [&](lean::expr const & self) { return lean::is_macro(self); })
    .def("is_app", [&](lean::expr const & self) { return lean::is_app(self); })
    .def("is_lambda", [&](lean::expr const & self) { return lean::is_lambda(self); })
    .def("is_pi", [&](lean::expr const & self) { return lean::is_pi(self); })    
    .def("is_let", [&](lean::expr const & self) { return lean::is_let(self); })
    .def("is_sort", [&](lean::expr const & self) { return lean::is_sort(self); })
    .def("is_binding", [&](lean::expr const & self) { return lean::is_binding(self); })
    .def("is_mlocal", [&](lean::expr const & self) { return lean::is_mlocal(self); })

    .def("is_atomic", [&](lean::expr const & self) { return lean::is_atomic(self); })
    .def("is_arrow", [&](lean::expr const & self) { return lean::is_arrow(self); })
    .def("is_meta_app", [&](lean::expr const & self) { return lean::is_meta(self); })

    .def("var_idx", [&](lean::expr const & self) { return lean::var_idx(self); })
    .def("const_name", [&](lean::expr const & self) { return lean::const_name(self); })
    .def("const_levels", [&](lean::expr const & self) { return lean::const_levels(self); })
    .def("macro_def", [&](lean::expr const & self) { return lean::macro_def(self); })
    .def("macro_num_args", [&](lean::expr const & self) { return lean::macro_num_args(self); })
    .def("macro_arg", [&](lean::expr const & self, unsigned i) { return lean::macro_arg(self, i); })
    .def("app_fn", [&](lean::expr const & self) { return lean::app_fn(self); })
    .def("app_arg", [&](lean::expr const & self) { return lean::app_arg(self); })
    .def("binding_name", [&](lean::expr const & self) { return lean::binding_name(self); })
    .def("binding_domain", [&](lean::expr const & self) { return lean::binding_domain(self); })            
    .def("binding_body", [&](lean::expr const & self) { return lean::binding_body(self); })
    .def("binding_info", [&](lean::expr const & self) { return lean::binding_info(self); })
    .def("binding_binder", [&](lean::expr const & self) { return lean::binding_binder(self); })
    .def("sort_level", [&](lean::expr const & self) { return lean::sort_level(self); })
    .def("mlocal_name", [&](lean::expr const & self) { return lean::mlocal_name(self); })
    .def("mlocal_type", [&](lean::expr const & self) { return lean::mlocal_type(self); })                            
    .def("mlocal_pp_name", [&](lean::expr const & self) { return lean::mlocal_pp_name(self); })
    .def("local_info", [&](lean::expr const & self) { return lean::local_info(self); })
    .def("let_name", [&](lean::expr const & self) { return lean::let_name(self); })
    .def("let_type", [&](lean::expr const & self) { return lean::let_type(self); })                            
    .def("let_value", [&](lean::expr const & self) { return lean::let_value(self); })
    .def("let_body", [&](lean::expr const & self) { return lean::let_body(self); })                            

    .def("get_tag", &lean::expr::get_tag)

    .def("__hash__", &lean::expr::hash)    
    .def("__str__", [&](lean::expr const & self) {
	std::ostringstream os;
	os << self;
	return os.str();
      })

    .def("__eq__", [&](lean::expr const & self, lean::expr const & other) { return self == other; })
    .def("__ne__", [&](lean::expr const & self, lean::expr const & other) { return self != other; })
    ;
  
  m.def("mk_var", &lean::mk_var, py::arg("idx"), py::arg("g") = lean::nulltag);
  m.def("mk_constant", [&](lean::name const & n, lean::levels const & ls = lean::list<lean::level>(), lean::tag g = lean::nulltag) {
      return lean::mk_constant(n, ls, g); },
    py::arg("n"), py::arg("ls") = lean::list<lean::level>(), py::arg("g") = lean::nulltag);

  m.def("mk_metavar", [&](lean::name const & n, lean::expr const & t, lean::tag g) {
      return lean::mk_metavar(n, t, g); },
    py::arg("n"), py::arg("t"), py::arg("g") = lean::nulltag);

  m.def("mk_metavar", [&](lean::name const & n, lean::name const & pp_n, lean::expr const & t, lean::tag g) {
      return lean::mk_metavar(n, pp_n, t, g); },
    py::arg("n"), py::arg("pp_n"), py::arg("t"), py::arg("g") = lean::nulltag);

  m.def("mk_local", [&](lean::name const & n, lean::name const & pp_n, lean::expr const & t, lean::binder_info const & bi, lean::tag g) {
      return lean::mk_local(n, pp_n, t, bi, g); },
    py::arg("n"), py::arg("pp_n"), py::arg("t"), py::arg("bi") = lean::binder_info(), py::arg("g") = lean::nulltag);

  m.def("mk_app", [&](lean::expr const & f, lean::expr const & a, lean::tag g) {
      return lean::mk_app(f, a, g); },
    py::arg("f"), py::arg("a"), py::arg("g") = lean::nulltag);

  m.def("mk_lambda", [&](lean::name const & n, lean::expr const & t, lean::expr const & e, lean::binder_info const & bi, lean::tag g) {
      return lean::mk_lambda(n, t, e, bi, g); },
    py::arg("n"), py::arg("t"), py::arg("e"), py::arg("bi") = lean::binder_info(), py::arg("g") = lean::nulltag);

  m.def("mk_pi", [&](lean::name const & n, lean::expr const & t, lean::expr const & e, lean::binder_info const & bi, lean::tag g) {
      return lean::mk_pi(n, t, e, bi, g); },
    py::arg("n"), py::arg("t"), py::arg("e"), py::arg("bi") = lean::binder_info(), py::arg("g") = lean::nulltag);

  m.def("mk_let", [&](lean::name const & n, lean::expr const & t, lean::expr const & v, lean::expr const & b, lean::tag g) {
      return lean::mk_let(n, t, v, b, g); },
    py::arg("n"), py::arg("t"), py::arg("v"), py::arg("b"), py::arg("g") = lean::nulltag);
  
  m.def("mk_sort", [&](lean::level const & l, lean::tag g) {
      return lean::mk_sort(l, g); },
    py::arg("l"), py::arg("g") = lean::nulltag);

  m.def("mk_Prop", &lean::mk_Prop);
  m.def("mk_Type", &lean::mk_Type);
  m.def("mk_arrow", &lean::mk_arrow, py::arg("t"), py::arg("e"), py::arg("g") = lean::nulltag);

  py::class_<lean::list<lean::expr> >(m, "list_expr")
    .def(py::init<>())
    .def(py::init<lean::expr const &, lean::list<lean::expr> const &>())

    .def("is_nil", [&](lean::list<lean::expr> const & self) { return is_nil(self); })
    .def("head", [&](lean::list<lean::expr> const & self) { return head(self); })
    .def("tail", [&](lean::list<lean::expr> const & self) { return tail(self); })

    .def("__str__", [&](lean::list<lean::expr> const & self) { std::ostringstream os; os << self; return os.str(); })
    ;
  
  py::class_<lean::declaration>(m, "declaration")
    .def(py::init<>())
    .def("is_definition", &lean::declaration::is_definition)
    .def("is_axiom", &lean::declaration::is_axiom)
    .def("is_theorem", &lean::declaration::is_theorem)
    .def("is_constant_assumption", &lean::declaration::is_constant_assumption)
    .def("is_trusted", &lean::declaration::is_trusted)

    .def("get_name", &lean::declaration::get_name)
    .def("get_univ_params", &lean::declaration::get_univ_params)
    .def("get_num_univ_params", &lean::declaration::get_num_univ_params)
    .def("get_type", &lean::declaration::get_type)
    .def("get_value", &lean::declaration::get_value)
    ;

  m.def("mk_definition", [&](lean::environment const & env, lean::name const & n,
			     lean::level_param_names const & params, lean::expr const & t, lean::expr const & v, bool trusted) {
	  return lean::mk_definition(env, n, params, t, v, true, trusted); });

  m.def("mk_theorem", [&](lean::name const & n, lean::level_param_names const & params, lean::expr const & t, lean::expr const & v) {
      return lean::mk_theorem(n, params, t, v);
    });

  m.def("mk_axiom", [&](lean::name const & n, lean::level_param_names const & params, lean::expr const & t) {
      return lean::mk_axiom(n, params, t);
    });

  m.def("mk_constant_assumption", [&](lean::name const & n, lean::level_param_names const & params, lean::expr const & t, bool trusted) {
      return lean::mk_constant_assumption(n, params, t, trusted);
    });

  py::class_<lean::environment>(m, "environment")
    .def(py::init<>())
    .def("is_recursor", &lean::environment::is_recursor)
    .def("is_builtin", &lean::environment::is_builtin)   

    .def("find", &lean::environment::find)
    .def("get", &lean::environment::get)

    .def("for_each_declaration", [&](lean::environment const & self, py::function fn) {
	self.for_each_declaration([&](lean::declaration const & d) { fn(d); }); })
  ;

  m.def("mk_environment", &lean::mk_environment, py::arg("trust_lvl") = 0);

  m.def("import_modules", [&](std::vector<std::string> const & search_path, std::vector<lean::name> const & module_names, unsigned trust_lvl) {
      lean::environment env = lean::mk_environment(trust_lvl);
      std::vector<lean::module_name> imports;
      for (lean::name const & n : module_names) {
	imports.emplace_back(n);
      }
      return lean::import_modules(env, "", imports, lean::mk_olean_loader(search_path));
    });

  // TODO(dhs): expose more methods
  py::class_<lean::local_context>(m, "local_context")
    .def(py::init<>())
    ;

  // TODO(dhs): expose more methods  
  py::class_<lean::metavar_context>(m, "metavar_context")
    .def(py::init<>())
    .def("mk_metavar_decl", [&](lean::metavar_context & self, lean::local_context const & ctx, lean::expr const & type) {
	return self.mk_metavar_decl(ctx, type); })
    ;

  py::class_<lean::defeq_can_state>(m, "defeq_can_state")
    .def(py::init<>())
    ;

  py::class_<lean::tactic_user_state>(m, "tactic_user_state")
    .def(py::init<>())
    ;

  // TODO(dhs): expose more methods
  py::class_<lean::tactic_state>(m, "tactic_state")
    .def(py::init<lean::environment const &, lean::options const &, lean::name const &,
	 lean::metavar_context const &, lean::list<lean::expr> const &, lean::expr const &,
	 lean::defeq_can_state const &, lean::tactic_user_state const &>())
    .def(py::init<lean::tactic_state const &>())
    .def("goals", &lean::tactic_state::goals, py::return_value_policy::reference_internal)
    ;

  py::class_<lean::vm_obj>(m, "vm_obj")
    .def(py::init<>())
    ;

  py::class_<lean::optional<std::pair<lean::vm_obj, lean::tactic_state> > >(m, "optional_tactic_result")
    .def(py::init<>())
    .def(py::init<std::pair<lean::vm_obj const &, lean::tactic_state const &> >())
    .def("is_some", [&](lean::optional<std::pair<lean::vm_obj, lean::tactic_state> > const & self) { return static_cast<bool>(self); })
    .def("value", [&](lean::optional<std::pair<lean::vm_obj, lean::tactic_state> > const & self) { return self.value(); })
  ;

  m.def("mk_vm_unit", [&]() { return lean::mk_vm_unit(); });
  m.def("to_star", [&](lean::vm_obj const & s) { return py::tuple(); });    
  m.def("to_expr", [&](lean::vm_obj const & e) { return lean::to_expr(e); });
  m.def("to_obj", [&](lean::expr const & e) { return lean::to_obj(e); });  
  
  m.def("run_tactic", [&](lean::tactic_state const & ts, lean::expr const & tactic,
			  lean::level_param_names const & ls, std::vector<lean::vm_obj> const & _args) {
	  lean::name fn_name("_main");
	  lean::type_context tc(ts.env(), lean::transparency_mode::All);
	  lean::expr type = tc.infer(tactic);

	  lean::environment new_env = ts.env();
	  bool use_conv_opt   = true;
	  bool is_trusted     = false;
	  lean::certified_declaration cd = lean::check(new_env, mk_definition(new_env, fn_name, ls, type, tactic, use_conv_opt, is_trusted));
	  new_env = new_env.add(cd);
	  new_env = lean::vm_compile(new_env, new_env.get(fn_name));

	  lean::vm_state vms(new_env, ts.get_options());
	  
	  std::vector<lean::vm_obj> args;
	  args.push_back(lean::to_obj(ts));

	  for_each (_args.rbegin(), _args.rend(), [&](lean::vm_obj const & arg) {
	      args.push_back(arg);
	    });
	  
	  lean::vm_obj r = vms.invoke(fn_name, args.size(), args.data());
	  if (lean::tactic::is_result_success(r)) {
	    return lean::optional<std::pair<lean::vm_obj, lean::tactic_state> >(lean::mk_pair(lean::tactic::get_result_value(r),
											    lean::tactic::to_state(lean::tactic::get_result_state(r))));
	  } else {
	    return lean::optional<std::pair<lean::vm_obj, lean::tactic_state> >();
	  }
	});

  return m.ptr();
}
