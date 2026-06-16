set display verblevel 0
set timing enabled FALSE
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/Cardinality/atm_5_25_1.cip"
optimize
write statistics temp/atm_5_25_1.cip_r1.stats
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/Cardinality/atm_5_25_1.cip"
optimize
write statistics temp/atm_5_25_1.cip_r2.stats
quit
