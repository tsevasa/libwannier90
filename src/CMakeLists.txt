cmake_minimum_required(VERSION 3.12)
project(libwannier90)

# Set the relative path to the wannier90 directory
set(W90DIR ../wannier90-3.1.0)

# Find LAPACK and BLAS libraries (not using pkg-config)
find_library(LAPACK_LIBRARY NAMES lapack PATHS /opt/homebrew/opt/lapack/lib)
find_library(BLAS_LIBRARY NAMES blas PATHS /opt/homebrew/opt/lapack/lib)

# Find Pybind11 package
find_package(pybind11 REQUIRED)

# Find Python
find_package(Python REQUIRED COMPONENTS Interpreter Development)

# Use g++ as the C++ compiler
set(CMAKE_CXX_COMPILER g++)

# Compiler settings
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -Wall -std=c++11 -fPIC -D_UF")

# Add source files
add_library(libwannier90 MODULE libwannier90.cpp)

# Link LAPACK and BLAS libraries
target_link_libraries(libwannier90 PRIVATE ${LAPACK_LIBRARY} ${BLAS_LIBRARY})

# Link the libwannier.a library with the relative path
target_link_libraries(libwannier90 PRIVATE ${CMAKE_SOURCE_DIR}/${W90DIR}/libwannier.a)

# Link with Python libraries
target_link_libraries(libwannier90 PRIVATE Python::Python)

# Set the output file name and extension
set_target_properties(libwannier90 PROPERTIES PREFIX "")
set_target_properties(libwannier90 PROPERTIES SUFFIX ${PYTHON_MODULE_EXTENSION})

# Include Pybind11 headers
target_include_directories(libwannier90 PRIVATE ${pybind11_INCLUDE_DIR})

# Include Python headers
target_include_directories(libwannier90 PRIVATE ${Python_INCLUDE_DIRS})

# Use -dynamiclib on macOS
if(APPLE)
  set_target_properties(libwannier90 PROPERTIES SUFFIX .so)
  set_target_properties(libwannier90 PROPERTIES LINK_FLAGS "-Wl,-undefined,dynamic_lookup")
endif()
