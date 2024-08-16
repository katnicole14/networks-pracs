#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>

using namespace std;

int next_fibonacci(const string& fib_file) {
    
    //open the file
    ifstream file(fib_file);
    if (!file.is_open()) {
        cerr << "Error: Unable to open file " << fib_file << endl;
        return -1;
    }

    // Read the last two Fibonacci numbers
    string line;
    getline(file, line);
    stringstream ss(line);
    int num1, num2 , num3;
    ss >> num1 >> num2 >> num3;

    // Calculate the next Fibonacci number
    int next_fib = num2 + num3;

    // Update the file with the new Fibonacci sequence
    ofstream outfile(fib_file);
    if (!outfile.is_open()) {
        cerr << "Error: Unable to open file " << fib_file << " for writing" << endl;
        return -1;
    }
    outfile << num3 << " " << next_fib;

    return next_fib;
}

// Function to generate HTML output
void generate_html(int next_fib) {
    // Generate HTML content
    cout << "Content-type: text/html\n" << endl;
    cout << "<!DOCTYPE html>" << endl;
    cout << "<html>" << endl;
    cout << "<head>" << endl;
    cout << "<title>Next Fibonacci Number</title>" << endl;
    cout << "</head>" << endl;
    cout << "<body>" << endl;
    cout << "<h1>Next Fibonacci Number:</h1>" << endl;
    cout << "<p>" << next_fib << "</p>" << endl;
    cout << "<a href=\"/cgi-bin/prev.cgi\">Previous</a>" << endl;
    cout << "</body>" << endl;
    cout << "</html>" << endl;
}

int main() {

    const string fib_file = "/usr/lib/cgi-bin/fibonacci.txt";
    int next_fib = next_fibonacci(fib_file);
    generate_html(next_fib);

    return 0;
}
