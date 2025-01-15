#include <stdio.h>
#include <stdint.h>

#define ARRAY_SIZE 1000

int main() {
    uint32_t array[ARRAY_SIZE];
    uint64_t sum = 0;
    
    // Initialize array
    for (int i = 0; i < ARRAY_SIZE; i++) {
        array[i] = i;
    }
    
    // Sum array elements
    for (int i = 0; i < ARRAY_SIZE; i++) {
        sum += array[i];
    }
    
    printf("Sum: %lu\n", sum);
    return 0;
}
