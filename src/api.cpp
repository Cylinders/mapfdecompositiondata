#include <iostream>
#include <string>
#include <fstream>
#include <vector>

// Make sure you include the necessary headers for your CBS implementation!
//#include "CBSHeuristic.h"
#include "CBS.h"
// #include "Instance.h"
#include <boost/program_options.hpp>
#include <boost/tokenizer.hpp>
//#include "conflictbasedsearch.h"
// --- String Processing Functions ---

#include <stdio.h>
#include <stdlib.h>
#include <sys/times.h>
#include <unistd.h>

#include "config.h"
#include "compile.h"
#include "defs.h"
#include "reloc.h"
#include "multirobot.h"
#include "compress.h"
#include "statistics.h"
#include "version.h"
#include "search.h"

#include "solver_main.h"
#include "solver.h"

using namespace std;

//ALGORITHM ONE: CBS
bool algorithmOne(const string &mapFilePath, const string &scenFilePath, int n) {
    // --- CBSH ---
    // You can easily change your heuristics and other parameters right here!

    string chosenHeuristic = "Zero";         // Options: "Zero", "CG", "DG", "WDG"
    string chosenRectReasoning = "None";      // Options: "None", "R", "RM", "GR", "Disjoint"
    string chosenCorridorReasoning = "None";  // Options: "None", "C", "PC", "STC", "GC", "Disjoint"

    // Other solver configurations
    int agentNum = 0;            // 0 reads all agents from the file
    double cutoffTime = 60.0;    // seconds
    int screenOption = 0;        // 0: none, 1: results, 2: all
    int seed = 0;
    int restartRuns = 1;
    bool usingSipp = false;

    // 1. Check and assign heuristics
    heuristics_type h;
    if (chosenHeuristic == "Zero") h = heuristics_type::ZERO;
    else if (chosenHeuristic == "CG") h = heuristics_type::CG;
    else if (chosenHeuristic == "DG") h = heuristics_type::DG;
    else if (chosenHeuristic == "WDG") h = heuristics_type::WDG;
    else return "Error: WRONG heuristics strategy!";

    // 2. Check and assign rectangle reasoning
    rectangle_strategy r;
    if (chosenRectReasoning == "None") r = rectangle_strategy::NR;
    else if (chosenRectReasoning == "R") r = rectangle_strategy::R;
    else if (chosenRectReasoning == "RM") r = rectangle_strategy::RM;
    else if (chosenRectReasoning == "GR") r = rectangle_strategy::GR;
    else if (chosenRectReasoning == "Disjoint") r = rectangle_strategy::DR;
    else return "Error: WRONG rectangle reasoning strategy!";

    // 3. Check and assign corridor reasoning
    corridor_strategy c;
    if (chosenCorridorReasoning == "None") c = corridor_strategy::NC;
    else if (chosenCorridorReasoning == "C") c = corridor_strategy::C;
    else if (chosenCorridorReasoning == "PC") c = corridor_strategy::PC;
    else if (chosenCorridorReasoning == "STC") c = corridor_strategy::STC;
    else if (chosenCorridorReasoning == "GC") c = corridor_strategy::GC;
    else if (chosenCorridorReasoning == "Disjoint") c = corridor_strategy::DC;
    else return "Error: WRONG corridor reasoning strategy!";

    // --- Load the Instance ---
    // Assuming constructor matches: (map_file, agents_file, num_agents, agent_indices, rows, cols, obs, warehouse_width)
    Instance instance(mapFilePath, scenFilePath, n, "", 0, 0, 0, 0);
    srand(seed);

    // --- Initialize the Solver ---
    CBS cbs(instance, usingSipp, screenOption);
    cbs.setPrioritizeConflicts(true);
    cbs.setDisjointSplitting(false);
    cbs.setBypass(true);
    cbs.setRectangleReasoning(r);
    cbs.setCorridorReasoning(c);
    cbs.setHeuristicType(h);
    cbs.setTargetReasoning(true);
    cbs.setMutexReasoning(false);
    cbs.setSavingStats(false);
    // cbs.setNodeLimit(MAX_NODES); // Uncomment if MAX_NODES is defined in your headers

    // --- Run CBS ---
    double runtime = 0;
    int min_f_val = 0;
    for (int i = 0; i < restartRuns; i++) {
        cbs.clear();
        cbs.solve(cutoffTime, min_f_val);
        runtime += cbs.runtime;
        if (cbs.solution_found) break;
        min_f_val = (int) cbs.min_f_val;
        cbs.randomRoot = true;
    }
    cout << cbs.writePaths();
    cbs.runtime = runtime;
    if (cbs.solution_found) {
        cout << "CBSH Result: Success! Solved in " + to_string(runtime) + " seconds.";
    } else {
        cout << "CBSH Result: Failed to find a solution within " + to_string(cutoffTime) + " seconds.";
    }
    cbs.clearSearchEngines();

    return cbs.solution_found;

    // // Return a summary string based on the result
    // if (cbs.solution_found) {
    //     return cbs.writePaths();
    // } else {
    //     return "fail";
    // }
}


// ALGORITHM 2: CBSH:

