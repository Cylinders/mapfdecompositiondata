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
    Instance instance(mapFilePath, scenFilePath, 200   , "", 0, 0, 0, 0);
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
    

    // Return a summary string based on the result
    if (cbs.solution_found) {
        return cbs.writePaths();
    } else {
        return "fail";
    }
}


// ALGORITHM 2: CBSH:

string algorithmTwo(const string& mapFilePath, const string& scenFilePath) {
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
    Instance instance(mapFilePath, scenFilePath, 2100, "", 0, 0, 0, 0);
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


// ALGORITHM 3: BCP

string algorithmThree(const string& input) {
    // TODO: Implement your third string logic here
    return "Result 3: " + input;
}

// ALGORITHM 3: MDD SAT

string algorithmFour(const string& input) {
    string s_arg0 = "MyApp";
    string s_arg1 = "--input-file=" + input;
    string s_arg2 = "--output-file=my_output.txt"; 

    char* args[] = { &s_arg0[0], &s_arg1[0], &s_arg2[0] };

    return "Result 4: " + sReloc::MDDSATSolver(3, args);
}
// --- File Reading Function ---

string readMapAndScenFiles(const string& mapFilePath, const string& scenFilePath) {
    ifstream mapStream(mapFilePath);
    ifstream scenStream(scenFilePath);
    ostringstream outData;

    if (!mapStream.is_open()) {
        cerr << "Error: Could not open .map file at " << mapFilePath << "\n";
        return "";
    }
    if (!scenStream.is_open()) {
        cerr << "Error: Could not open .scen file at " << scenFilePath << "\n";
        return "";
    }

    // ---------------------------------------------------------
    // 1. Process the .map file (Extract grid and build Nodes)
    // ---------------------------------------------------------
    string line;
    int height = 0, width = 0;
    
    // Read the Moving AI header (type, height, width, map)
    while (getline(mapStream, line)) {
        if (line.find("height") != string::npos) sscanf(line.c_str(), "height %d", &height);
        else if (line.find("width") != string::npos) sscanf(line.c_str(), "width %d", &width);
        else if (line.find("map") != string::npos) break; // Grid layout starts immediately after this
    }

    vector<string> grid(height);
    // This array maps raw map coordinates (Y * Width + X) to our sequential solver IDs
    vector<int> dense_ids(height * width, -1); 
    int current_vertex_id = 0;

    for (int y = 0; y < height; ++y) {
        getline(mapStream, grid[y]);
        for (int x = 0; x < width; ++x) {
            char c = grid[y][x];
            // Moving AI uses '.' or 'G' for passable terrain. '@', 'T', 'O' are walls.
            if (c == '.' || c == 'G' || c == 'S') {
                dense_ids[y * width + x] = current_vertex_id++;
            }
        }
    }
    mapStream.close();
    cout << "Successfully processed .map file. Walkable nodes: " << current_vertex_id << "\n";

    // ---------------------------------------------------------
    // 2. Process the .scen file (Extract start and goal locations)
    // ---------------------------------------------------------
    // We create a temporary list to hold the robot data for each node
    struct VertexData {
        int init_robot = 0;
        int goal_robot = 0;
    };
    vector<VertexData> solver_nodes(current_vertex_id);
    
    int robot_id = 1; // Solver expects robots to be 1-indexed (ID > 0)

    while (getline(scenStream, line)) {
        // Skip empty lines or the "version 1" header
        if (line.empty() || line.find("version") != string::npos) continue;

        istringstream iss(line);
        string bucket, map_name;
        int mw, mh, sx, sy, gx, gy;
        double dist;

        // Moving AI format: bucket map_name w h start_x start_y goal_x goal_y optimal_length
        if (iss >> bucket >> map_name >> mw >> mh >> sx >> sy >> gx >> gy >> dist) {
            int start_dense_id = dense_ids[sy * width + sx];
            int goal_dense_id  = dense_ids[gy * width + gx];

            // Only assign if both the start and goal are actually on walkable tiles
            if (start_dense_id != -1 && goal_dense_id != -1) {
                solver_nodes[start_dense_id].init_robot = robot_id;
                solver_nodes[goal_dense_id].goal_robot = robot_id;
                robot_id++;
            }
        }
    }
    scenStream.close();
    cout << "Successfully processed .scen file. Active Robots: " << (robot_id - 1) << "\n";

    // ---------------------------------------------------------
    // 3. Construct the Unified Matrix String
    // ---------------------------------------------------------
    outData << "V =\n";
    for (int v = 0; v < current_vertex_id; ++v) {
        // Format: (vertex_id:cycle_id)[init_robot:ignored:goal_robot]
        // We set cycle_id and the dummy variable to 0
        outData << "(" << v << ":0)[" 
                << solver_nodes[v].init_robot << ":0:" 
                << solver_nodes[v].goal_robot << "]\n";
    }

    outData << "E =\n";
    // Iterate the grid to generate the paths (Edges)
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            int u = dense_ids[y * width + x];
            if (u == -1) continue; // Skip walls

            // Check Right Neighbor (4-way movement)
            if (x + 1 < width && dense_ids[y * width + (x + 1)] != -1) {
                int v = dense_ids[y * width + (x + 1)];
                outData << "{" << u << "," << v << "}\n";
            }
            // Check Down Neighbor (4-way movement)
            if (y + 1 < height && dense_ids[(y + 1) * width + x] != -1) {
                int v = dense_ids[(y + 1) * width + x];
                outData << "{" << u << "," << v << "}\n";
            }
        }
    }

    return outData.str();
}




int main(int argc, char* argv[]) {
    cout << "--- Testing String Functions & CBSH ---\n";


    string mapFile = "../originalmaps/lak103d.map";
    string scenFile = "../originalscen/lak103d.map.scen";
    string myInput = "PathfindingTest";
    //cout << readMapAndScenFiles(mapFile, scenFile);

    // Now algorithmOne takes the two file paths!
    // cout << algorithmOne(mapFile, scenFile) << "\n";

    // cout << algorithmTwo(myInput) << "\n";
    //  cout << algorithmThree(myInput) << "\n";
    cout << algorithmFour(readMapAndScenFiles(mapFile, scenFile)) << "\n";

    cout << "\n--- Testing File Reader ---\n";
    

    return 0;
}
