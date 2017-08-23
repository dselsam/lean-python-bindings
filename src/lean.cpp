#include <pybind11/pybind11.h>
#include "util/name.h"

namespace py = pybind11;


PYBIND11_PLUGIN(lean) {
  py::module m("lean", "pybind11 lean plugin");

  py::class_<lean::name>(m, "name")
    .def(py::init<>())
    .def(py::init<std::string>())
    .def(py::init<lean::name const &, char const *>())
    .def(py::init<lean::name const &, unsigned>())
    //    .def("to_string", (std::string (lean::name::*)(char const *)) &lean::name::to_string, "to_string", py::arg("sep") = lean::lean_name_separator)
    .def("to_string", &lean::name::to_string, py::arg("sep") = lean::lean_name_separator)
  ;
  
  return m.ptr();
}
