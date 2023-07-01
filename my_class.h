#include <string>

#include "message.pb.h"

namespace comm {
class MyClass {
public:
    MyClass(const std::string &name, int value) : name_(name), value_(value) {}

    std::string GetName() const { return name_; }
    int GetValue() const { return value_; }

private:
    std::string name_;
    int value_;
};

std::vector<std::string> deserialize_and_create_fn(const std::string& serialized_people);

}