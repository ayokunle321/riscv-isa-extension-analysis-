import argparse
import m5
from m5.objects import *

parser = argparse.ArgumentParser()
parser.add_argument('--binary', type=str, required=True,
                    help='Path to RISC-V binary to execute')
parser.add_argument('--gshare-size', type=int, default=2048,
                    help='Gshare predictor table size')
parser.add_argument('--history-length', type=int, default=12,
                    help='Gshare history length')
args = parser.parse_args()

# System setup
system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# CPU setup - MinorCPU with gshare predictor
system.cpu = MinorCPU()
system.cpu.branchPred = GshareBP()
system.cpu.branchPred.numEntries = args.gshare_size
system.cpu.branchPred.globalHistoryBits = args.history_length

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

# Set up workload
system.workload = SEWorkload.init_compatible(args.binary)
process = Process()
process.cmd = [args.binary]
system.cpu.workload = process
system.cpu.createThreads()

# Root and simulation
root = Root(full_system=False, system=system)
m5.instantiate()

print(f"Running {args.binary} with gshare predictor...")
exit_event = m5.simulate()
print(f'Exiting @ tick {m5.curTick()} because {exit_event.getCause()}')
