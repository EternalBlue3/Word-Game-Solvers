#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>
#include <algorithm>
#include <utility>
#include <tuple>

using namespace std;

vector<string> read_gameboard() {
    try {
        ifstream file("game.txt");
        if (!file.is_open()) {
            throw runtime_error("Could not find the game file. Please create a file called \"game.txt\" in the same directory as this solver.");
        }
        vector<string> gameboard;
        string row;
        while (getline(file, row)) {
            gameboard.push_back(row);
        }
        for (string& row : gameboard) {
            for (char& c : row) {
                c = tolower(c);
            }
        }
        return gameboard;
    } catch (exception& e) {
        cerr << e.what() << endl;
        exit(1);
    }
}

std::pair<bool, tuple<int, int, int, int>> check_horizontal_vertical(std::vector<std::string>& gameboard, std::string word) {
    // Check rows
    for (int i = 0; i < gameboard.size(); i++) {
        if (gameboard[i].find(word) != std::string::npos) {
            int j = gameboard[i].find(word);
            return std::make_pair(true, make_tuple(i, j, i, j + word.length() - 1));
        } else if (gameboard[i].find(std::string(word.rbegin(), word.rend())) != std::string::npos) {
            int j = gameboard[i].find(std::string(word.rbegin(), word.rend()));
            return std::make_pair(true, make_tuple(i, j + word.length() - 1, i, j));
        }
    }

    // Check columns
    for (int j = 0; j < gameboard[0].length(); j++) {
        std::string column;
        for (int i = 0; i < gameboard.size(); i++) {
            column.push_back(gameboard[i][j]);
        }
        if (column.find(word) != std::string::npos) {
            int i = column.find(word);
            return std::make_pair(true, make_tuple(i, j, i + word.length() - 1, j));
        } else if (column.find(std::string(word.rbegin(), word.rend())) != std::string::npos) {
            int i = column.find(std::string(word.rbegin(), word.rend()));
            return std::make_pair(true, make_tuple(i + word.length() - 1, j, i, j));
        }
    }

    return std::make_pair(false, make_tuple(0, 0, 0, 0));
}

int main() {
  vector<string> gameboard = read_gameboard();
  string word;
  bool diagonal;
    
  while (true) {
      cout << "Enter word: ";
      cin >> word;
      std::transform(word.begin(), word.end(), word.begin(), [](unsigned char c) { return std::tolower(c); });
      
      if (word == "exit") {
          exit(0);
      }
      
      std::pair<bool, tuple<int, int, int, int>> output = check_horizontal_vertical(gameboard,word);
      if (output.first) {
          cout << "x: " << std::get<0>(output.second) << "  y: " << std::get<1>(output.second) << endl;
      } else {
          cout << "Word not found." << endl;
      }
  }

  return 0;
}
