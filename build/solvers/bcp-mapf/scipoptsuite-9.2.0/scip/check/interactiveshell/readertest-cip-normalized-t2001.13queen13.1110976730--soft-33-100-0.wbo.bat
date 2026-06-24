set heur emph off
read "/home/ogvruth/zhouResearchSP26/mapfdecompositiondata/solvers/bcp-mapf/scipoptsuite-9.2.0/scip"/check/"instances/PseudoBoolean/normalized-t2001.13queen13.1110976730--soft-33-100-0.wbo"
write problem temp/normalized-t2001.13queen13.1110976730--soft-33-100-0.wbo.cip
presolve
write transproblem temp/normalized-t2001.13queen13.1110976730--soft-33-100-0.wbo_trans.cip
set heur emph def
read temp/normalized-t2001.13queen13.1110976730--soft-33-100-0.wbo_trans.cip
optimize
validatesolve "4" "4"
read temp/normalized-t2001.13queen13.1110976730--soft-33-100-0.wbo.cip
optimize
validatesolve "4" "4"
quit
