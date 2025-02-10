from m5.objects import *

# Import baseline CPU config
from configs.baseline_cpu import *

# Clone the baseline CPU
cpu = system.cpu

# Configure a simple bimodal branch predictor
cpu.branchPred = BimodalBP()
cpu.branchPred.size = 4096  # example size

system.workload = SEWorkload.init_compatible(args.binary)
