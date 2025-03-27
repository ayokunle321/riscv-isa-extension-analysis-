#!/usr/bin/env python3
"""
Unified Branch Predictor Experiment Runner
Runs all predictors (bimodal, gshare, tournament) on all benchmarks
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
GEM5_BIN = PROJECT_ROOT / "gem5" / "build" / "RISCV" / "gem5.opt"
BENCHMARK_DIR = PROJECT_ROOT / "benchmarks"
RESULTS_DIR = PROJECT_ROOT / "results"
SRC_DIR = PROJECT_ROOT / "src"

# Predictors to test
PREDICTORS = ["bimodal", "gshare", "tournament"]

# Benchmarks to run
BENCHMARKS = [
    "bfs_riscv",
    "factorial_riscv", 
    "hash_lookup_riscv"
]

def check_prerequisites():
    """Verify gem5 binary and benchmarks exist"""
    errors = []
    
    if not GEM5_BIN.exists():
        errors.append(f"gem5 binary not found at: {GEM5_BIN}")
        errors.append("  Run: cd gem5 && scons build/RISCV/gem5.opt -j$(nproc)")
    
    for benchmark in BENCHMARKS:
        bm_path = BENCHMARK_DIR / benchmark
        if not bm_path.exists():
            errors.append(f"Benchmark not found: {bm_path}")
            errors.append(f"  Run: cd benchmarks && make")
    
    if errors:
        print("Prerequisites missing:")
        for error in errors:
            print(error)
        sys.exit(1)
    
    print("✓ All prerequisites found")

def run_experiment(predictor, benchmark, output_dir):
    """Run a single experiment: predictor + benchmark"""
    
    benchmark_path = BENCHMARK_DIR / benchmark
    run_script = SRC_DIR / "run_branch_pred.py"
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Build gem5 command
    cmd = [
        str(GEM5_BIN),
        "--outdir", str(output_dir),
        str(run_script),
        "--binary", str(benchmark_path),
        "--predictor", predictor
    ]
    
    print(f"  Running: {predictor} on {benchmark}")
    print(f"    Output: {output_dir}")
    
    try:
        # Run gem5 simulation
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300  # 5 minute timeout per experiment
        )
        
        # Save stdout/stderr
        (output_dir / "stdout.txt").write_text(result.stdout)
        (output_dir / "stderr.txt").write_text(result.stderr)
        
        if result.returncode == 0:
            print(f"    ✓ Success")
            return True
        else:
            print(f"    ✗ Failed (return code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"    ✗ Timeout (>5 minutes)")
        return False
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Run branch predictor experiments on all benchmarks"
    )
    parser.add_argument(
        "--predictor",
        choices=PREDICTORS + ["all"],
        default="all",
        help="Which predictor to test (default: all)"
    )
    parser.add_argument(
        "--benchmark",
        choices=BENCHMARKS + ["all"],
        default="all",
        help="Which benchmark to run (default: all)"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean results directory before running"
    )
    
    args = parser.parse_args()
    
    # Clean results if requested
    if args.clean and RESULTS_DIR.exists():
        print(f"🗑️  Cleaning {RESULTS_DIR}")
        import shutil
        shutil.rmtree(RESULTS_DIR)
    
    # Check prerequisites
    check_prerequisites()
    
    # Determine which experiments to run
    predictors_to_run = PREDICTORS if args.predictor == "all" else [args.predictor]
    benchmarks_to_run = BENCHMARKS if args.benchmark == "all" else [args.benchmark]
    
    # Run experiments
    total = len(predictors_to_run) * len(benchmarks_to_run)
    current = 0
    successes = 0
    failures = 0
    
    print(f"\n🚀 Starting {total} experiments")
    print(f"   Predictors: {', '.join(predictors_to_run)}")
    print(f"   Benchmarks: {', '.join(benchmarks_to_run)}")
    print()
    
    for predictor in predictors_to_run:
        for benchmark in benchmarks_to_run:
            current += 1
            print(f"[{current}/{total}] {predictor} + {benchmark}")
            
            # Create output directory: results/predictor/benchmark/
            output_dir = RESULTS_DIR / predictor / benchmark.replace("_riscv", "")
            
            # Run experiment
            success = run_experiment(predictor, benchmark, output_dir)
            
            if success:
                successes += 1
            else:
                failures += 1
            
            print()
    
    # Summary
    print("=" * 60)
    print(f"✓ Completed: {successes}/{total} experiments successful")
    if failures > 0:
        print(f"✗ Failed: {failures}/{total} experiments")
    print(f"Results saved to: {RESULTS_DIR}")
    print()
    print("Next steps:")
    print(f"  - View stats: cat {RESULTS_DIR}/predictor/benchmark/stats.txt")
    print(f"  - Parse results: python scripts/parse_results.py")

if __name__ == "__main__":
    main()