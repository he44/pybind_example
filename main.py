import random
import string
import sys
import time
import os

build_dir = os.path.abspath("build")
sys.path.append(build_dir)

import my_module
import message_pb2

def get_random_word(length):
  return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def get_random_id():
  return random.randint(0, 10000)

def generate_serialized_bytes():
  # Create a People instance
  people = message_pb2.People()

  # Add a Person to the People instance
  person = people.person.add()
  person.name = "John Doe"
  person.age = 1234

  for i in range(99):
    person = people.person.add()
    person.name = get_random_word(random.randint(4, 10))
    person.age = get_random_id()

  # generate a random name-like string
  # Serialize to a string
  serialized_people = people.SerializeToString()
  return people, serialized_people


def try_pybind():
  # Create an instance of MyClass
  my_class = my_module.MyClass("MyName", 42)

  # Call functions
  print(my_class.GetName())
  print(my_class.GetAge())


def test_deserialize_performance():
  # Assume serialized_people is a serialized string of your protobuf message
  # You might get this from reading a file, over the network, etc.
  _, serialized_people = generate_serialized_bytes()

  num_iters = 100000
  # Using Python API
  print(' ------------- Using Python API now -------------')
  tic = time.time()
  for _ in range(num_iters):
    people = message_pb2.People()
    people.ParseFromString(serialized_people)
    python_names = []
    for person in people.person:
      python_names.append(person.name)
  toc = time.time()
  print('Using Python API for {} iterations took {:.3f} seconds'.format(num_iters, toc-tic))

  # Here
  print(' ------------- Using pybind now -------------')
  # Call the function that deserializes and creates MyClass instances

  # Now people is a list of MyClass instances
  tic = time.time()
  for _ in range(num_iters):
    pybind_names = my_module.deserialize_and_create_fn(serialized_people)
  toc = time.time()
  print('Using pybind for {} iterations took {:.3f} seconds'.format(num_iters, toc-tic))

  print('Conformance test: ', pybind_names == python_names)


def test_modification_performance():
  original_people, serialized_people = generate_serialized_bytes()
  num_iters = 100000

  tic = time.time()
  for i in range(num_iters):
    serialized_modified_people = my_module.increment_age(serialized_people)
  toc = time.time()
  print('Using pybind to modify for {} iterations took {:.3f} seconds'.format(num_iters, toc-tic))

  modified_people = message_pb2.People() 
  modified_people.ParseFromString(serialized_modified_people)

  for op, mp in zip(original_people.person, modified_people.person):
    assert op.name == mp.name, 'Pybind Conformance test failed: name changed'
    assert op.age + 1 == mp.age, 'Pybind Conformance test failed: age not incremented'
  print('Pybind Conformance test: ', True)

  tic = time.time()
  for i in range(num_iters):
    modified_people = message_pb2.People() 
    modified_people.ParseFromString(serialized_people)
    for person in modified_people.person:
      person.age += 1
    serialized_modified_people = modified_people.SerializeToString()
  toc = time.time()
  print('Using Python API to modify for {} iterations took {:.3f} seconds'.format(num_iters, toc-tic))

  modified_people = message_pb2.People() 
  modified_people.ParseFromString(serialized_modified_people)
  for op, mp in zip(original_people.person, modified_people.person):
    assert op.name == mp.name, 'Python API Conformance test failed: name changed'
    assert op.age + 1 == mp.age, 'Python API Conformance test failed: age not incremented'
  print('Python API Conformance test: ', True)

def main():
  # try_pybind() 
  # test_deserialize_performance()
  test_modification_performance()

if __name__ == "__main__":
  main()
