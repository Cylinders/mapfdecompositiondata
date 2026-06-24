set display verblevel 0
set timing enabled FALSE
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/PseudoBoolean/normalized-bsg_10_4_5.opb"
optimize
write statistics temp/normalized-bsg_10_4_5.opb_r1.stats
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/PseudoBoolean/normalized-bsg_10_4_5.opb"
optimize
write statistics temp/normalized-bsg_10_4_5.opb_r2.stats
quit
