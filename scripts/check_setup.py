#!/usr/bin/env python3
"""
Verify experiment setup is ready to run
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent.absolute()

def check_item(name, path, fix_cmd=None):
    """Check if a file/directory exists"""
    exists = path.exists()
    status = "✓" if exists else "✗"
    print(f"{status} {name}: {path}")
    
    if not exists and fix_cmd:
        print(f"   Fix: {fix_cmd}")
    
    return exists

def main():
    print("🔍 Checking experiment setup...\n")
    
    all_good = True
    
    # Check gem5
    gem5_bin = PROJECT_ROOT / "gem5" / "build" / "RISCV" / "gem5.opt"
    all_good &= check_item(
        "gem5 binary",
        gem5_bin,
        "cd gem5 && scons build/RISCV/gem5.opt -j$(nproc)"
    )
    
    # Check benchmarks
    print("\nBenchmarks:")
    benchmark_dir = PROJECT_ROOT / "benchmarks"
    for bm in ["bfs_riscv", "factorial_riscv", "hash_lookup_riscv"]:
        all_good &= check_item(
            f"  {bm}",
            benchmark_dir / bm,
            "cd benchmarks && make"
        )
    
    # Check source files
    print("\nSource files:")
    src_dir = PROJECT_ROOT / "src"
    all_good &= check_item("  run_branch_pred.py", src_dir / "run_branch_pred.py")
    
    # Check scripts
    print("\nScripts:")
    scripts_dir = PROJECT_ROOT / "scripts"
    all_good &= check_item("  run_all_experiments.py", scripts_dir / "run_all_experiments.py")
    all_good &= check_item("  parse_results.py", scripts_dir / "parse_results.py")
    
    print("\n" + "=" * 60)
    if all_good:
        print("Setup is ready! You can now run:")
        print(f"   cd {PROJECT_ROOT}")
        print("   ./scripts/run_all_experiments.py")
    else:
        print("Setup incomplete. Fix the issues above first.")
        sys.exit(1)

if __name__ == "__main__":
    main()