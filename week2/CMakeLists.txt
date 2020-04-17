cmake_minimum_required(VERSION 3.10)

set (PROJ_NAME quant)
set (SRC_DIR src)
set (VENDOR_DIR vendor)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# set the project name
project(${PROJ_NAME})

# add the executable
# src
aux_source_directory("${SRC_DIR}" SRC_FILES)
# src/quant
set(QUANT_DIR ${SRC_DIR}/quant)
aux_source_directory(${QUANT_DIR} SRC_FILES)

add_executable(${PROJ_NAME} "${SRC_FILES}")

# include files
target_include_directories(${PROJ_NAME} PUBLIC "${SRC_DIR}")

target_compile_definitions(${PROJ_NAME} PUBLIC "-DDEBUG")

add_custom_command(TARGET ${PROJ_NAME}
    POST_BUILD
    COMMAND mkdir data
    COMMAND ${CMAKE_COMMAND} -E copy_directory "${CMAKE_CURRENT_SOURCE_DIR}/config" "${PROJECT_BINARY_DIR}/config"
    COMMAND ${CMAKE_COMMAND} -E copy_directory "${CMAKE_CURRENT_SOURCE_DIR}/scripts" "${PROJECT_BINARY_DIR}/scripts"
)

# set(CONFIG_DIR config)
# file(COPY "${CMAKE_CURRENT_SOURCE_DIR}/${CONFIG_DIR}" 
#     DESTINATION "${PROJECT_BINARY_DIR}"
# )


################ vendor ################

# simnow
add_subdirectory(${VENDOR_DIR}/simnow)
target_link_libraries(${PROJ_NAME} simnow_md)

# yaml-cpp
add_subdirectory(${VENDOR_DIR}/yaml-cpp)
target_link_libraries(${PROJ_NAME} yaml-cpp)

# spdlog
add_subdirectory(${VENDOR_DIR}/spdlog)
target_link_libraries(${PROJ_NAME} spdlog)

# # libuv
# set (LIBUV_DIR ${VENDOR_DIR}/libuv)
# add_subdirectory(${LIBUV_DIR})
# include_directories(${LIBUV_DIR}/libuv/include)
# target_link_libraries(${PROJ_NAME} uv)
