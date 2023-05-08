cmake_minimum_required(VERSION 3.10)

project(ExampleInterface)

find_package(nlohmann_json REQUIRED)

# Some system may inject Python headers via Toolchain file
if(NOT PythonLibs_FOUND)
    find_package(PythonLibs REQUIRED)
endif()

find_package(PythonInterp)
find_package(Python)

# add_custom_command(
#     TARGET Module
#     PRE_BUILD # Call this command pre-build
#     COMMAND ${PYTHON_EXECUTABLE} ../../easy_extension.py ../ExampleInterface.hpp > ../ExampleInterfaceModule.cpp
#     COMMENT "Generate Module"
# )

# add_custom_command(OUTPUT "../ExampleInterfaceModule.cpp"
#     COMMAND "${PYTHON_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/../easy_extension.py" ExampleInterface.hpp > ExampleInterfaceModule.cpp)

# execute_process(COMMAND ${PYTHON_EXECUTABLE} ../../easy_extension.py ../ExampleInterface.hpp > ../ExampleInterfaceModule.cpp)

add_custom_command(OUTPUT ../ExampleInterfaceModule.cpp
    COMMAND ${PYTHON_EXECUTABLE} ../../easy_extension.py ../ExampleInterface.hpp > ../ExampleInterfaceModule.cpp
    VERBATIM # optional
)

# file(GLOB_RECURSE TEST_SRCS ExampleInterfaceModule.cpp)

include_directories(example ${PYTHON_INCLUDE_DIRS})

add_library(ExampleInterface SHARED ../ExampleInterfaceModule.cpp)



target_link_libraries(ExampleInterface ${PYTHON_LIBRARIES} nlohmann_json::nlohmann_json)

set_target_properties(
    ExampleInterface
        PROPERTIES
        PREFIX ""
        OUTPUT_NAME "ExampleInterface"
        LINKER_LANGUAGE CXX
    )