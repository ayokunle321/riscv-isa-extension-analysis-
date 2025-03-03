import m5
from m5.objects import *

# System setup
system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# CPU setup
system.cpu = MinorCPU()
system.cpu.branchPred = TournamentBP()  

# Memory bus
system.membus = SystemXBar()
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

system.cpu.createInterruptController()

# Memory controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

# Workload
binary = 'benchmarks/bfs_riscv'
system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()

print(f"Running simulation on {binary} with stats collection...")

exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")

# Print relevant statistics
print("\n=== Statistics ===")
print(f"Instructions executed: {system.cpu.numInst}")
print(f"IPC: {system.cpu.numInst / m5.curTick() * float(system.clk_domain.clock)}")
print(f"Branch mispredictions: {system.cpu.branchMispred}")
