#!/usr/bin/env python3
"""
Generate comparison graphs for branch predictor performance
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import json

# Load results
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
RESULTS_FILE = PROJECT_ROOT / "results" / "analysis" / "results.json"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "graphs"

def load_results():
    """Load results from JSON"""
    with open(RESULTS_FILE, 'r') as f:
        return json.load(f)

def plot_ipc_comparison(results):
    """Generate IPC comparison bar chart"""
    benchmarks = sorted(set(bm for pred_data in results.values() for bm in pred_data.keys()))
    predictors = sorted(results.keys())
    
    x = np.arange(len(benchmarks))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for i, predictor in enumerate(predictors):
        ipcs = [results[predictor].get(bm, {}).get('ipc', 0) for bm in benchmarks]
        ax.bar(x + i * width, ipcs, width, label=predictor.capitalize())
    
    ax.set_xlabel('Benchmark', fontsize=12)
    ax.set_ylabel('IPC (Instructions Per Cycle)', fontsize=12)
    ax.set_title('Branch Predictor IPC Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels([bm.upper() for bm in benchmarks])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / "ipc_comparison.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()

def plot_mispred_comparison(results):
    """Generate misprediction rate comparison bar chart"""
    benchmarks = sorted(set(bm for pred_data in results.values() for bm in pred_data.keys()))
    predictors = sorted(results.keys())
    
    x = np.arange(len(benchmarks))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for i, predictor in enumerate(predictors):
        mispreds = [results[predictor].get(bm, {}).get('mispredict_rate', 0) for bm in benchmarks]
        ax.bar(x + i * width, mispreds, width, label=predictor.capitalize())
    
    ax.set_xlabel('Benchmark', fontsize=12)
    ax.set_ylabel('Misprediction Rate (%)', fontsize=12)
    ax.set_title('Branch Predictor Misprediction Rates', fontsize=14, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels([bm.upper() for bm in benchmarks])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / "mispred_comparison.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()

def plot_cycles_comparison(results):
    """Generate cycle count comparison"""
    benchmarks = sorted(set(bm for pred_data in results.values() for bm in pred_data.keys()))
    predictors = sorted(results.keys())
    
    x = np.arange(len(benchmarks))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for i, predictor in enumerate(predictors):
        cycles = [results[predictor].get(bm, {}).get('num_cycles', 0) / 1000 for bm in benchmarks]
        ax.bar(x + i * width, cycles, width, label=predictor.capitalize())
    
    ax.set_xlabel('Benchmark', fontsize=12)
    ax.set_ylabel('Cycles (thousands)', fontsize=12)
    ax.set_title('Execution Cycles Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels([bm.upper() for bm in benchmarks])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / "cycles_comparison.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Generating performance comparison graphs...")
    
    results = load_results()
    
    plot_ipc_comparison(results)
    plot_mispred_comparison(results)
    plot_cycles_comparison(results)
    
    print("\n✓ All graphs generated successfully")
    print(f"   Location: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()