#include <vector>
#include <assert.h>

/// Giving 9999 of the first 10000 numbers, write a routine that
/// is efficient in memory and computation time to find which number is missing.
int FindMissingInt(const std::vector<int>& numbers) {
    int result = 0;
    for (int i = 0; i < 10000; i++) {
        result ^= i;
    }

    for (auto iter = numbers.begin(); iter != numbers.end(); ++iter) { 
        result ^= *iter;
    }
    
    return result;
}

int main() {
    std::vector<int> numbers;
    int result = 1234;
    for (int i = 0; i < 10000; i++) {
        if (i != result) {
            numbers.push_back(i);
        }
    }

    assert(FindMissingInt(numbers) == result);

    return 0;
}