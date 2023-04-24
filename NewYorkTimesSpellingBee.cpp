#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>
#include <set>
#include <chrono>

int main() {
    // Define some variables
    std::string text, middle, other_letters, all_letters, missing_letters;
    std::vector<std::string> Wordlist;
    
    // Read from file    
    std::ifstream File("wordlist.txt");
    
    while (getline (File, text)) {
        Wordlist.push_back(text);
    }

    File.close();
    
    // Get input
    std::cout << "Enter the middle letter: ";
    std::cin >> middle;
    
    std::cout << "Enter the other letters: ";
    std::cin >> other_letters;
    
    // Define Alphabet and all the letters that are used in the game
    std::set<char> alphabet = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'};
    all_letters = middle + other_letters;
    
    // Convert letters to uppercase
    std::transform(all_letters.begin(), all_letters.end(), all_letters.begin(), toupper);
    std::transform(middle.begin(), middle.end(), middle.begin(), toupper);
    
    // Find missing letters
    std::set<char> all_letters_set(all_letters.begin(), all_letters.end());
    std::set_difference(alphabet.begin(), alphabet.end(), all_letters_set.begin(), all_letters_set.end(), std::back_inserter(missing_letters));
    
    // Start timer
    auto start = std::chrono::high_resolution_clock::now();
    
    // Solve
    std::cout << "\nAll found words:\n\n";
    
    bool print_word;
    for (const auto& word : Wordlist) {
        print_word = true;
        
        if (word.find_first_of(missing_letters) != std::string::npos) {
            print_word = false;
        }
        
        if (word.find(middle) == std::string::npos) {
            print_word = false;
        }
        
        if (print_word) {
            std::cout << "    " << word << std::endl;
        }
        
    }
    
    // End timer and print time
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "\nElapsed time: " << elapsed.count() << " seconds\n\n";
    
    return 0;
}
