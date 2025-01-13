# model parameters
INPUT_DIM = 30
NUM_LEADING_POINTS = 5
ACTION_DIM = 2
HIDDEN_LAYER_DIM = 128
DISCOUNT = 1
LR = 0.002
OUTPUT_SCALING = 3
SIGMA = 0.02

# Options
USE_PHASE_DIFFERENCE = False
NORMALIZE_STATES = True
VERBOSE = 0
SAVE_IMAGE_FREQ = 5
SAVE_SIMPLIFIED = False
COMBINE_STATES_FOR_CRITIC = True
ADD_PROGRESS_INDICATOR = True
REWARD_DISTANCE_CLIPPING = 10
REWARD_NORMALIZATION_MODE = 'sigmoid' # options: 'linear', 'sigmoid'
