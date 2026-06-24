# CMake generated Testfile for 
# Source directory: /home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/examples/Queens
# Build directory: /home/ogvruth/zhouResearchSP26/mapfdecompositiondata/build/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/examples/Queens
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(examples-queens-build "/usr/bin/cmake" "--build" "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/build" "--config" "Release" "--target" "queens")
set_tests_properties(examples-queens-build PROPERTIES  RESOURCE_LOCK "libscip" _BACKTRACE_TRIPLES "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/examples/Queens/CMakeLists.txt;28;add_test;/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/examples/Queens/CMakeLists.txt;0;")
add_test(examples-queens-1 "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/build/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/bin/examples/queens" "1")
set_tests_properties(examples-queens-1 PROPERTIES  DEPENDS "examples-queens-build" _BACKTRACE_TRIPLES "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/examples/Queens/CMakeLists.txt;52;add_test;/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/examples/Queens/CMakeLists.txt;0;")
add_test(examples-queens-2 "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/build/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/bin/examples/queens" "2")
set_tests_properties(examples-queens-2 PROPERTIES  DEPENDS "examples-queens-build" _BACKTRACE_TRIPLES "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/examples/Queens/CMakeLists.txt;52;add_test;/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/examples/Queens/CMakeLists.txt;0;")
add_test(examples-queens-4 "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/build/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/bin/examples/queens" "4")
set_tests_properties(examples-queens-4 PROPERTIES  DEPENDS "examples-queens-build" _BACKTRACE_TRIPLES "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/examples/Queens/CMakeLists.txt;52;add_test;/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/examples/Queens/CMakeLists.txt;0;")
add_test(examples-queens-8 "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/build/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/bin/examples/queens" "8")
set_tests_properties(examples-queens-8 PROPERTIES  DEPENDS "examples-queens-build" _BACKTRACE_TRIPLES "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/examples/Queens/CMakeLists.txt;52;add_test;/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/examples/Queens/CMakeLists.txt;0;")
add_test(examples-queens-16 "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/build/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/bin/examples/queens" "16")
set_tests_properties(examples-queens-16 PROPERTIES  DEPENDS "examples-queens-build" _BACKTRACE_TRIPLES "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/examples/Queens/CMakeLists.txt;52;add_test;/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip/examples/Queens/CMakeLists.txt;0;")
