#!/bin/bash
set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <benchmark.elf>"
    exit 1
fi

BENCHMARK=$1
GEM5_BIN=./gem5/build/RISCV/gem5.opt
CONFIG=scripts/simple_config.py

echo "Running $BENCHMARK in gem5..."
$GEM5_BIN $CONFIG --binary=$BENCHMARK
echo "Run complete! Check m5out/stats.txt for results"
