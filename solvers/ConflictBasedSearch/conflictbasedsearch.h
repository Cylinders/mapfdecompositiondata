#pragma once

#include <vector>
#include <string>
#include "HighLevelSolver.h" // Ensures Map and Cell are recognized

// Executes the Conflict-Based Search.
// Set verbose to true if you want to print the map and execution time to the console.

namespace conflictbasedsearch {
std::vector<std::vector<string>> solveCBS(const std::string& filename, bool verbose = false);}
