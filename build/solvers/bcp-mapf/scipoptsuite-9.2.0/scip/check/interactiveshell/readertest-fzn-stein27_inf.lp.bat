set heur emph off
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/MIP/stein27_inf.lp"
write problem temp/stein27_inf.lp.fzn
presolve
write transproblem temp/stein27_inf.lp_trans.fzn
set heur emph def
read temp/stein27_inf.lp_trans.fzn
optimize
validatesolve "+infinity" "+infinity"
read temp/stein27_inf.lp.fzn
optimize
validatesolve "+infinity" "+infinity"
quit
