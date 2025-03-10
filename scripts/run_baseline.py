#!/usr/bin/env python3
import os
import subprocess

benchmarks = [
    "benchmarks/bfs_riscv",
    "benchmarks/factorial_riscv",
    "benchmarks/hash_lookup_riscv"
]

gem5_bin = "gem5/build/RISCV/gem5.opt"
cpu_cfg = "configs/baseline_cpu.json" 
results_dir = "results/baseline"

os.makedirs(results_dir, exist_ok=True)

for bm in benchmarks:
    bm_name = os.path.basename(bm)
    out_dir = os.path.join(results_dir, bm_name)
    os.makedirs(out_dir, exist_ok=True)

    print(f"Running baseline for {bm_name}...")
    subprocess.run([
        gem5_bin,
        "--outdir", out_dir,
        "--script", cpu_cfg,
        "--binary", bm
    ])
