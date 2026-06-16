set heur emph off
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/PseudoBoolean/wheel010.lap.opb.pre.cip"
write problem temp/wheel010.lap.opb.pre.cip.cip
presolve
write transproblem temp/wheel010.lap.opb.pre.cip_trans.cip
set heur emph def
read temp/wheel010.lap.opb.pre.cip_trans.cip
optimize
validatesolve "25" "25"
read temp/wheel010.lap.opb.pre.cip.cip
optimize
validatesolve "25" "25"
quit
