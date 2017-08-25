cmake_minimum_required(VERSION 2.8.12)
project(leanpy)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake")

find_package(PythonLibsNew REQUIRED)

# TODO(pcm): Make a pkg-config script for Lean and replace the path.
include_directories(/usr/local/include/lean_ext/)

add_subdirectory(pybind11)
pybind11_add_module(lean lean/lean.cpp)

# TODO(pcm): Make a pkg-config script for Lean and replace the path.
if (APPLE)
  target_link_libraries(lean PRIVATE /usr/local/lib/libleanshared.dylib)
else()
  target_link_libraries(lean PRIVATE /usr/local/lib/libleanshared.so)
endif()
