"""
System Setup Helper
Builds base gem5 system with configurable branch predictor
"""

import m5
from m5.objects import *

def build_system(binary_path, predictor_type="bimodal"):
    """
    Build gem5 system with specified branch predictor
    
    Args:
        binary_path: Path to RISC-V binary
        predictor_type: "bimodal", "gshare", or "tournament"
    
    Returns:
        Configured system object
    """
    
    # Create system
    system = System()
    
    # Clock domain (1 GHz)
    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = '1GHz'
    system.clk_domain.voltage_domain = VoltageDomain()
    
    # Memory configuration
    system.mem_mode = 'timing'
    system.mem_ranges = [AddrRange('512MB')]
    
    # CPU setup (MinorCPU for in-order execution)
    system.cpu = MinorCPU()
    
    # Configure branch predictor based on type
    if predictor_type == "bimodal":
        system.cpu.branchPred = BiModeBP()
        system.cpu.branchPred.globalPredictorSize = 4096
        
    elif predictor_type == "gshare":
        # gem5 doesn't have direct GshareBP, use LTAGE which has similar behavior
        system.cpu.branchPred = LTAGE()
        
    elif predictor_type == "tournament":
        system.cpu.branchPred = TournamentBP()
        system.cpu.branchPred.localPredictorSize = 2048
        system.cpu.branchPred.globalPredictorSize = 8192
        system.cpu.branchPred.choicePredictorSize = 8192
        
    else:
        raise ValueError(f"Unknown predictor type: {predictor_type}")
    
    # Memory bus
    system.membus = SystemXBar()
    system.cpu.icache_port = system.membus.cpu_side_ports
    system.cpu.dcache_port = system.membus.cpu_side_ports
    
    # Interrupt controller
    system.cpu.createInterruptController()
    
    # Memory controller (DDR3)
    system.mem_ctrl = MemCtrl()
    system.mem_ctrl.dram = DDR3_1600_8x8()
    system.mem_ctrl.dram.range = system.mem_ranges[0]
    system.mem_ctrl.port = system.membus.mem_side_ports
    
    # System port
    system.system_port = system.membus.cpu_side_ports
    
    # Workload setup
    system.workload = SEWorkload.init_compatible(binary_path)
    
    process = Process()
    process.cmd = [binary_path]
    system.cpu.workload = process
    system.cpu.createThreads()
    
    return system

def run_simulation(system):
    """
    Run the simulation and print basic stats
    
    Args:
        system: Configured system object
    """
    root = Root(full_system=False, system=system)
    m5.instantiate()
    
    print("Starting simulation...")
    exit_event = m5.simulate()
    
    print(f'\nSimulation complete!')
    print(f'Exited @ tick {m5.curTick()} because {exit_event.getCause()}')
    
    return exit_event