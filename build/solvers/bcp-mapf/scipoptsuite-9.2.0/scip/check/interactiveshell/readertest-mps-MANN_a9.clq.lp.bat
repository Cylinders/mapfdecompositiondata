set heur emph off
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/MIP/MANN_a9.clq.lp"
write problem temp/MANN_a9.clq.lp.mps
presolve
write transproblem temp/MANN_a9.clq.lp_trans.mps
set heur emph def
read temp/MANN_a9.clq.lp_trans.mps
optimize
validatesolve "16" "16"
read temp/MANN_a9.clq.lp.mps
optimize
validatesolve "16" "16"
quit
