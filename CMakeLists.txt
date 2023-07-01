# CMakeLists.txt
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
cmake_minimum_required(VERSION 3.5)
project(my_module)

# Find required protobuf package
 
set(Protobuf_DIR, "/opt/homebrew/Cellar/protobuf/23.3/lib/cmake/protobuf")
find_package(Protobuf REQUIRED)

message(STATUS "Adding protobuf include directory ${PROTOBUF_INCLUDE_DIRS}")
include_directories(${PROTOBUF_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_BINARY_DIR})

# Protobuf file generation
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS message.proto)

set(PROTO_PY message_pb2.py)
add_custom_command(
    OUTPUT ${PROTO_PY}
    COMMAND ${PROTOBUF_PROTOC_EXECUTABLE} --python_out=${CMAKE_CURRENT_BINARY_DIR} -I${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/message.proto
    DEPENDS ${PROTO_HDRS}
)

find_package(pybind11 REQUIRED)

add_library(my_module MODULE my_class.cpp my_module.cpp ${PROTO_SRCS} ${PROTO_HDRS})

target_link_libraries(my_module PRIVATE pybind11::module ${PROTOBUF_LIBRARIES})

set_target_properties(my_module PROPERTIES PREFIX "${PYTHON_MODULE_PREFIX}"
                                           SUFFIX "${PYTHON_MODULE_EXTENSION}")

add_custom_target(protobuf_python ALL DEPENDS ${PROTO_PY})