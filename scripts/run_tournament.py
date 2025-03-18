import argparse
import m5
from m5.objects import *

parser = argparse.ArgumentParser()
parser.add_argument('--binary', type=str, required=True,
                    help='Path to RISC-V binary to execute')
args = parser.parse_args()

# Create system
system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Memory setup
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# CPU setup - using MinorCPU for in-order execution
system.cpu = MinorCPU()
# Tournament/hybrid branch predictor config
system.cpu.branchPred = TournamentBP()

# Memory bus
system.membus = SystemXBar()
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

# Interrupt controller
system.cpu.createInterruptController()

# Memory controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# System port
system.system_port = system.membus.cpu_side_ports

# Set up the workload
system.workload = SEWorkload.init_compatible(args.binary)

# Process
process = Process()
process.cmd = [args.binary]
system.cpu.workload = process
system.cpu.createThreads()

# Root and simulation
root = Root(full_system=False, system=system)
m5.instantiate()

print(f"Running {args.binary} with Tournament predictor...")
exit_event = m5.simulate()
print(f'Exiting @ tick {m5.curTick()} because {exit_event.getCause()}')
