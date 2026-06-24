cmake_minimum_required(VERSION 3.21)
project(MyMAPFProject VERSION 1.0)

# =======================================================
# GLOBAL SETTINGS
# =======================================================
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Set C version
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED 1)

# Set C++ version
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED 1)

# Set release build default
if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif ()

# Find Boost WITH the specific components required by CBSH2
find_package(Boost REQUIRED COMPONENTS program_options system filesystem)

# Link to math library globally
find_library(LIBM m)
if (NOT LIBM)
    set(LIBM "")
endif ()

# =======================================================
# LIBRARY 1: BCP-MAPF (Branch-Cut-and-Price)
# =======================================================
set(BCP_DIR "solvers/bcp-mapf")

set(BCP_MAPF_SOURCE_FILES
    ${BCP_DIR}/bcp/branching/branching_rule.cpp
    ${BCP_DIR}/bcp/branching/fractional.cpp
    ${BCP_DIR}/bcp/branching/length_branching_constraint.cpp
    ${BCP_DIR}/bcp/branching/pseudosolution.cpp
    ${BCP_DIR}/bcp/branching/vertex_branching_constraint.cpp
    ${BCP_DIR}/bcp/constraints/agent_wait_edge.cpp
    ${BCP_DIR}/bcp/constraints/corridor.cpp
    ${BCP_DIR}/bcp/constraints/edgetime.cpp
    ${BCP_DIR}/bcp/constraints/exit_entry.cpp
    ${BCP_DIR}/bcp/constraints/five_edge.cpp
    ${BCP_DIR}/bcp/constraints/four_edge.cpp
    ${BCP_DIR}/bcp/constraints/nodetime.cpp
    ${BCP_DIR}/bcp/constraints/preprocessing.cpp
    ${BCP_DIR}/bcp/constraints/rectangle_knapsack.cpp
    ${BCP_DIR}/bcp/constraints/rectangle.cpp
    ${BCP_DIR}/bcp/constraints/six_edge.cpp
    ${BCP_DIR}/bcp/constraints/step_aside.cpp
    ${BCP_DIR}/bcp/constraints/target.cpp
    ${BCP_DIR}/bcp/constraints/three_vertex.cpp
    ${BCP_DIR}/bcp/constraints/two_edge.cpp
    ${BCP_DIR}/bcp/constraints/two_vertex.cpp
    ${BCP_DIR}/bcp/constraints/vertex_four_edge.cpp
    ${BCP_DIR}/bcp/constraints/wait_delay.cpp
    ${BCP_DIR}/bcp/heuristics/prioritized_planning.cpp
    ${BCP_DIR}/bcp/solver.cpp
    ${BCP_DIR}/bcp/pricing/astar.cpp
    ${BCP_DIR}/bcp/pricing/distance_heuristic.cpp
    ${BCP_DIR}/bcp/pricing/pricer.cpp
    ${BCP_DIR}/bcp/problem/instance.cpp
    ${BCP_DIR}/bcp/problem/map.cpp
    ${BCP_DIR}/bcp/problem/output.cpp
    ${BCP_DIR}/bcp/problem/problem.cpp
    ${BCP_DIR}/bcp/problem/reader.cpp
    ${BCP_DIR}/bcp/problem/variable_data.cpp
    ${BCP_DIR}/bcp/types/memory_pool.cpp
)

add_library(BCP_MAPF_Library STATIC ${BCP_MAPF_SOURCE_FILES})
target_include_directories(BCP_MAPF_Library PUBLIC ${BCP_DIR}/ ${BCP_DIR}/bcp/)

# Include SCIP binaries
find_path(SCIP_INCLUDE_DIR
          NAMES scip/scip.h
          HINTS "${SCIP_DIR}/scip/src" "$ENV{SCIP_DIR}/scip/src")
find_path(SCIP_CONFIG_DIR
          NAMES scip/config.h
          HINTS "${SCIP_DIR}/build/scip" "$ENV{SCIP_DIR}/build/scip")
find_library(SCIP_LIBRARY
             NAMES scip
             HINTS "${SCIP_DIR}/build/lib" "$ENV{SCIP_DIR}/build/lib")

if (SCIP_INCLUDE_DIR AND SCIP_CONFIG_DIR AND SCIP_LIBRARY)
    target_include_directories(BCP_MAPF_Library PUBLIC ${SCIP_INCLUDE_DIR} ${SCIP_CONFIG_DIR})
    message("Using SCIP binary at ${SCIP_LIBRARY}")
