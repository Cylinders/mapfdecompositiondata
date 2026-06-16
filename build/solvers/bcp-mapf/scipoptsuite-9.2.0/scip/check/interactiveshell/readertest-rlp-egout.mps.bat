set heur emph off
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/MIP/egout.mps"
write problem temp/egout.mps.rlp
presolve
write transproblem temp/egout.mps_trans.rlp
set heur emph def
read temp/egout.mps_trans.rlp
optimize
validatesolve "568.1007" "568.1007"
read temp/egout.mps.rlp
optimize
validatesolve "568.1007" "568.1007"
quit
