#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <span>

using namespace std;

/*
function generateScenes
return type: void
parameters:
selector: int pass-by-reference
selector = 0:
selector = 1:
selector = 2:
selector = 3:

*/

/*
void processData(const std::string& myString, int myInteger, const std::vector<float>& myFloatList) {

    // Example: Reading the data
    std::cout << "String: " << myString << "\n";
    std::cout << "Integer: " << myInteger << "\n";
    std::cout << "First float in list: " << myFloatList[0] << "\n";

    // Return void just means we don't need a 'return' statement at the end
}
*/

// Calculate Standard Deviation of ROD


vector<vector<string>> read2DVector(const std::string& filepath) {
    ifstream file(filepath);
    vector<vector<string>> data2D;
    string currentLine;

    if (!file.is_open()) {
        cerr << "Error: Could not open the file at " << filepath << std::endl;
        return data2D;
    }

    while (getline(file, currentLine)) {
        vector<string> row;
        stringstream ss(currentLine);
        string item;

        while (ss >> item) {
            row.push_back(item);
        }

        data2D.push_back(row);
    }

    file.close();
    return data2D;
}

float calculateROD(const vector<vector<string>>& data) {
    int numRows = data.size();      // No dereferencing needed

    if (numRows > 0) {
        string firstElement = data[0][0]; // Standard access
    }

    return 0.0f;
}
float calculateSDROD(const std::string& input) {
	vector<vector<string>> original = read2DVector(input);
	string type = original[0][1];
	int height = stoi(original[1][1]);
  int width = stoi(original[2][1]);




}




int main(int argc, char* argv[]) {
    if (argc <= 1) {
        std::cout << "No additional command-line arguments provided." << std::endl;
        std::cout << "Program name: " << argv[0] << std::endl;
        return 0;
    }

    std::cout << "Number of arguments passed: " << (argc - 1) << std::endl;
    std::cout << "---" << std::endl;

    for (int i = 0; i < argc; ++i) {
        std::cout << "Argument " << i << ": " << argv[i] << std::endl;
    }

    return 0;
}