else ()
    # Include Gurobi
    find_path(GUROBI_INCLUDE_DIRS
        NAMES gurobi_c.h
        HINTS "${GUROBI_DIR}/include" "${GUROBI_DIR}/*/include" "$ENV{GUROBI_DIR}/include" "$ENV{GUROBI_DIR}/*/include" "$ENV{GUROBI_HOME}/include")
    find_library(GUROBI_LIBRARY
        NAMES gurobi120 gurobi110 gurobi100 gurobi95 gurobi91 gurobi90 gurobi81 gurobi80 gurobi75 gurobi70
        HINTS "${GUROBI_DIR}/lib" "${GUROBI_DIR}/*/lib" "$ENV{GUROBI_DIR}/lib" "$ENV{GUROBI_DIR}/*/lib" "$ENV{GUROBI_HOME}/lib")
    
    if (GUROBI_INCLUDE_DIRS AND GUROBI_LIBRARY)
        set(LPS grb CACHE STRING "options for LP solver")
        target_include_directories(BCP_MAPF_Library PUBLIC ${GUROBI_INCLUDE_DIRS})
        message("Using Gurobi at ${GUROBI_LIBRARY} as LP solver")
    endif ()

    # Include CPLEX (Fallback if Gurobi is not found)
    if (NOT GUROBI_INCLUDE_DIRS OR NOT GUROBI_LIBRARY)
        find_path(CPLEX_INCLUDE_DIR
            NAMES cplex.h
            HINTS "${CPLEX_DIR}/include/ilcplex" "$ENV{CPLEX_DIR}/include/ilcplex")
        find_library(CPLEX_LIBRARY
            NAMES cplex
            HINTS "${CPLEX_DIR}/lib/*/static_pic" "$ENV{CPLEX_DIR}/lib/*/static_pic")
        if (CPLEX_INCLUDE_DIR AND CPLEX_LIBRARY)
            set(LPS cpx CACHE STRING "options for LP solver")
            target_include_directories(BCP_MAPF_Library PUBLIC ${CPLEX_INCLUDE_DIR})
            message("Using CPLEX at ${CPLEX_LIBRARY} as LP solver")
        endif ()
    endif ()

    # Include SoPlex (Fallback if neither Gurobi nor CPLEX are found)
    if ((NOT GUROBI_INCLUDE_DIRS OR NOT GUROBI_LIBRARY) AND (NOT CPLEX_INCLUDE_DIR OR NOT CPLEX_LIBRARY))
        set(LPS spx CACHE STRING "options for LP solver")
        set(CONF_INCLUDE_DIRS ../soplex/src/)
        configure_file(${BCP_DIR}/scipoptsuite-9.2.0/soplex/soplex-config.cmake.in
                       "${CMAKE_BINARY_DIR}/soplex/soplex-config.cmake"
                       @ONLY)
        set(SOPLEX_DIR ${CMAKE_BINARY_DIR}/soplex)
        add_subdirectory(${BCP_DIR}/scipoptsuite-9.2.0/soplex/ EXCLUDE_FROM_ALL)
        message("Using SoPlex as LP solver ${SOPLEX_INCLUDE_DIRS}")
    endif ()

    # Include SCIP compilation
    set(WITH_SCIPDEF on)
    set(TPI none)
    set(tpisources tpi/tpi_none.c)
    set(THREAD_LIBRARIES "")
    set(TPI_NONE on)
    set(GMP off)
    set(IPOPT off)
    set(PAPILO off)
    set(ZIMPL off)
    configure_file(${BCP_DIR}/scipoptsuite-9.2.0/scip/src/scip/config.h.in "${CMAKE_BINARY_DIR}/scip/config.h" @ONLY)
    target_include_directories(BCP_MAPF_Library PUBLIC ${CMAKE_BINARY_DIR})
    
    if (${CMAKE_SYSTEM_NAME} MATCHES "Linux")
        set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -ldl")
    endif ()
    
    add_subdirectory(${BCP_DIR}/scipoptsuite-9.2.0/scip/ EXCLUDE_FROM_ALL)
    target_include_directories(BCP_MAPF_Library PRIVATE ${BCP_DIR}/scipoptsuite-9.2.0/scip/src/
                                                SYSTEM INTERFACE ${BCP_DIR}/scipoptsuite-9.2.0/scip/src/)
    set(SCIP_LIBRARY libscip)
endif ()

