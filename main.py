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

def generate_serizlied_bytes():
  # Create a People instance
  people = message_pb2.People()

  # Add a Person to the People instance
  person = people.person.add()
  person.name = "John Doe"
  person.id = 1234

  for i in range(99):
    person = people.person.add()
    person.name = get_random_word(random.randint(4, 10))
    person.id = get_random_id()

  # generate a random name-like string
  # Serialize to a string
  serialized_people = people.SerializeToString()
  return serialized_people


def try_pybind():
  # Create an instance of MyClass
  my_class = my_module.MyClass("MyName", 42)

  # Call functions
  print(my_class.GetName())
  print(my_class.GetValue())

  # Assume serialized_people is a serialized string of your protobuf message
  # You might get this from reading a file, over the network, etc.
  serialized_people = generate_serizlied_bytes()

  num_iters = 100000

  # Using Python API
  print(' ------------- Uisng Python API now -------------')
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
  print(' ------------- Uisng pybind now -------------')
  # Call the function that deserializes and creates MyClass instances

  # Now people is a list of MyClass instances
  tic = time.time()
  for _ in range(num_iters):
    pybind_names = my_module.deserialize_and_create_fn(serialized_people)
  toc = time.time()
  print('Using pybind for {} iterations took {:.3f} seconds'.format(num_iters, toc-tic))

  print(pybind_names == python_names)

def main():
  generate_serizlied_bytes()
  try_pybind() 

if __name__ == "__main__":
  main()
