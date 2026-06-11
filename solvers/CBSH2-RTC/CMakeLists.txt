cmake_minimum_required (VERSION 3.5)
project(cbs)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "RELEASE")
endif()

# 1. Use Boost_ (Title Case) for all input variables!
set(BOOST_ROOT "C:/local/boost_1_82_0")

# 2. Set the library dir. 
set(BOOST_LIBRARYDIR "${Boost_ROOT}/lib64-msvc-14.3") 

# 3. Tell CMake NOT to search standard system paths
set(BOOST_NO_SYSTEM_PATHS ON)

# --- THE BULLETPROOF WINDOWS FIX ---
set(BOOST_USE_STATIC_LIBS ON) 
add_compile_definitions(BOOST_ALL_NO_LIB) # (This one stays all caps because it's a C++ macro, not a CMake variable!)
# -----------------------------------

# 4. The package name MUST be Title Case
find_package(Boost 1.66.0 REQUIRED COMPONENTS program_options system filesystem)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")

# Add your executable
file(GLOB SOURCES "src/*.cpp")
add_executable(cbs ${SOURCES})

# 5. The output variables from CMake are also Title Case
target_include_directories(cbs PRIVATE "inc" ${Boost_INCLUDE_DIRS})

# 6. Link using ONLY the classic Boost variables.
target_link_libraries(cbs PRIVATE ${Boost_LIBRARIES})