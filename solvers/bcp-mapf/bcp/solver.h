/*
This file is part of BCP-MAPF.

BCP-MAPF is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BCP-MAPF is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BCP-MAPF.  If not, see <https://www.gnu.org/licenses/>.

Author: Edward Lam <ed@ed-lam.com>
*/

#ifndef BCP_MAPF_SOLVER_H
#define BCP_MAPF_SOLVER_H

#include <string>
#include <utility>
#include "scip/scip.h"

/**
 * @brief Initializes and runs the BCP-MAPF SCIP solver.
 * @param argc Number of shell parameters
 * @param argv Array with shell parameters
 * @return std::pair<SCIP_RETCODE, std::string> A pair containing the SCIP return code and the output solution string.
 */
std::pair<SCIP_RETCODE, std::string> start_solver(int argc, char** argv);

/**
 * @brief Runs the solver and directly returns the best solution string.
 * @param argc Number of shell parameters
 * @param argv Array with shell parameters
 * @return std::string The output solution string.
 */
std::string returnSol(int argc, char** argv);

#endif // BCP_MAPF_SOLVER_H