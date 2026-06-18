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

#include "problem/output.h"
#include "problem/includes.h"
#include "problem/problem.h"
#include "problem/variable_data.h"
#include <string> // Required for std::string

std::string write_best_solution(
    SCIP* scip    // SCIP
)
{
    // Check.
    debug_assert(scip);

    // Get problem data.
    auto probdata = SCIPgetProbData(scip);
    const auto N = SCIPprobdataGetN(probdata);

    // Get variables.
    const auto& dummy_vars = SCIPprobdataGetDummyVars(probdata);
    const auto& agent_vars = SCIPprobdataGetAgentVars(probdata);

    // Get best solution.
    auto sol = SCIPgetBestSol(scip);
    SCIP_Real obj = 0;
    
    if (!sol)
    {
        return "-\n";
    }

    // Exit if no solution within objective limit is found.
    obj = SCIPgetSolOrigObj(scip, sol);
    if (obj >= ARTIFICIAL_VAR_COST)
    {
        return "-\n";
    }

    // Note: This helper function might still print to standard output internally.
    print_used_paths(scip, sol);

    // Check if dummy variables are used.
    for (Agent a = 0; a < N; ++a)
    {
        // Get the variable.
        auto var = dummy_vars[a];
        debug_assert(var);
        debug_assert(!SCIPvarGetData(var));

        // Check.
        const auto var_val = SCIPgetSolVal(scip, sol, var);
        if (SCIPisPositive(scip, var_val))
        {
            return "-\n";
        }
    }

    // Initialize the output string with the objective value.
    std::string output_str = fmt::format("{:.0f}\n\n", SCIPround(scip, obj));

    // Append paths to the string.
    for (Agent a = 0; a < N; ++a)
    {
        bool found = false;
        for (const auto& [var, _] : agent_vars[a])
        {
            debug_assert(var);

            // Write the path.
            const auto var_val = SCIPgetSolVal(scip, sol, var);
            if (SCIPisPositive(scip, var_val))
            {
                // Get the path.
                auto vardata = SCIPvarGetData(var);
                const auto path_length = SCIPvardataGetPathLength(vardata);
                const auto path = SCIPvardataGetPath(vardata);

                // Append the specific agent's path to our string.
                output_str += fmt::format("Agent {}, cost {:.0f}, path {}\n",
                                          a,
                                          SCIPround(scip, SCIPvarGetObj(var)),
                                          format_path(probdata, path_length, path));

                // Move to next agent.
                release_assert(!found, "Agent {} is using more than one path", a);
                found = true;
                break;
            }
        }
        release_assert(found, "Agent {} has no path in the solution", a);
    }

    // Return the final formatted string.
    return output_str;
}