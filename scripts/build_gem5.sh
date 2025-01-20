#!/bin/bash
set -e

echo "Building gem5 for RISC-V target..."
cd gem5
scons build/RISCV/gem5.opt -j$(nproc)
echo "gem5 build complete!"
