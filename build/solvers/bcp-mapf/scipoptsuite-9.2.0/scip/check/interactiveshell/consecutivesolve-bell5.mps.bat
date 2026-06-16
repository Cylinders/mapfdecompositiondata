set display verblevel 0
set timing enabled FALSE
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/MIP/bell5.mps"
optimize
write statistics temp/bell5.mps_r1.stats
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/MIP/bell5.mps"
optimize
write statistics temp/bell5.mps_r2.stats
quit
