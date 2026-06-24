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
    outData << mapStream.rdbuf();
    outData << scenStream.rdbuf();
    mapStream.close();
    scenStream.close();
    cout << outData.str(); 
    return outData.str();
}

int main(int argc, char* argv[]) {
    cout << "--- Testing String Functions & CBSH ---\n";


    string mapFile = "../originalmaps/lak103d.map";
    string scenFile = "../originalscen/lak103d.map.scen";
    string myInput = "PathfindingTest";
    // cout << readMapAndScenFiles(mapFile, scenFile);

    // Now algorithmOne takes the two file paths!
    //cout << algorithmOne(mapFile, scenFile) << "\n";

    //cout << algorithmTwo(mapFile, scenFile) << "\n";
    //cout << algorithmThree("../solvers/bcp-mapf/instances/warehouse_extended/10x30-w5-0.scen") << "\n";
    
    cout << algorithmFour(readMapAndScenFiles(mapFile, scenFile)) << "\n";

    

    return 0;
}
