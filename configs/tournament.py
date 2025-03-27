"""
Tournament (Hybrid) Branch Predictor Configuration
Combines local and global predictors with a selector
"""

from m5.objects import TournamentBP

def create_predictor():
    """Create and configure tournament branch predictor"""
    bp = TournamentBP()
    
    # Local predictor settings
    bp.localPredictorSize = 2048
    bp.localCtrBits = 2
    
    # Global predictor settings  
    bp.globalPredictorSize = 8192
    bp.globalCtrBits = 2
    
    # Choice predictor (meta-predictor)
    bp.choicePredictorSize = 8192
    bp.choiceCtrBits = 2
    
    return bp