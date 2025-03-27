#!/usr/bin/env python3
print("=" * 60)
print("SCRIPT STARTING!")
print("=" * 60)

import argparse
import sys
from pathlib import Path
import m5
from m5.objects import *

print("Parsing arguments...")

parser = argparse.ArgumentParser(description='Run RISC-V binary with specified branch predictor')
parser.add_argument('--binary', type=str, required=True, help='Path to RISC-V binary')
parser.add_argument('--predictor', type=str, choices=['bimodal', 'gshare', 'tournament'], default='bimodal', help='Branch predictor type')

args = parser.parse_args()

print(f"Configuration: {args.binary} with {args.predictor}")

# Create system
system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

system.cpu = MinorCPU()

# Configure predictor
if args.predictor == "bimodal":
    system.cpu.branchPred = BiModeBP()
    system.cpu.branchPred.globalPredictorSize = 4096
elif args.predictor == "gshare":
    system.cpu.branchPred = LTAGE()
elif args.predictor == "tournament":
    system.cpu.branchPred = TournamentBP()

print(f"Predictor: {args.predictor} configured")

system.membus = SystemXBar()
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports
system.cpu.createInterruptController()

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

print(f"Loading binary: {args.binary}")
system.workload = SEWorkload.init_compatible(args.binary)

process = Process()
process.cmd = [args.binary]
system.cpu.workload = process
system.cpu.createThreads()

print("Instantiating...")
root = Root(full_system=False, system=system)
m5.instantiate()

print("Starting simulation...")
exit_event = m5.simulate()

print(f"DONE! Exited @ tick {m5.curTick()}")