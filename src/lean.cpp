#include <boost/python.hpp>

#include "util/name.h"

using namespace boost::python;

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(lean_name_to_string_overloads, lean::name::to_string, 0, 1)

BOOST_PYTHON_MODULE(lean) {
  class_<lean::name>("name", init<>())
    .def(init<std::string>())
    .def(init<lean::name const &, char const *>())
    .def(init<lean::name const &, unsigned>())

    .def("to_string", &lean::name::to_string, lean_name_to_string_overloads())
    ;
}



