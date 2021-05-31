from os.path import join
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ctf_dataset.load import create_wrapped_dataset
from features import get_features

#import luke's heuristics functions 
from ctf_dataset.behaviours.heuristic import near_teammate
from ctf_dataset.behaviours.heuristic import camp_own_base, camp_opponent_base, running_forwards, running_backwards, approaching_own_base, approaching_opponent_base, approaching_own_flag, approaching_opponent_flag, approaching_teammate


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
following_sam = get_following(wrap_f, matchup_id=0, repeat_id=0)

#testing luke's following function 
following_luke = near_teammate(wrap_f, map_id=0, matchup_id=0, repeat_id=0,
                         min_behaviour_length=30, teammate_radius=2)

## Plotting to verify 

plt.plot(following_sam[0].T, label='sam p1')
plt.plot(following_sam[1].T, label='sam p2')

# Plotting Luke's 
fig, axs = plt.subplots(6,1)
axs[0].plot(following_luke[0,:,0])
axs[1].plot(following_luke[1,:,0])
axs[2].plot(following_luke[2,:,0])
axs[3].plot(following_luke[3,:,0])
axs[4].plot(following_sam[0,:])
axs[5].plot(following_sam[1,:])

# Compare Sam and Luke's directly 
# It appears that Luke's function takes account of isalive and this limits the time courses for following (as it should be)

fig, axs = plt.subplots(2,1)
axs[0].plot(following_luke[0,:500,0], label='luke')
axs[1].plot(following_sam[0,:500], label='sam')
plt.legend()

from animations import time_series_animation
from IPython.display import Video

## Testing basecamping functions 

camp_own = camp_own_base(wrap_f, map_id=0, matchup_id=0, repeat_id=0,
                         min_behaviour_length=15, base_radius=1)

# Plot 

fig, axs = plt.subplots(4,1)
axs[0].plot(camp_own[0,:,0], label='p1')
axs[1].plot(camp_own[1,:,0], label='p2')
axs[2].plot(camp_own[2,:,0], label='p3')
axs[3].plot(camp_own[3,:,0], label='p4')
fig.legend()

## Animation 
map_id = 0
matchup_id = 0
repeat_id = 0
anim = time_series_animation(camp_own[[0,2],:,0], wrap_f, map_id=map_id, matchup_id=matchup_id, repeat_id=repeat_id, label='basecamping')


anim.save(f'figures/time_series_animation_basecamping_min-br_m{matchup_id}_'
          f'r{repeat_id}.mp4', dpi=90)

Video(f'figures/time_series_animation_basecamping_min-br_m{matchup_id}_' f'r{repeat_id}.mp4')

## Testing basecamping functions 

camp_opp = camp_opponent_base(wrap_f, map_id=0, matchup_id=0, repeat_id=0,
                         min_behaviour_length=15, base_radius=1)

# Plot 

fig, axs = plt.subplots(4,1)
axs[0].plot(camp_opp[0,:,0], label='p1')
axs[1].plot(camp_opp[1,:,0], label='p2')
axs[2].plot(camp_opp[2,:,0], label='p3')
axs[3].plot(camp_opp[3,:,0], label='p4')
fig.legend()

## Animation 
map_id = 0
matchup_id = 0
repeat_id = 0
anim = time_series_animation(camp_opp[[0,2],:,0], wrap_f, map_id=map_id, matchup_id=matchup_id, repeat_id=repeat_id, label='spawncamping')


anim.save(f'figures/time_series_animation_spawncamping_min-br_m{matchup_id}_' f'r{repeat_id}.mp4', dpi=90)

Video(f'figures/time_series_animation_spawncamping_min-br_m{matchup_id}_' f'r{repeat_id}.mp4')

### It appears that what we're categorizing as 'spawncamping' might actually be being 'trapped' at opponent's plate after flag capture but before being killed. A kill follows almost every instance of 'spawncamping'


