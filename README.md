# Branch Predictor Comparison Study

Comparative analysis of branch prediction strategies on irregular workloads using gem5.

## Overview

This project compares three branch predictors (Bimodal, Gshare/LTAGE, Tournament) on workloads designed to stress prediction accuracy (graph traversal, recursion, and hash table operations). The goal is to understand which predictor performs best under different control flow patterns.

## Predictors Tested

- **Bimodal**: Simple 2-bit saturating counters (4K entries)
- **Gshare (LTAGE)**: Global history-based prediction
- **Tournament**: Hybrid local + global with meta-predictor

## Benchmarks

- **BFS**: Graph traversal with irregular branching patterns
- **Factorial**: Deep recursion with mutual recursion and fibonacci
- **Hash Lookup**: Hash table with collision chains (pointer chasing)

## Quick Results

| Benchmark   | Best Predictor | IPC    | Mispred Rate |
|-------------|----------------|--------|--------------|
| BFS         | Tournament     | 0.0465 | 17.21%       |
| Factorial   | Bimodal        | 0.0548 | 18.37%       |
| Hash Lookup | Gshare         | 0.0446 | 5.82%        |

See [detailed findings](docs/FINDINGS.md) for full analysis.

## Setup

### Prerequisites

- gem5 (RISC-V build)
- RISC-V cross-compiler (`riscv64-unknown-elf-gcc`)
- Python 3.8+

### Build

```bash
# Clone the repo
git clone <your-repo-url>
cd riscv-isa-extension-analysis-

# Build gem5 for RISC-V
cd gem5
scons build/RISCV/gem5.opt -j$(nproc)
cd ..

# Compile benchmarks
cd benchmarks
make
cd ..
```

## Running Experiments

### Run All Experiments

```bash
python3 scripts/run_all_experiments.py
```

This runs 9 experiments (3 predictors × 3 benchmarks) and saves results to `results/`.

### Run Single Configuration

```bash
./gem5/build/RISCV/gem5.opt \
  --outdir=output \
  src/run_branch_pred.py \
  --binary benchmarks/bfs_riscv \
  --predictor tournament
```

## Analyzing Results

### Generate Comparison Table

```bash
python3 scripts/parse_results.py
```

### Export Data

```bash
# Export to CSV/JSON
python3 scripts/parse_results.py --csv --json

# Generate graphs
python3 scripts/generate_graphs.py
```

## Project Structure

```
.
├── benchmarks/          # RISC-V test programs
│   ├── bfs.c
│   ├── factorial.c
│   └── hash_lookup.c
├── src/
│   └── run_branch_pred.py    # Main simulation script
├── scripts/
│   ├── run_all_experiments.py # Automation
│   ├── parse_results.py       # Stats parser
│   └── generate_graphs.py     # Visualization
├── results/
│   ├── bimodal/
│   ├── gshare/
│   ├── tournament/
│   └── analysis/
└── docs/
    ├── FINDINGS.md             # Detailed analysis
    └── graphs/                 # Performance charts
```
