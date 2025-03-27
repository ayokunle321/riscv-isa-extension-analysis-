"""
Bimodal Branch Predictor Configuration
Uses simple 2-bit saturating counter per branch
"""

from m5.objects import BiModeBP

def create_predictor():
    """Create and configure bimodal branch predictor"""
    bp = BiModeBP()
    bp.numThreads = 1
    bp.globalPredictorSize = 4096  # 4K entry table
    return bp