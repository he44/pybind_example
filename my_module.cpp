// my_module.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "my_class.h"

PYBIND11_MODULE(my_module, m) {
    m.doc() = "Pybind Example with Protobuf.";

    // Bindings for MyClass class
    pybind11::class_<example::MyClass>(m, "MyClass")
        .def(pybind11::init<const std::string &, int>())
        .def("GetName", &example::MyClass::GetName)
        .def("GetAge", &example::MyClass::GetAge);
    m.def(
        "deserialize_and_create_fn", 
        &example::deserialize_and_create_fn);
    m.def(
      "increment_age", &example::increment_age);

}
