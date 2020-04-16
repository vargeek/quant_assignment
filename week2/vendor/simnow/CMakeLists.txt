find_library(SIMNOW_MD_PATH
    NAMES thostmduserapi_se.so
    HINTS ${CMAKE_CURRENT_SOURCE_DIR}
)

add_library(simnow_md SHARED IMPORTED GLOBAL)
set_property(TARGET simnow_md 
    PROPERTY IMPORTED_LOCATION ${SIMNOW_MD_PATH}
)
target_include_directories(simnow_md 
    INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
)
