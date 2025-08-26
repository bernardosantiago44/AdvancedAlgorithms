// Bernardo Santiago Marín
// A01638915
#include <iostream>
#include <vector>

using namespace std;

int fibonacciRecursive(int n) {
    if (n == 0) return 0;
    else if (n == 1) return 1;
    return fibonacciRecursive(n-1) + fibonacciRecursive(n-2);
}

int fibonacciDP(int n, vector<int>* seen) {
    if (n < seen->size()) return seen->at(n);
    int fibResult =  fibonacciDP(n-2, seen) + fibonacciDP(n-1, seen);
    seen->push_back(fibResult);
    return fibResult;
}

int fibonacciDP(int n) {
    vector<int> seen = {0, 1};
    return fibonacciDP(n, &seen);
}

int main() {
    int n;

    cout << "Fibonacci: ";
    cin >> n;

    // Mark time taken for both implementations in ms
    clock_t start = clock();
    int fibRecursive = fibonacciRecursive(n);
    clock_t end = clock();
    double timeTaken = double(end - start) / CLOCKS_PER_SEC * 1000;
    cout << "Time taken (Recursive): " << timeTaken << " ms" << endl;

    start = clock();
    int fibDP = fibonacciDP(n);
    end = clock();
    timeTaken = double(end - start) / CLOCKS_PER_SEC * 1000;
    cout << "Time taken (DP): " << timeTaken << " ms" << endl;

    cout << "Fibonacci of " << n << " is: " << fibRecursive << endl;
    cout << "Fibonacci with DP: " << fibDP << endl;
}