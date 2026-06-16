if(NOT TARGET libsoplex)
  include("${CMAKE_CURRENT_LIST_DIR}/soplex-targets.cmake")
endif()

set(SOPLEX_LIBRARIES libsoplex)
set(SOPLEX_PIC_LIBRARIES libsoplex-pic)
set(SOPLEX_INCLUDE_DIRS "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/soplex/src;/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/build/solvers/bcp-mapf/scipoptsuite-9.2.0/soplex")
set(SOPLEX_FOUND TRUE)

if(on)
  find_package(Boost 1.65.0)
  include_directories(${Boost_INCLUDE_DIRS})
endif()

if(off)
  set(SOPLEX_WITH_PAPILO TRUE)
endif()
