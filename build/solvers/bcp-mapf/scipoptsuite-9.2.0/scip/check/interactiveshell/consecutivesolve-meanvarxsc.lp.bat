set display verblevel 0
set timing enabled FALSE
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/MINLP/meanvarxsc.lp"
optimize
write statistics temp/meanvarxsc.lp_r1.stats
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/MINLP/meanvarxsc.lp"
optimize
write statistics temp/meanvarxsc.lp_r2.stats
quit
