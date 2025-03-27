#!/usr/bin/env python3
"""
Parse gem5 statistics and generate comparison tables
"""

import re
import json
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
RESULTS_DIR = PROJECT_ROOT / "results"

def parse_stats_file(stats_path):
    """Extract key statistics from gem5 stats.txt file"""
    
    if not stats_path.exists():
        return None
    
    stats = {}
    content = stats_path.read_text()
    
    # Key metrics to extract (using regex)
    patterns = {
        'sim_ticks': r'simTicks\s+(\d+)',
        'sim_seconds': r'simSeconds\s+([\d.]+)',
        'num_insts': r'system\.cpu\.numInsts\s+(\d+)',
        'num_cycles': r'system\.cpu\.numCycles\s+(\d+)',
        'ipc': r'system\.cpu\.ipc\s+([\d.]+)',
        'branch_pred_lookups': r'system\.cpu\.branchPred\.lookups\s+(\d+)',
        'branch_pred_cond_predicted': r'system\.cpu\.branchPred\.condPredicted\s+(\d+)',
        'branch_pred_cond_incorrect': r'system\.cpu\.branchPred\.condIncorrect\s+(\d+)',
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            try:
                # Try to parse as int first, then float
                value = int(match.group(1))
            except ValueError:
                value = float(match.group(1))
            stats[key] = value
        else:
            stats[key] = None
    
    # Calculate misprediction rate
    if stats.get('branch_pred_cond_predicted') and stats.get('branch_pred_cond_incorrect'):
        predicted = stats['branch_pred_cond_predicted']
        incorrect = stats['branch_pred_cond_incorrect']
        stats['mispredict_rate'] = (incorrect / predicted * 100) if predicted > 0 else 0
    else:
        stats['mispredict_rate'] = None
    
    return stats

def collect_all_results():
    """Collect results from all experiments"""
    
    results = defaultdict(lambda: defaultdict(dict))
    
    if not RESULTS_DIR.exists():
        print(f"Results directory not found: {RESULTS_DIR}")
        return None
    
    # Iterate through results/predictor/benchmark/
    for predictor_dir in RESULTS_DIR.iterdir():
        if not predictor_dir.is_dir():
            continue
        
        predictor = predictor_dir.name
        
        for benchmark_dir in predictor_dir.iterdir():
            if not benchmark_dir.is_dir():
                continue
            
            benchmark = benchmark_dir.name
            stats_path = benchmark_dir / "stats.txt"
            
            stats = parse_stats_file(stats_path)
            if stats:
                results[predictor][benchmark] = stats
    
    return results

def print_comparison_table(results):
    """Print formatted comparison table"""
    
    if not results:
        print("No results to display")
        return
    
    # Get all predictors and benchmarks
    predictors = sorted(results.keys())
    all_benchmarks = set()
    for pred_results in results.values():
        all_benchmarks.update(pred_results.keys())
    benchmarks = sorted(all_benchmarks)
    
    print("\n" + "=" * 80)
    print("BRANCH PREDICTOR COMPARISON")
    print("=" * 80)
    
    for benchmark in benchmarks:
        print(f"\n{benchmark.upper()}")
        print("-" * 80)
        
        # Table header
        print(f"{'Predictor':<15} {'IPC':<10} {'Mispred %':<12} {'Instructions':<15} {'Cycles':<15}")
        print("-" * 80)
        
        for predictor in predictors:
            stats = results[predictor].get(benchmark)
            
            if stats:
                ipc = f"{stats.get('ipc', 0):.4f}" if stats.get('ipc') else "N/A"
                mispredict = f"{stats.get('mispredict_rate', 0):.2f}%" if stats.get('mispredict_rate') is not None else "N/A"
                insts = f"{stats.get('num_insts', 0):,}" if stats.get('num_insts') else "N/A"
                cycles = f"{stats.get('num_cycles', 0):,}" if stats.get('num_cycles') else "N/A"
                
                print(f"{predictor:<15} {ipc:<10} {mispredict:<12} {insts:<15} {cycles:<15}")
            else:
                print(f"{predictor:<15} {'NO DATA':<10}")
        
        print()

def export_json(results, output_path):
    """Export results to JSON file"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✓ Exported to {output_path}")

def export_csv(results, output_path):
    """Export results to CSV file"""
    import csv
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            'Predictor', 'Benchmark', 'IPC', 'Misprediction Rate (%)',
            'Instructions', 'Cycles', 'Sim Seconds'
        ])
        
        # Data rows
        for predictor, benchmarks in sorted(results.items()):
            for benchmark, stats in sorted(benchmarks.items()):
                writer.writerow([
                    predictor,
                    benchmark,
                    stats.get('ipc', ''),
                    stats.get('mispredict_rate', ''),
                    stats.get('num_insts', ''),
                    stats.get('num_cycles', ''),
                    stats.get('sim_seconds', '')
                ])
    
    print(f"✓ Exported to {output_path}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Parse gem5 experiment results")
    parser.add_argument('--json', action='store_true', help='Export to JSON')
    parser.add_argument('--csv', action='store_true', help='Export to CSV')
    parser.add_argument('--output-dir', type=Path, default=RESULTS_DIR / "analysis",
                       help='Output directory for exports')
    
    args = parser.parse_args()
    
    print("Collecting results...")
    results = collect_all_results()
    
    if not results:
        print("No results found")
        return
    
    # Print comparison table
    print_comparison_table(results)
    
    # Export if requested
    if args.json:
        export_json(results, args.output_dir / "results.json")
    
    if args.csv:
        export_csv(results, args.output_dir / "results.csv")
    
    print("\n✓ Analysis complete")

if __name__ == "__main__":
    main()