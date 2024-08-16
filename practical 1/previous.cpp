#include <iostream>
#include <fstream>
#include <string>

// Function to calculate the previous Fibonacci number
int previousFibonacci(const std::string& fibFile) {
    // Open the Fibonacci file in read mode
    std::ifstream file(fibFile);
    if (!file.is_open()) {
        std::cerr << "Error: Unable to open file: " << fibFile << std::endl;
        return -1;
    }

    // Read the current Fibonacci numbers
    int fibNumbers[3];
    for (int i = 0; i < 3; ++i) {
        file >> fibNumbers[i];
    }

    // Calculate the previous Fibonacci number
    int prevFib = fibNumbers[1] - fibNumbers[0];

    // Update the file with the new Fibonacci sequence
    file.close();
    std::ofstream outFile(fibFile);
    if (!outFile.is_open()) {
        std::cerr << "Error: Unable to open file for writing: " << fibFile << std::endl;
        return -1;
    }
    outFile << prevFib << " " << fibNumbers[0] << " " << fibNumbers[1];

    return prevFib;
}

// Function to generate HTML output
void generateHtml(int prevFib) {
    // Generate HTML content
    std::cout << "Content-type: text/html\n\n";
    std::cout << "<!DOCTYPE html>\n";
    std::cout << "<html>\n";
    std::cout << "<head>\n";
    std::cout << "<title>Previous Fibonacci Number</title>\n";
    std::cout << "</head>\n";
    std::cout << "<body>\n";
    std::cout << "<h1>Previous Fibonacci Number:</h1>\n";
    std::cout << "<p>" << prevFib << "</p>\n";
    std::cout << "<a href=\"/cgi-bin/next.cgi\">Next</a>\n";
    std::cout << "</body>\n";
    std::cout << "</html>\n";
}

// Main function
int main() {
    // Path to the Fibonacci file
    std::string fibFile = "/usr/lib/cgi-bin/fibonacci.txt";

    // Calculate the previous Fibonacci number
    int prevFib = previousFibonacci(fibFile);

    // Generate HTML output
    generateHtml(prevFib);

    return 0;
}
