#include "my_class.h"

#include <string>
#include <vector>

#include <pybind11/pybind11.h>

#include "message.pb.h"

namespace example {
std::vector<std::string> deserialize_and_create_fn(const std::string& serialized_people) {
  People people;
  people.ParseFromString(serialized_people);

  std::vector<std::string> result;
  result.reserve(people.person_size());
  for (const auto& person : people.person()) {
    result.emplace_back(person.name());
  }
  return result;
}

pybind11::bytes increment_age(const std::string& serialized_people) {
  People people;
  if (!people.ParseFromString(serialized_people)) {
    return pybind11::bytes("");
  }
  for (auto& person : *people.mutable_person()) {
    person.set_age(person.age() + 1);
  }
  std::string output;
  output.reserve(serialized_people.size());
  return pybind11::bytes(people.SerializeAsString());
}

} // namespace example