## Fetch Boost headers (if custom download is still desired for bcp-mapf)
#set(BOOST_VERSION 1.87.0)
#message(STATUS "Downloading Boost libraries for BCP-MAPF")
#include(FetchContent)
#FetchContent_Declare(boost
#    URL https://github.com/boostorg/boost/releases/download/boost-${BOOST_VERSION}/boost-${BOOST_VERSION}-b2-nodocs.tar.gz
#    DOWNLOAD_EXTRACT_TIMESTAMP TRUE)
#FetchContent_MakeAvailable(boost)
#set(BOOST_FETCH_INCLUDE_DIR "${boost_SOURCE_DIR}")
#message("Downloaded Custom Boost to ${boost_SOURCE_DIR}")

# BCP-MAPF specific libraries/includes
add_subdirectory(${BCP_DIR}/fmt EXCLUDE_FROM_ALL)
target_include_directories(BCP_MAPF_Library PUBLIC ${BCP_DIR}/fmt/include/)
target_include_directories(BCP_MAPF_Library PUBLIC ${BCP_DIR}/cxxopts/include/)
target_include_directories(BCP_MAPF_Library PUBLIC ${BCP_DIR}/robin-hood-hashing/src/include/)
target_include_directories(BCP_MAPF_Library PUBLIC ${Boost_INCLUDE_DIRS})

target_link_libraries(BCP_MAPF_Library PUBLIC
        Boost::headers
        fmt::fmt-header-only
        ${SCIP_LIBRARY}
        ${LIBM}
)
# BCP-MAPF Compile Options
target_compile_options(BCP_MAPF_Library PRIVATE 
    -DUSE_RESERVATION_TABLE -DUSE_ASTAR_SOLUTION_CACHING
    -DUSE_WAITEDGE_CONFLICTS -DUSE_RECTANGLE_KNAPSACK_CONFLICTS
    -DUSE_CORRIDOR_CONFLICTS -DUSE_WAITCORRIDOR_CONFLICTS
    -DUSE_WAITDELAY_CONFLICTS -DUSE_EXITENTRY_CONFLICTS
    -DUSE_TWOEDGE_CONFLICTS -DUSE_WAITTWOEDGE_CONFLICTS
    -DUSE_AGENTWAITEDGE_CONFLICTS -DUSE_GOAL_CONFLICTS
    -DUSE_BEST_FIRST_NODE_SELECTION
    -Wall -Wextra -Wignored-qualifiers -Werror=return-type -Wno-sign-compare
)

check_cxx_compiler_flag("-march=native" MARCH_NATIVE)
if (MARCH_NATIVE)
    target_compile_options(BCP_MAPF_Library PRIVATE -march=native)
endif ()

if (CMAKE_BUILD_TYPE STREQUAL "Debug")
    target_compile_options(BCP_MAPF_Library PRIVATE -DDEBUG -D_GLIBCXX_DEBUG)
    message("Compiled in debug mode")
elseif (CMAKE_BUILD_TYPE STREQUAL "RelWithDebInfo")
    target_compile_options(BCP_MAPF_Library PRIVATE -Og -DNDEBUG -funroll-loops -fstrict-aliasing)
    message("Compiled in release with debug info mode")
else ()
    target_compile_options(BCP_MAPF_Library PRIVATE -O3 -DNDEBUG -funroll-loops -fstrict-aliasing)
    message("Compiled in release mode")
endif ()

if (${CMAKE_SYSTEM_NAME} MATCHES "Linux")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -flto")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -flto")
endif ()


# =======================================================
# LIBRARY 2: CBSH2-RTC
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
# LIBRARY 3: reLOC (MDDSAT)
# =======================================================
set(MDDSAT "solvers/MDDSAT") 
file(GLOB MDDSAT_SOURCES "${MDDSAT}/src/*.cpp")
message(STATUS "MDDSAT Sources found: ${MDDSAT_SOURCES}")
add_library(MDDSAT_Library STATIC ${MDDSAT_SOURCES})


# =======================================================
# MAIN APPLICATION
# =======================================================

add_library(mapf-solvers STATIC
        src/api.cpp
)

target_link_libraries(mapf-solvers PUBLIC
        BCP_MAPF_Library
        CBSH2_Library
        MDDSAT_Library
)

target_include_directories(mapf-solvers
        PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/solvers/MDDSAT/src"
)

option(MAPF_BUILD_APP "standalone app" OFF)

if (MAPF_BUILD_APP)
    add_executable(MyApp src/main.cpp)
    target_link_libraries(MyApp PRIVATE
            BCP_MAPF_Library
            CBSH2_Library
            MDDSAT_Library
    )
    target_include_directories(MyApp PRIVATE
            "${CMAKE_CURRENT_SOURCE_DIR}/solvers/MDDSAT/src"
    )
endif()

