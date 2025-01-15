#include <stdio.h>

#define ITERATIONS 10000

int main() {
    volatile int counter = 0;
    
    for (int i = 0; i < ITERATIONS; i++) {
        counter++;
    }
    
    printf("Counter: %d\n", counter);
    return 0;
}
