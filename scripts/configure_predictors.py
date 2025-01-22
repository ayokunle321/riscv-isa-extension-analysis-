import m5
from m5.objects import *

# Predictor setup
predictor_type = 'TournamentBP'  # default
predictors = {
    'bimodal': BimodalBP(),
    'gshare': GshareBP(),
    'tournament': TournamentBP()
}

def create_predictor(name):
    if name not in predictors:
        raise ValueError(f"Unknown predictor: {name}")
    return predictors[name]
