set display verblevel 0
set timing enabled FALSE
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/MIP/stein27.fzn"
optimize
write statistics temp/stein27.fzn_r1.stats
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/MIP/stein27.fzn"
optimize
write statistics temp/stein27.fzn_r2.stats
quit
