#include <iostream>
#include <vector>

using namespace std;

vector<double> merge(vector<double>& left, vector<double>& right) {
    if (left.size() == 0) return right;
    else if (right.size() == 0) return left;

    int leftPtr = 0, rightPtr = 0;
    
    vector<double> result;
    result.reserve(left.size() + right.size());
    
    // While both arrays have numbers, merge them in descending order
    while (leftPtr < left.size() && rightPtr < right.size()) {
        if (left[leftPtr] >= right[rightPtr]) {
            result.push_back(left[leftPtr++]);
        } else {
            result.push_back(right[rightPtr++]);
        }
    }

    // Copy all remaining items from the left
    while (leftPtr < left.size()) result.push_back(left[leftPtr++]);

    // Copy all remaining items from the right
    while (rightPtr < right.size()) result.push_back(right[rightPtr++]);

    return result;
}

vector<double> mergeSort(vector<double>& values) {
    if (values.size() <= 1) return values;

    size_t mid = values.size() / 2;

    vector<double> left(values.begin(), values.begin() + mid);
    vector<double> right(values.begin() + mid, values.end());
    
    left = mergeSort(left);
    right = mergeSort(right);

    return merge(left, right);
}

int main() {
    int inputAmount;
    vector<double> values;

    cin >> inputAmount;

    for (int i = 0; i < inputAmount; i++) {
        double num;
        cin >> num;
        values.push_back(num);
    }

    values = mergeSort(values);

    for (double num: values) {
        cout << num << " ";
    }
    cout << endl;  
}