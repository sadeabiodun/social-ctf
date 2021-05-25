## Script for Detecting High Order Behaviors 
# SA 5.6.21 

from os.path import join
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ctf_dataset.load import create_wrapped_dataset
from features import get_features
from itertools import combinations

base_dir = '/mnt/bucket/labs/hasson/snastase/social-ctf'
data_dir = join(base_dir, 'data')

# Create wrapped CTF dataset
wrap_f = create_wrapped_dataset(data_dir, output_dataset_name="virtual.hdf5")

n_lstms = 512
n_repeats = 8
n_players = 4
map_id = 0

matchup_id = 0 # 0-54 (0, 34, 49, 54)
repeat_id = slice(None) # 0-7
player_id = slice(None) # 0-3


# Get matchups with all same agents (e.g. AA vs AA)
agent_ids = wrap_f['map/matchup/repeat/player/agent_id'][0, :, :, :, 0]
matchup_ids = np.all(agent_ids[:, 0, :] == agent_ids[:, 0, 0][:, np.newaxis], axis=1)
n_matchups = np.sum(matchup_ids) # 0, 34, 49, 54

#def check_following():
# commenting out for now but eventually things below should go into a func
"""
Function to compute following behavior
"""
feature_set = ['position']
# Pulling in get position code from behavior.py 
position, position_labels = get_features(wrap_f,
                                         feature_set=feature_set,
                                         map_id=map_id,
                                         matchup_id=matchup_id,
                                         repeat_id=repeat_id,
                                         player_id=player_id)

# Ignore z-position for now
position = position[..., :2]

repeat = 0 
position = position[repeat, ...]

# Compute Euclidean distance over time for all payers of players
n_players = 4
proximities = []

for pair in combinations(np.arange(n_players), 2):
    proximities.append(np.sqrt(np.sum((position[pair[0], ...] -
                                       position[pair[1], ...]) ** 2,
                                      axis=1)))
proximities = np.array(proximities).T

# Get proximities for cooperating and competing agents
coop_ids, comp_ids = [0, 5], [1, 2, 3, 4]


prox_coop = proximities[..., coop_ids]
prox_comp = proximities[..., comp_ids]




"""The thing about this function is it has to incorporate the following
1. Following for longer than x amount of time (time course + position)
2. Who is following whom 
3. Can the agents see each other (incorporating ray tracing variable)
