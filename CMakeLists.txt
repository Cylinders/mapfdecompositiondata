cmake_minimum_required(VERSION 3.10)
project(MyMAPFProject VERSION 1.0)

# C++17 is fine!
set(CMAKE_CXX_STANDARD 17)

# 1. Find Boost WITH the specific components
find_package(Boost REQUIRED COMPONENTS program_options system filesystem)

# =======================================================
# LIBRARY 1: CBSH2-RTC
# =======================================================
set(CBSH2_DIR "solvers/CBSH2-RTC") 
file(GLOB CBSH2_SOURCES "${CBSH2_DIR}/src/*.cpp")
list(REMOVE_ITEM CBSH2_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/${CBSH2_DIR}/src/driver.cpp")

add_library(CBSH2_Library STATIC ${CBSH2_SOURCES})
target_include_directories(CBSH2_Library PUBLIC 
    ${CBSH2_DIR}/inc 
    ${Boost_INCLUDE_DIRS}
)
target_link_libraries(CBSH2_Library PUBLIC ${Boost_LIBRARIES})

# =======================================================
# YOUR MAIN APPLICATION
# =======================================================
# Build your executable
add_executable(MyApp src/main.cpp)

# Link BOTH libraries to your app
target_link_libraries(MyApp PRIVATE CBSH2_Library)