// my_module.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "my_class.h"

namespace py = pybind11;

PYBIND11_MODULE(my_module, m) {
    m.doc() = "pybind11 example module";

    // Bindings for MyClass class
    py::class_<comm::MyClass>(m, "MyClass")
        .def(py::init<const std::string &, int>())
        .def("GetName", &comm::MyClass::GetName)
        .def("GetValue", &comm::MyClass::GetValue);

    // Binding for our new function
    m.def("deserialize_and_create_fn", &comm::deserialize_and_create_fn);
}
