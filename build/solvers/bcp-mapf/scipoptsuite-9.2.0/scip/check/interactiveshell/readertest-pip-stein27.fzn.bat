set heur emph off
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/MIP/stein27.fzn"
write problem temp/stein27.fzn.pip
presolve
write transproblem temp/stein27.fzn_trans.pip
set heur emph def
read temp/stein27.fzn_trans.pip
optimize
validatesolve "18" "18"
read temp/stein27.fzn.pip
optimize
validatesolve "18" "18"
quit
