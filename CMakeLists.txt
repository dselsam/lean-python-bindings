cmake_minimum_required(VERSION 2.8.12)
project(leanpy)

# TODO(pcm): Make a pkg-config script for Lean and replace the path.
include_directories(/usr/local/include/lean_ext/)

add_subdirectory(pybind11)
pybind11_add_module(lean src/lean.cpp)

# TODO(pcm): Make a pkg-config script for Lean and replace the path.
target_link_libraries(lean PRIVATE /usr/local/lib/libleanshared.so)
