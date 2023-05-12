#include <iostream>
#include <fstream>
#include <vector>
#include <utility>
#include <chrono>
#include <set>
#include <algorithm>

using namespace std;

vector<string> read_gameboard() {
    vector<string> gameboard;
    ifstream f("game.txt");
    if (f.is_open()) {
        string row;
        while (getline(f, row)) {
            gameboard.push_back(row);
        }
    } else {
        cerr << "Could not find the game file. Please create a file called \"game.txt\" in the same directory as this solver." << endl;
        exit(1);
    }
    f.close();
    for (int i = 0; i < gameboard.size(); i++) {
        for (int j = 0; j < gameboard[i].size(); j++) {
            gameboard[i][j] = tolower(gameboard[i][j]);
        }
    }
    return gameboard;
}

vector<pair<int, int>> check_dir(const vector<string>& gameboard, const string& word, const pair<int, int>& direction, const int& lengthx, const int& lengthy) {
    int dx = direction.first, dy = direction.second;
    vector<pair<int, int>> coords;
    for (int y = 0; y < lengthy; y++) {
        for (int x = 0; x < lengthx; x++) {
            bool match = true;
            for (int i = 0; i < word.length(); i++) {
                int xi = x + i * dx, yi = y + i * dy;
                if (!(0 <= xi && xi < lengthx && 0 <= yi && yi < lengthy) || gameboard[yi][xi] != word[i]) {
                    match = false;
                    break;
                }
            }
            if (match) {
                for (int i = 0; i < word.length(); i++) {
                    int xi = x + i * dx, yi = y + i * dy;
                    coords.push_back({xi, yi});
                }
                return coords;
            }
        }
    }
    return {};
}

pair<bool, vector<pair<int, int>>> find_word(const vector<string>& gameboard, const string& word) {
    vector<pair<int, int>> dirs = {{-1,-1},{-1,0},{-1,1},{0,-1},{0,1},{1,-1},{1,0},{1,1}};
    int lengthx = gameboard[0].length(), lengthy = gameboard.size();
    for (auto direction : dirs) {
        vector<pair<int, int>> coords = check_dir(gameboard, word, direction, lengthx, lengthy);
        if (!coords.empty()) {
            return {true, coords};
        }
    }
    return {false, {}};
}

void print_board(vector<string>& gameboard, vector<pair<int,int>>& coords, string& word) {
    const string RED = "\033[31m";  // red text color
    const string END = "\033[0m";     // end color
    
    std::set<std::pair<int, int>> coord_set(coords.begin(), coords.end());
    
    std::cout << "\n\"" << word << "\" found at coords: ";
    for (const auto& coord : coords) {
        std::cout << "(" << coord.first << ", " << coord.second << ") ";
    }
    std::cout << "\n    ";
    for (int i = 0; i < gameboard[0].size(); i++) {
        std::cout << i % 10 << " ";
    }
    std::cout << "\n";
    for (int i = 0; i < gameboard.size(); i++) {
        std::string line = std::to_string(i) + " " + std::string(std::to_string(gameboard.size()).length() - std::to_string(i).length() + 1, ' ');
        for (int j = 0; j < gameboard[i].size(); j++) {
            if (coord_set.count({j, i}) != 0) {
                line += RED + gameboard[i][j] + END + " ";
            } else {
                line += gameboard[i][j];
                line += " ";
            }
        }
        std::cout << line << "\n";
    }
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
      
      auto start = chrono::high_resolution_clock::now();
      std::pair<bool, vector<pair<int, int>>> output = find_word(gameboard, word);
      auto end = chrono::high_resolution_clock::now();
      
      if (!output.first) {
          cout << "\"" << word << "\" not found." << endl << endl;
          continue;
      } else {
          vector<pair<int,int>> coords = output.second;
          print_board(gameboard,coords,word);
          
          auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
          std::cout << "\nSearch took " << duration.count() << "μs to complete.\n"; //Print time taken to complete search
      }
      
  }

  return 0;
}
