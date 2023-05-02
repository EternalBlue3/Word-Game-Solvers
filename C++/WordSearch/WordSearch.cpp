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
            return std::make_pair(true, make_tuple(i, j, i, j + word.length() - 1));
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
            return std::make_pair(true, make_tuple(i, j, i + word.length() - 1, j));
        }
    }

    return std::make_pair(false, make_tuple(0, 0, 0, 0));
}

void print_board(vector<string>& gameboard, vector<int>& coords, string& word) {
    const string RED = "\033[31m";  // red text color
    const string END = "\033[0m";     // end color
    
    cout << "\n\"" << word << "\" found at: (" << coords[0] << "," << coords[1] << ") to (" << coords[2] << "," << coords[3] << ")\n";
    cout << "   ";
    for (int i = 0; i < gameboard[0].size(); i++) {
        cout << i % 10 << " ";
    }
    cout << endl;
    for (int i = 0; i < gameboard.size(); i++) {
        cout << i << "  ";
        for (int j = 0; j < gameboard[i].size(); j++) {
            if (coords[0] <= i && i <= coords[2] && coords[1] <= j && j <= coords[3]) {
                cout << RED << gameboard[i][j] << END << " ";
            } else {
                cout << gameboard[i][j] << " ";
            }
        }
        cout << endl;
    }
    cout << endl;
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
          vector<int> coordinates{std::get<0>(output.second),std::get<1>(output.second),std::get<2>(output.second),std::get<3>(output.second)};
          print_board(gameboard,coordinates,word);
      } else {
          cout << "Word not found." << "\n\n";
      }
  }

  return 0;
}
