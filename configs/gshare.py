"""
Gshare Branch Predictor Configuration
Uses global history XORed with PC
"""

from m5.objects import MultiperspectivePerceptron8KB

def create_predictor():
    """Create and configure gshare branch predictor"""
    
    # Use the TAGE-based predictor which includes gshare-like behavior
    from m5.objects import LTAGE
    bp = LTAGE()
    return bp

