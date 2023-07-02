#include <string>

#include <pybind11/pybind11.h>

#include "message.pb.h"

namespace example {
class MyClass {
public:
    MyClass(const std::string &name, int age) : name_(name), age_(age) {}

    std::string GetName() const { return name_; }
    int GetAge() const { return age_; }

private:
    std::string name_;
    int age_;
};

std::vector<std::string> deserialize_and_create_fn(const std::string& serialized_people);

pybind11::bytes increment_age(const std::string& serialized_people);

} // namespace example