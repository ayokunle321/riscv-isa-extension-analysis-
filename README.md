# RISC-V ISA Extension Performance Analysis

This project explores the performance impact of adding custom instructions to the RISC-V ISA using the gem5 simulator.

## Project Goals
- Implement and evaluate POPCOUNT and FMA custom instructions in gem5  
- Compare real workload performance against theoretical speedups  
- Identify and analyze microarchitectural factors that limit gains from ISA-level optimizations  

## Project Structure
- `gem5/` – gem5 simulator (submodule)  
- `benchmarks/` – test programs and workloads  
- `patches/` – ISA extension source patches  
- `scripts/` – automation for build and run experiments  
- `results/` – collected performance data  
- `docs/` – analysis reports and supporting documentation  

## Status
**Phase 1: Infrastructure Setup – In Progress**
