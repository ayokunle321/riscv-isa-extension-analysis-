#include <stdio.h>

// Recursive factorial with extra branches to stress predictor
long long factorial(int n) {
    // Base case - predictable branch at end
    if (n <= 1) {
        return 1;
    }
    
    long long result;
    
    // Irregular branching based on odd/even
    if (n % 2 == 0) {
        result = n * factorial(n - 1);
        // Extra conditional
        if (n % 4 == 0) {
            result += 1;  // Just to add more branches
        }
    } else {
        result = n * factorial(n - 1);
        // Different branch pattern for odd numbers
        if (n % 3 == 0) {
            result -= 1;
        }
    }
    
    return result;
}

// Mutual recursion - even more unpredictable for branch predictor
int is_even(int n);
int is_odd(int n);

int is_even(int n) {
    if (n == 0) return 1;
    if (n < 0) return is_even(-n);
    return is_odd(n - 1);
}

int is_odd(int n) {
    if (n == 0) return 0;
    if (n < 0) return is_odd(-n);
    return is_even(n - 1);
}

// Fibonacci with lots of branches (exponential branching)
long long fib_branchy(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;
    
    long long result = fib_branchy(n - 1) + fib_branchy(n - 2);
    
    // Add conditional branches based on result
    if (result % 2 == 0) {
        return result;
    } else if (result % 3 == 0) {
        return result + 1;
    } else {
        return result - 1;
    }
}

int main() {
    long long sum = 0;
    
    // Test factorial with various inputs
    printf("Computing factorials...\n");
    for (int i = 1; i <= 15; i++) {
        sum += factorial(i);
    }
    printf("Sum of factorials: %lld\n", sum);
    
    // Test mutual recursion
    printf("Testing mutual recursion...\n");
    int even_count = 0;
    for (int i = 0; i < 50; i++) {
        if (is_even(i)) even_count++;
    }
    printf("Even numbers from 0-49: %d\n", even_count);
    
    // Test branchy fibonacci (small n to avoid timeout)
    printf("Computing branchy fibonacci...\n");
    sum = 0;
    for (int i = 1; i <= 12; i++) {
        sum += fib_branchy(i);
    }
    printf("Sum of branchy fib: %lld\n", sum);
    
    return 0;
}