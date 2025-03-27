#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TABLE_SIZE 64
#define NUM_KEYS 200

// Hash table with chaining (linked list for collisions)
typedef struct Node {
    int key;
    int value;
    struct Node* next;
} Node;

Node* hash_table[TABLE_SIZE];

// Simple hash function (deliberately causes collisions)
int hash(int key) {
    return (key * 31 + 17) % TABLE_SIZE;
}

void insert(int key, int value) {
    int index = hash(key);
    
    Node* new_node = (Node*)malloc(sizeof(Node));
    new_node->key = key;
    new_node->value = value;
    new_node->next = hash_table[index];
    hash_table[index] = new_node;
}

// Lookup with unpredictable branching (depends on collision chain length)
int lookup(int key) {
    int index = hash(key);
    Node* current = hash_table[index];
    
    // Traverse collision chain - highly unpredictable branching
    while (current != NULL) {
        if (current->key == key) {
            return current->value;
        }
        current = current->next;
        
        // Extra branch to stress predictor
        if (current != NULL && current->key % 2 == 0) {
            // Even keys take different path
            continue;
        }
    }
    
    return -1; // Not found
}

// Delete operation with complex branching
int delete(int key) {
    int index = hash(key);
    Node* current = hash_table[index];
    Node* prev = NULL;
    
    while (current != NULL) {
        if (current->key == key) {
            // Found the key - branching based on position
            if (prev == NULL) {
                // First node in chain
                hash_table[index] = current->next;
            } else {
                // Middle or end of chain
                prev->next = current->next;
            }
            free(current);
            return 1;
        }
        prev = current;
        current = current->next;
    }
    
    return 0; // Not found
}

// Count collision chain length (irregular branching)
int count_chain(int index) {
    int count = 0;
    Node* current = hash_table[index];
    
    while (current != NULL) {
        count++;
        current = current->next;
        
        // Branch based on count (unpredictable)
        if (count > 5) {
            break;
        }
    }
    
    return count;
}

int main() {
    // Initialize hash table
    for (int i = 0; i < TABLE_SIZE; i++) {
        hash_table[i] = NULL;
    }
    
    // Insert keys with pattern that causes collisions
    printf("Inserting keys...\n");
    for (int i = 0; i < NUM_KEYS; i++) {
        int key = i * 7 + 3;  // Pattern that causes collisions
        insert(key, i * 10);
    }
    
    // Lookup with unpredictable access pattern
    printf("Looking up keys...\n");
    int found_count = 0;
    int not_found_count = 0;
    
    for (int i = 0; i < NUM_KEYS * 2; i++) {
        int key = i * 7 + 3;
        int result = lookup(key);
        
        // Irregular branching based on lookup result
        if (result != -1) {
            found_count++;
            if (result % 2 == 0) {
                found_count++;  // Extra increment for even values
            }
        } else {
            not_found_count++;
        }
    }
    
    printf("Found: %d, Not found: %d\n", found_count, not_found_count);
    
    // Count collisions (more irregular branching)
    printf("Counting collision chains...\n");
    int total_nodes = 0;
    int max_chain = 0;
    
    for (int i = 0; i < TABLE_SIZE; i++) {
        int chain_len = count_chain(i);
        total_nodes += chain_len;
        
        if (chain_len > max_chain) {
            max_chain = chain_len;
        }
    }
    
    printf("Total nodes: %d, Max chain length: %d\n", total_nodes, max_chain);
    
    // Delete some keys (complex branching)
    printf("Deleting keys...\n");
    int deleted = 0;
    for (int i = 0; i < NUM_KEYS; i += 3) {
        int key = i * 7 + 3;
        if (delete(key)) {
            deleted++;
        }
    }
    printf("Deleted %d keys\n", deleted);
    
    // Cleanup
    for (int i = 0; i < TABLE_SIZE; i++) {
        Node* current = hash_table[i];
        while (current != NULL) {
            Node* temp = current;
            current = current->next;
            free(temp);
        }
    }
    
    return 0;
}