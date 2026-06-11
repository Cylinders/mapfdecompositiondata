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
# LIBRARY 2: ConflictBasedSearch
# =======================================================
# Define the path to the new solver
set(CBS_DIR "solvers/ConflictBasedSearch") 

# Grab all the .cpp files (notice there is no /src/ folder here)
file(GLOB CBS_SOURCES "${CBS_DIR}/*.cpp")

# Exclude their main.cpp so it doesn't conflict with yours
list(REMOVE_ITEM CBS_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/${CBS_DIR}/main.cpp")

# Create the library
add_library(CBS_Library STATIC ${CBS_SOURCES})

# Include headers (they are in the exact same folder as the source code)
target_include_directories(CBS_Library PUBLIC ${CBS_DIR})

# =======================================================
# YOUR MAIN APPLICATION
# =======================================================
# Build your executable
add_executable(MyApp src/main.cpp)

# Link BOTH libraries to your app
target_link_libraries(MyApp PRIVATE CBSH2_Library CBS_Library)