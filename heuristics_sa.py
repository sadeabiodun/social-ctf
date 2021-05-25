from os.path import join
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ctf_dataset.load import create_wrapped_dataset
from features import get_features

#import luke's heuristics functions 
from ctf_dataset.behaviours.heuristic import near_teammate
from ctf_dataset.behaviours.heuristic import local_behaviour_length, pad_behaviour,  behvaiour_start_and_end, camp_own_base, camp_opponent_base, running_forwards, running_backwards, approaching_own_base, approaching_opponent_base, approaching_own_flag, approaching_opponent_flag, approaching_teammate


#import sam's heuristics functions 
from detectors_sam import get_position, get_proximity, get_following

# Set base directory 
base_dir = '/mnt/bucket/labs/hasson/snastase/social-ctf'
data_dir = join(base_dir, 'data')

# Create wrapped CTF dataset
wrap_f = create_wrapped_dataset(data_dir, output_dataset_name="virtual.hdf5")

map_id = 0 # 0
matchup_id = 54 # 0-54 (0, 34, 49, 54)
repeat_id = slice(None) # 0-7
player_id = slice(None) # 0-3

# Test functions by viewing output for one matchup one repeat 

#testing sam's following function 
test_sam = get_following(wrap_f, matchup_id=0, repeat_id=0)

#testing luke's following function 
test_luke = near_teammate(wrap_f, matchup_id=0, repeat_id=0)

## Plotting to verify 

plt.plot(test_sam[0].T, label='sam p1')
plt.plot(test_sam[1].T, label='sam p2')

plt.plot(p1[:,0].T, label='luke p1')
plt.plot(p2[:,0].T, label='luke p2')
plt.legend()

## current conundrum, the output for luke and sam's functions do not match, even when setting matchup and repeat id to 0 