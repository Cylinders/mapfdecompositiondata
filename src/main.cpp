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
#include "conflictbasedsearch.h"
// --- String Processing Functions ---

//ALGORITHM ONE: CBS
using namespace std;

string algorithmOne(const string& mapFilePath, const string& scenFilePath) {
    // --- CBSH ---
    // You can easily change your heuristics and other parameters right here!

    string chosenHeuristic = "WDG";         // Options: "Zero", "CG", "DG", "WDG"
    string chosenRectReasoning = "GR";      // Options: "None", "R", "RM", "GR", "Disjoint"
    string chosenCorridorReasoning = "GC";  // Options: "None", "C", "PC", "STC", "GC", "Disjoint"

    // Other solver configurations
    int agentNum = 0;            // 0 reads all agents from the file
    double cutoffTime = 60.0;    // seconds
    int screenOption = 1;        // 0: none, 1: results, 2: all
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
    Instance instance(mapFilePath, scenFilePath, agentNum, "", 0, 0, 0, 0);
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

    // Return a summary string based on the result
    if (cbs.solution_found) {
        return "CBSH Result: Success! Solved in " + to_string(runtime) + " seconds.";
    } else {
        return "CBSH Result: Failed to find a solution within " + to_string(cutoffTime) + " seconds.";
    }
}


// ALGORITHM 2: CBSH:

string algorithmTwo(const string& input) {
    // TODO: Implement your second string logic here
		conflictbasedsearch::solveCBS()
    return "Result 2: " + input;
}


// ALGORITHM 3: BCP

string algorithmThree(const string& input) {
    // TODO: Implement your third string logic here
    return "Result 3: " + input;
}

// ALGORITHM 3: MDD SAT

string algorithmFour(const string& input) {
    // TODO: Implement your fourth string logic here
    return "Result 4: " + input;
}

// --- File Reading Function ---

void readMapAndScenFiles(const string& mapFilePath, const string& scenFilePath) {
    ifstream mapStream(mapFilePath);
    ifstream scenStream(scenFilePath);

    // 1. Process the .map file
    if (mapStream.is_open()) {
        cout << "Successfully opened .map file: " << mapFilePath << "\n";
        string line;

        // Read line by line
        while (getline(mapStream, line)) {
            // TODO: Parse the map grid/headers here
        }
        mapStream.close();
    } else {
        cerr << "Error: Could not open .map file at " << mapFilePath << "\n";
    }

    // 2. Process the .scen file
    if (scenStream.is_open()) {
        cout << "Successfully opened .scen file: " << scenFilePath << "\n";
        string line;

        // Read line by line
        while (getline(scenStream, line)) {
            // TODO: Parse the scenario data
        }
        scenStream.close();
    } else {
        cerr << "Error: Could not open .scen file at " << scenFilePath << "\n";
    }
}

// --- Main Execution ---

int main(int argc, char* argv[]) {
    cout << "--- Testing String Functions & CBSH ---\n


    // Replace these strings with your actual local file paths
    string mapFile = "test_grid.map";
    string scenFile = "test_grid.scen";
    string myInput = "PathfindingTest";

    // Now algorithmOne takes the two file paths!
    cout << algorithmOne(mapFile, scenFile) << "\n";

    cout << algorithmTwo(myInput) << "\n";
    cout << algorithmThree(myInput) << "\n";
    cout << algorithmFour(myInput) << "\n";

    cout << "\n--- Testing File Reader ---\n";
    readMapAndScenFiles(mapFile, scenFile);

    return 0;
}
