#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <chrono>
#include <algorithm>
#include <set>
    
int multiple_letters(std::string word, std::string letters) {
    
    for (auto& character : word) {
        int word_count = std::count(word.begin(), word.end(), character);
        int letter_count = std::count(letters.begin(), letters.end(), character);
        if (word_count > letter_count) {
            return 1;
        }
    }
    
    return 0;
}
    
int main() {
    // Define Variables
    std::string letters, text, missing_letters;
    std::vector<std::string> Wordlist;
    
    // Read wordlist file    
    std::ifstream File("wordlist.txt");
    while (getline (File, text)) {
        Wordlist.push_back(text);
    }
    File.close();
    
    // Get input
    std::cout << "Enter all letters on the board: ";
    std::cin >> letters;
    
    // Define Alphabet and convert input to uppercase
    std::set<char> alphabet = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'};
    std::transform(letters.begin(), letters.end(), letters.begin(), toupper);
    
    // Define a set of letters and Find the missing letters
    std::set<char> letters_set(letters.begin(), letters.end());
    std::set_difference(alphabet.begin(), alphabet.end(), letters_set.begin(), letters_set.end(), std::back_inserter(missing_letters));
    
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
        
        if (print_word == true) {
            if (multiple_letters(word,letters) == 1) {
                print_word = false;
            }
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
