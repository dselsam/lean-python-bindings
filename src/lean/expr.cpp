#include <boost/python.hpp>

#include "api/lean_macros.h"
#include "api/lean_bool.h"
#include "api/lean_exception.h"
#include "api/lean_name.h"
#include "api/lean_options.h"
#include "api/lean_univ.h"
#include "api/lean_expr.h"

using namespace boost::python;

BOOST_PYTHON_MODULE(expr) {
  def("lean_expr_mk_var", lean_expr_mk_var);
  /*
  def("lean_expr_mk_sort", lean_expr_mk_sort);
  def("lean_expr_mk_const", lean_expr_mk_const);
  def("lean_expr_mk_app", lean_expr_mk_app);
  def("to_binder_info", to_binder_info);
  def("of_binder_info", of_binder_info);
  def("lean_expr_mk_lambda", lean_expr_mk_lambda);
  def("lean_expr_mk_pi", lean_expr_mk_pi);
  def("lean_expr_mk_macro", lean_expr_mk_macro);
  def("lean_expr_mk_local", lean_expr_mk_local);
  def("lean_expr_mk_local_ext", lean_expr_mk_local_ext);
  def("lean_expr_mk_metavar", lean_expr_mk_metavar);
  def("lean_expr_to_string", lean_expr_to_string);
  def("lean_expr_del", lean_expr_del);
  def("lean_macro_def_del", lean_macro_def_del);
  def("lean_macro_def_eq", lean_macro_def_eq);
  def("lean_macro_def_to_string", lean_macro_def_to_string);
  def("lean_expr_get_kind", lean_expr_get_kind);
  def("lean_expr_eq", lean_expr_eq);
  def("lean_expr_lt", lean_expr_lt);
  def("lean_expr_quick_lt", lean_expr_quick_lt);
  def("check_expr_kind", check_expr_kind);
  def("lean_expr_get_var_idx", lean_expr_get_var_idx);
  def("lean_expr_get_sort_univ", lean_expr_get_sort_univ);
  def("check_constant", check_constant);
  def("lean_expr_get_const_name", lean_expr_get_const_name);
  def("lean_expr_get_const_univs", lean_expr_get_const_univs);
  def("check_app", check_app);
  def("lean_expr_get_app_fun", lean_expr_get_app_fun);
  def("lean_expr_get_app_arg", lean_expr_get_app_arg);
  def("check_mlocal", check_mlocal);
  def("check_local", check_local);
  def("lean_expr_get_mlocal_name", lean_expr_get_mlocal_name);
  def("lean_expr_get_mlocal_type", lean_expr_get_mlocal_type);
  def("lean_expr_get_local_pp_name", lean_expr_get_local_pp_name);
  def("lean_expr_get_local_binder_kind", lean_expr_get_local_binder_kind);
  def("check_binding", check_binding);
  def("lean_expr_get_binding_name", lean_expr_get_binding_name);
  def("lean_expr_get_binding_domain", lean_expr_get_binding_domain);
  def("lean_expr_get_binding_body", lean_expr_get_binding_body);
  def("lean_expr_get_binding_binder_kind", lean_expr_get_binding_binder_kind);
  def("check_macro", check_macro);
  def("lean_expr_get_macro_def", lean_expr_get_macro_def);
  def("lean_expr_get_macro_args", lean_expr_get_macro_args);
  def("lean_list_expr_mk_nil", lean_list_expr_mk_nil);
  def("lean_list_expr_mk_cons", lean_list_expr_mk_cons);
  def("lean_list_expr_del", lean_list_expr_del);
  def("lean_list_expr_is_cons", lean_list_expr_is_cons);
  def("lean_list_expr_eq", lean_list_expr_eq);
  def("lean_list_expr_head", lean_list_expr_head);
  def("lean_list_expr_tail", lean_list_expr_tail);
  */
}