bool algorithmTwo(const string &mapFilePath, const string &scenFilePath, int n) {
    // --- CBSH ---
    // You can easily change your heuristics and other parameters right here!

    string chosenHeuristic = "WDG";         // Options: "Zero", "CG", "DG", "WDG"
    string chosenRectReasoning = "GR";      // Options: "None", "R", "RM", "GR", "Disjoint"
    string chosenCorridorReasoning = "GC";  // Options: "None", "C", "PC", "STC", "GC", "Disjoint"

    // Other solver configurations
    int agentNum = 0;            // 0 reads all agents from the file
    double cutoffTime = 60.0;    // seconds
    int screenOption = 0;        // 0: none, 1: results, 2: all
    int seed = 0;
    int restartRuns = 1;
    bool usingSipp = false;

    // 1. Check and assign heuristics
    heuristics_type h;
    if (chosenHeuristic == "Zero") h = heuristics_type::ZERO;
    else if (chosenHeuristic == "CG") h = heuristics_type::CG;
    else if (chosenHeuristic == "DG") h = heuristics_type::DG;
    else if (chosenHeuristic == "WDG") h = heuristics_type::WDG;
    else return "Error: WRONG heuristics strategy!";

    // 2. Check and assign rectangle reasoning
    rectangle_strategy r;
    if (chosenRectReasoning == "None") r = rectangle_strategy::NR;
    else if (chosenRectReasoning == "R") r = rectangle_strategy::R;
    else if (chosenRectReasoning == "RM") r = rectangle_strategy::RM;
    else if (chosenRectReasoning == "GR") r = rectangle_strategy::GR;
    else if (chosenRectReasoning == "Disjoint") r = rectangle_strategy::DR;
    else return "Error: WRONG rectangle reasoning strategy!";

    // 3. Check and assign corridor reasoning
    corridor_strategy c;
    if (chosenCorridorReasoning == "None") c = corridor_strategy::NC;
    else if (chosenCorridorReasoning == "C") c = corridor_strategy::C;
    else if (chosenCorridorReasoning == "PC") c = corridor_strategy::PC;
    else if (chosenCorridorReasoning == "STC") c = corridor_strategy::STC;
    else if (chosenCorridorReasoning == "GC") c = corridor_strategy::GC;
    else if (chosenCorridorReasoning == "Disjoint") c = corridor_strategy::DC;
    else return "Error: WRONG corridor reasoning strategy!";

    // --- Load the Instance ---
    // Assuming constructor matches: (map_file, agents_file, num_agents, agent_indices, rows, cols, obs, warehouse_width)
    Instance instance(mapFilePath, scenFilePath, n, "", 0, 0, 0, 0);
    srand(seed);

    // --- Initialize the Solver ---
    CBS cbs(instance, usingSipp, screenOption);
    cbs.setPrioritizeConflicts(true);
    cbs.setDisjointSplitting(false);
    cbs.setBypass(true);
    cbs.setRectangleReasoning(r);
    cbs.setCorridorReasoning(c);
    cbs.setHeuristicType(h);
    cbs.setTargetReasoning(true);
    cbs.setMutexReasoning(false);
    cbs.setSavingStats(false);
    // cbs.setNodeLimit(MAX_NODES); // Uncomment if MAX_NODES is defined in your headers

    // --- Run CBS ---
    double runtime = 0;
    int min_f_val = 0;
    for (int i = 0; i < restartRuns; i++) {
        cbs.clear();
        cbs.solve(cutoffTime, min_f_val);
        runtime += cbs.runtime;
        if (cbs.solution_found) break;
        min_f_val = (int) cbs.min_f_val;
        cbs.randomRoot = true;
    }
    cbs.runtime = runtime;
    cbs.clearSearchEngines();

    return cbs.solution_found;

    // // Return a summary string based on the result
    // if (cbs.solution_found) {
    //     return "CBSH Result: Success! Solved in " + to_string(runtime) + " seconds.";
    // } else {
    //     return "CBSH Result: Failed to find a solution within " + to_string(cutoffTime) + " seconds.";
    // }
}


// ALGORITHM 3: BCP

std::string algorithmThree(const int t, const std::string& input) {
    // 1. Setup the fake command line arguments
    std::string programName = "bcp-mapf"; // Dummy program name (equivalent to argv[0])
    std::string time_limit = "--time-limit="+std::to_string(t);

    // Create mutable char buffers for the arguments
    std::vector<char> arg0(programName.begin(), programName.end());
    arg0.push_back('\0'); // Null-terminate

    std::vector<char> arg1(time_limit.begin(), time_limit.end());
    arg1.push_back('\0'); // Null-terminate

    std::vector<char> arg2(input.begin(), input.end());
    arg2.push_back('\0'); // Null-terminate

    // 2. Build the argv array
    std::vector<char*> argv_vec;
    argv_vec.push_back(arg0.data()); // argv[0]
    argv_vec.push_back(arg1.data()); // argv[1]
    argv_vec.push_back(arg2.data()); // argv[1]
    argv_vec.push_back(nullptr);     // POSIX standard expects argv to be null-terminated

    int argc = 3;
    char** argv = argv_vec.data();

    // 3. Call your solver
    return returnSol(argc, argv);

}

// ALGORITHM 3: MDD SAT

string algorithmFour(const string& input) {
    string s_arg0 = "MyApp";
    string s_arg1 = "--input-file=" + input;
    string s_arg2 = "--output-file=my_output.txt";

    char* args[] = { &s_arg0[0], &s_arg1[0], &s_arg2[0] };

    return "Result 4: " + sReloc::MDDSATSolver(3, args);
}