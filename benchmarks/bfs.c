#include <stdio.h>
#include <stdlib.h>

#define MAX_NODES 100
#define MAX_QUEUE 100

// Simple adjacency list representation
typedef struct {
    int neighbors[10];
    int num_neighbors;
} Node;

Node graph[MAX_NODES];
int queue[MAX_QUEUE];
int visited[MAX_NODES];

void init_graph() {
    // Create a graph with irregular connectivity (stresses branch predictor)
    for (int i = 0; i < MAX_NODES; i++) {
        graph[i].num_neighbors = 0;
        visited[i] = 0;
        
        // Add edges in unpredictable pattern
        if (i % 3 == 0 && i + 1 < MAX_NODES) {
            graph[i].neighbors[graph[i].num_neighbors++] = i + 1;
        }
        if (i % 5 == 0 && i + 2 < MAX_NODES) {
            graph[i].neighbors[graph[i].num_neighbors++] = i + 2;
        }
        if (i % 7 == 0 && i + 3 < MAX_NODES) {
            graph[i].neighbors[graph[i].num_neighbors++] = i + 3;
        }
        if (i > 0 && i % 11 == 0) {
            graph[i].neighbors[graph[i].num_neighbors++] = i - 1;
        }
    }
}

void bfs(int start) {
    int front = 0, rear = 0;
    int nodes_visited = 0;
    
    queue[rear++] = start;
    visited[start] = 1;
    
    while (front < rear) {
        int current = queue[front++];
        nodes_visited++;
        
        // Irregular branching based on node neighbors
        for (int i = 0; i < graph[current].num_neighbors; i++) {
            int neighbor = graph[current].neighbors[i];
            
            // Unpredictable branch - depends on graph structure
            if (!visited[neighbor] && neighbor < MAX_NODES) {
                visited[neighbor] = 1;
                queue[rear++] = neighbor;
                
                // Extra irregular branch
                if (neighbor % 2 == 0) {
                    nodes_visited++;
                }
            }
        }
    }
    
    printf("BFS visited %d nodes\n", nodes_visited);
}

int main() {
    init_graph();
    
    // Run BFS multiple times to stress the predictor
    for (int trial = 0; trial < 5; trial++) {
        // Reset visited array
        for (int i = 0; i < MAX_NODES; i++) {
            visited[i] = 0;
        }
        
        bfs(0);
    }
    
    return 0;
}