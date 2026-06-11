#include "conflictbasedsearch.h"
#include "LowLevelSolver.h"
#include <chrono>
#include <iostream>
#include <fstream>
#include <sstream>
#include <utility>
#include <string>



namespace conflictbasedsearch {
std::vector<std::string> split(std::string s, char delim) {
    std::vector<std::string> result;
    std::stringstream ss(s);
    std::string item;

    while (getline(ss, item, delim)) {
        result.push_back(item);
    }
    return result;
}

Map readMap(std::string filename) {
    Map map; // Grid map
    int row, col;

    std::ifstream infile(filename);
    std::string line;

    getline(infile, line);

    auto splitted = split(line, ' ');
    row = std::stoi(splitted[0]);
    col = std::stoi(splitted[1]);

    getline(infile, line);

    // split second line to get obstacles
    std::istringstream k(line);
    std::string s;

    std::vector<std::vector<Cell>> cells;

    for (int i = 0; i < row; i++) {
        std::vector<Cell> row;
        for (int j = 0; j < col; j++) {
            row.emplace_back(Cell(i, j));
        }
        cells.emplace_back(row);
    };

    while (getline(k, s, ' ')) {
        int obstacleIndex = std::stoi(s);
        int x = obstacleIndex % row;
        int y = obstacleIndex / row;

        cells[x][y].isObstacle = true;
    }

    // next lines are agents. startIndex endIndex
    int start, end;
    std::vector<Agent> agents;
    int agentID = 0;

    while (infile >> start >> end) {
        int startX = start % row;
        int startY = start / row;

        int endX = end % row;
        int endY = end / row;

        Agent agent(agentID);
        agent.start = Cell(startX, startY);
        agent.end = Cell(endX, endY);

        // Console output for agent loading
        std::cout << "start: "  << startX << startY;
        std::cout << " end: " << endX << endY << "\n";

        agents.emplace_back(agent);
        agentID++;
    }

    map.cells = cells;
    map.agents = agents;
    return map;
}

Map readMapString(const std::string& mapData) {
    Map map; // Grid map
    int row, col;

    // Use istringstream to read from the passed string instead of a file
    std::istringstream infile(mapData);
    std::string line;

    getline(infile, line);

    auto splitted = split(line, ' ');
    row = std::stoi(splitted[0]);
    col = std::stoi(splitted[1]);

    getline(infile, line);

    // split second line to get obstacles
    std::istringstream k(line);
    std::string s;

    std::vector<std::vector<Cell>> cells;

    for (int i = 0; i < row; i++) {
        std::vector<Cell> rowVec; // Renamed to avoid shadowing 'int row'
        for (int j = 0; j < col; j++) {
            rowVec.emplace_back(Cell(i, j));
        }
        cells.emplace_back(rowVec);
    };

    while (getline(k, s, ' ')) {
        if (s.empty()) continue; // Safety check for extra spaces
        int obstacleIndex = std::stoi(s);
        int x = obstacleIndex % row;
        int y = obstacleIndex / row;

        cells[x][y].isObstacle = true;
    }

    // next lines are agents. startIndex endIndex
    int start, end;
    std::vector<Agent> agents;
    int agentID = 0;

    // This while loop works identically on string streams!
    while (infile >> start >> end) {
        int startX = start % row;
        int startY = start / row;

        int endX = end % row;
        int endY = end / row;

        Agent agent(agentID);
        agent.start = Cell(startX, startY);
        agent.end = Cell(endX, endY);

        // Console output for agent loading
        std::cout << "start: "  << startX << " " << startY;
        std::cout << " end: " << endX << " " << endY << "\n";

        agents.emplace_back(agent);
        agentID++;
    }

    map.cells = cells;
    map.agents = agents;
    return map;
}

void printMap(Map map) {
    for (int i = 0; i < map.cells.size(); i++) {
        for (int j = 0; j < map.cells[0].size(); j++) {
            if (map.cells[j][i].isObstacle)
                std::cout << "X";
            else
                std::cout << "_";
        }
        std::cout << std::endl;
    }
}

void printAgents(Map map) {
    for (int i = 0; i < map.agents.size(); i++) {
        std::cout << map.agents[i].start.y;
    }
}

void testLowLevel(Map map) {
    LowLevelSolver solver;
    auto x = solver.findOptimalPaths(std::vector<Constraint>(), map);

    std::cout << x.size();
    for (int i = 0; i < x.size(); i++) {
        for (int j = 0; j < x[0].size(); j++) {
            std::cout << x[i][j].x << "," << x[i][j].y << std::endl;
        }
    }
}

unsigned int Factorial(unsigned int number) {
    return number <= 1 ? number : Factorial(number - 1)*number;
}

void printSolution(std::vector<std::vector<Cell>> optimalPaths) {
    for (auto path : optimalPaths) {
        std::cout << "Optimal path of agent \n";
        for (auto cell : path) {
            std::cout << cell.x << cell.y << "\n";
        }
    }
}

// The new callable function that replaces main()
std::vector<std::vector<std::string>> solveCBS(const std::string& filename, bool verbose) {
    auto started = std::chrono::high_resolution_clock::now();

    Map map = readMap(filename);

    if (verbose) {
        printMap(map);
    }

    HighLevelSolver solver;
    std::vector<std::vector<Cell>> optimalPaths = solver.solve(map);

    if (verbose) {
        printSolution(optimalPaths);
        auto done = std::chrono::high_resolution_clock::now();
        auto elapsedTime = std::chrono::duration_cast<std::chrono::milliseconds>(done-started).count();
        std::cout << elapsedTime << " milliseconds\n";
    }

		// pass in the cells as a list of tuples.

		std::vector<std::vector<std::vector<int>>> efficientPaths;

		for (const auto& path : optimalPaths) {
	    	std::vector<std::pair<int, int>> currentPathCoords;
	    	for (const auto& cell : path) {
	        	currentPathCoords.push_back({cell.x, cell.y}); // Syntax is identical!
	    	}
	    efficientPaths.push_back(currentPathCoords);
		}

		return efficientPaths;

		// return optimalPaths (convert this into a string);
}}
