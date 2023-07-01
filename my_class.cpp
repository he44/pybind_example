#include "my_class.h"

#include <string>
#include <vector>

#include "message.pb.h"

namespace comm {
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
} // namespace comm
