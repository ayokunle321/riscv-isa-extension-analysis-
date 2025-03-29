# Branch Predictor Analysis

## What I Did

Tested three predictors (Bimodal, Gshare, Tournament) on workloads with unpredictable branching (graph traversal, recursion, hash lookups). Wanted to find out which one actually performs better when branches aren't easy to predict.

## Results Summary

### BFS (Graph Traversal)

| Predictor  | IPC    | Mispred Rate | Cycles    |
|------------|--------|--------------|-----------|
| Bimodal    | 0.0458 | 21.95%       | 265,980   |
| Gshare     | 0.0464 | 12.73%       | 262,934   |
| Tournament | 0.0465 | 17.21%       | 262,300   |

Tournament wins with best IPC and lowest cycles. Bimodal gets wrecked. 21.95% mispredictions because graph branching is too irregular. Gshare has better accuracy but Tournament still edges it out overall.

### Factorial (Recursive)

| Predictor  | IPC    | Mispred Rate | Cycles    |
|------------|--------|--------------|-----------|
| Bimodal    | 0.0548 | 18.37%       | 333,780   |
| Gshare     | 0.0545 | 14.11%       | 336,082   |
| Tournament | 0.0542 | 17.54%       | 337,593   |

Bimodal actually wins here. This is probably becuase recursion has enough pattern that the simple predictor can handle it. Differences are pretty small though as they all perform similarly.

### Hash Lookup (Pointer Chasing)

| Predictor  | IPC    | Mispred Rate | Cycles      |
|------------|--------|--------------|-------------|
| Bimodal    | 0.0442 | 9.47%        | 1,148,614   |
| Gshare     | 0.0446 | 5.82%        | 1,139,194   |
| Tournament | 0.0446 | 7.36%        | 1,139,715   |

Gshare dominates - 5.82% misprediction rate and tied for best IPC. Global history helps predict collision patterns better than local tracking.

## Main Takeaways

- No single predictor wins everything - depends on the workload
- Gshare is best when branches depend on data patterns (like hash collisions)
- Tournament is most consistent across different types of code
- Bimodal isn't terrible and works fine on recursive stuff

The misprediction rates varied a lot:
- BFS: 12.73% to 21.95% (huge spread)
- Hash lookup: 5.82% to 9.47% (tighter)
- Factorial: 14.11% to 18.37% (middle)

When branches are truly random (graph structure), even fancy predictors struggle. When there's a learnable pattern (hash collisions), history-based predictors catch on.

## Conclusion

The IPC numbers look small (0.04-0.05 range) but that's because I used an in-order CPU (MinorCPU). On an out-of-order core with more parallelism, mispredictions would hurt way more since the CPU can't hide the penalty as easily.