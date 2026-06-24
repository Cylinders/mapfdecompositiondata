set heur emph off
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/MIP/Negated.cip"
write problem temp/Negated.cip.opb
presolve
write transproblem temp/Negated.cip_trans.opb
set heur emph def
read temp/Negated.cip_trans.opb
optimize
validatesolve "1" "1"
read temp/Negated.cip.opb
optimize
validatesolve "1" "1"
quit
