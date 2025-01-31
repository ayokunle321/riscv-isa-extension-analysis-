import m5
from m5.objects import *

# Simple RISC-V system with default branch predictor
system = System()
system.clk_domain = SrcClockDomain(clock="1GHz", voltage_domain=VoltageDomain())
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]

system.cpu = MinorCPU()  # default predictor
system.membus = SystemXBar()
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports
system.cpu.createInterruptController()

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

# Example workload placeholder
from m5.objects import SEWorkload, Process
binary_path = "benchmarks/bfs_riscv"  # placeholder
system.workload = SEWorkload.init_compatible(binary_path)
process = Process()
process.cmd = [binary_path]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()
print(f"Running {binary_path}...")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")