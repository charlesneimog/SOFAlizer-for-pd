# Define your standard CMake header (for example):
cmake_minimum_required(VERSION 3.15)
set(CMAKE_SUPPRESS_REGENERATION true)
include(${CMAKE_CURRENT_SOURCE_DIR}/pd.build/pd.cmake)
project(SOFAlizer)
set_pd_external_path(${CMAKE_CURRENT_SOURCE_DIR}/${project_name})

# Lib Sofa
set(BUILD_TESTS OFF)
set(BUILD_SHARED_LIBS OFF)
set(BUILD_STATIC_LIBS ON)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/libmysofa/)
set_target_properties(mysofa-static PROPERTIES POSITION_INDEPENDENT_CODE ON)

# Pd Object
set(SOURCES_DIR ${CMAKE_SOURCE_DIR}/src)
file(GLOB SOURCES ${SOURCES_DIR}/*.c)
add_pd_external(SOFAlizer_tilde SOFAlizer~ ${SOURCES})

target_link_libraries(SOFAlizer_tilde PRIVATE mysofa-static)



