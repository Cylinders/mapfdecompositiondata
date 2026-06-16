set heur emph off
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/MIP/MANN_a9.clq.lp"
write problem temp/MANN_a9.clq.lp.cip
presolve
write transproblem temp/MANN_a9.clq.lp_trans.cip
set heur emph def
read temp/MANN_a9.clq.lp_trans.cip
optimize
validatesolve "16" "16"
read temp/MANN_a9.clq.lp.cip
optimize
validatesolve "16" "16"
quit
