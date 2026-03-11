#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <map>

// Your current best decoded message from FINAL_SOLVE.log
std::string CIPHERTEXT = "DOOILDKDESAOKPOTOIRIOEOOODLTKEADASLKATNIONLACEIITCSAIKTTKENDTLTTRSNILLAEOPPPKCDSNSIKPTRLINDTTTALONALCRRDAONRRISEKDDPSCSKPTPTKNAECSPKCLDLLNPENETKCNYTLONDTOYQAHSVLDKURUYCOORDINATESLRDANETKKRDSSNKAP";

// Keywords to look for after transposition
std::vector<std::string> ANCHORS = {"NORTH", "SOUTH", "EAST", "WEST", "LONDON", "MILES", "DEGREES"};

double score_text(const std::string& text) {
    double score = 0;
    for (const auto& word : ANCHORS) {
        if (text.find(word) != std::string::npos) score += 1000.0;
    }
    return score;
}

// Columnar Transposition Check
void check_transposition(const std::string& data) {
    int n = data.length();
    for (int width = 2; width < 15; ++width) {
        int rows = (n + width - 1) / width;
        std::string result = "";
        
        // Simple Columnar Read
        for (int c = 0; c < width; ++c) {
            for (int r = 0; r < rows; ++r) {
                int idx = r * width + c;
                if (idx < n) result += data[idx];
            }
        }

        double s = score_text(result);
        if (s > 0) {
            std::cout << "[!] Transposition Match (Width " << width << "): " << result.substr(0, 50) << "..." << std::endl;
        }
    }
}

int main() {
    std::cout << "Starting Layer 2 Analysis on Orange Pi 5 Max..." << std::endl;
    check_transposition(CIPHERTEXT);
    return 0;
}
