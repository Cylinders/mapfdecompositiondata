set heur emph off
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/MIP/vpm2.fzn"
write problem temp/vpm2.fzn.mps
presolve
write transproblem temp/vpm2.fzn_trans.mps
set heur emph def
read temp/vpm2.fzn_trans.mps
optimize
validatesolve "13.75" "13.75"
read temp/vpm2.fzn.mps
optimize
validatesolve "13.75" "13.75"
quit
