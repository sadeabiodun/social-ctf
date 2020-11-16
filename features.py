from os.path import join
import numpy as np
from ctf_dataset.load import create_wrapped_dataset
from ctf_dataset.info import events as event_names

base_dir = '/mnt/bucket/labs/hasson/snastase/social-ctf'
data_dir = join(base_dir, 'data')

# Create wrapped CTF dataset
wrap_f = create_wrapped_dataset(data_dir, output_dataset_name="virtual.hdf5")

map_id = 0 # 0
matchup_id = 0 # 0-54
repeat_id = 0 # 0-7
player_id = 0 # 0-3

# Convenience function to extract event array and labels
def get_events(wrap_f, map_id=0, matchup_id=0,
               repeat_id=0, player_id=0, time_id=slice(None)):
    
    # Extract events for a given game and time slice
    events = wrap_f['map/matchup/repeat/player/time/events'][
        map_id, matchup_id, repeat_id, player_id, time_id
    ]

    # Get the evennt labels
    event_labels = [e.name.lower().replace('ctf', 'CTF').replace('_', ' ')
                    for e in event_names.Events]
    
    # Get a subset of all events if requested
    assert events.shape[1] == len(event_labels)

    return events, event_labels


# Convenience function to extract action array and labels
def get_actions(wrap_f, map_id=0, matchup_id=0,
                repeat_id=0, player_id=0, time_id=slice(None)):

    actions = wrap_f['map/matchup/repeat/player/time/action'][
        map_id, matchup_id, repeat_id, player_id, time_id
    ]
    
    action_labels = ['look left/right', 'look up/down',
                     'strafe left/right', 'move backward/forward',
                     'fire or switch', 'jump']
    
    return actions, action_labels


# Convenience function to extract position
def get_position(wrap_f, map_id=0, matchup_id=0,
                  repeat_id=0, player_id=0, time_id=slice(None)):
    
    position = wrap_f['map/matchup/repeat/player/time/position'][
        map_id, matchup_id, repeat_id, player_id, time_id
    ]
    
    position_labels = ['x', 'y', 'z']
    
    return position, position_labels


# Convenience function to extract health
def get_health(wrap_f, map_id=0, matchup_id=0,
               repeat_id=0, player_id=0, time_id=slice(None)):
    
    health = wrap_f['map/matchup/repeat/player/time/health'][
        map_id, matchup_id, repeat_id, player_id, time_id
    ]
    
    health_label = ['health']
    
    return health, health_label


# Convenience function to extract game scores
def get_score(wrap_f, team=None, map_id=0, matchup_id=0,
               repeat_id=0, time_id=slice(None)):
    
    if team and team not in ['red', 'blue']:
        raise Exception(f"Invalid team label '{team}'; "
                        "must be 'red' or 'blue'")
    elif team:
        score = wrap_f[f'map/matchup/repeat/time/{team}_team_score'][
            map_id, matchup_id, repeat_id, time_id
        ]
        
        score_labels = [f'{team} score']
        
    else:
        red_score = wrap_f[f'map/matchup/repeat/time/red_team_score'][
            map_id, matchup_id, repeat_id, time_id
        ]
        blue_score = wrap_f[f'map/matchup/repeat/time/blue_team_score'][
            map_id, matchup_id, repeat_id, time_id
        ]
        score = np.column_stack((red_score, blue_score))
    
        score_labels = ['red score', 'blue score']
        
    return score, score_labels


# Convenience function to extract flag position
def get_flags(wrap_f, team=None, map_id=0, matchup_id=0,
               repeat_id=0, time_id=slice(None)):
    
    if team and team not in ['red', 'blue']:
        raise Exception(f"Invalid team label '{team}''; "
                        "must be 'red' or 'blue'")
    elif team:
        position = wrap_f[f'map/matchup/repeat/time/{team}_flag_position'][
            map_id, matchup_id, repeat_id, time_id
        ]

        status = wrap_f[f'map/matchup/repeat/time/{team}_flag_status'][
            map_id, matchup_id, repeat_id, time_id
        ]

        flags = np.column_stack((position, status))

        flag_labels = [f'{team} flag x', f'{team} flag y',
                       f'{team} flag z', f'{team} flag status']

    else:
        flags, flag_labels = [], []
        for team in ['red', 'blue']:
            position = wrap_f[f'map/matchup/repeat/time/{team}_flag_position'][
                map_id, matchup_id, repeat_id, time_id
            ]

            status = wrap_f[f'map/matchup/repeat/time/{team}_flag_status'][
                map_id, matchup_id, repeat_id, time_id
            ]

            flags.extend([position, status])
            flag_labels.extend([f'{team} flag x', f'{team} flag y',
                       f'{team} flag z', f'{team} flag status'])

        flags = np.column_stack(flags)
        
    return flags, flag_labels


# Convenience function to get multiple features ('design matrix')
def get_features(wrap_f, feature_set=None, team=None, map_id=0,
                 matchup_id=0, repeat_id=0, player_id=0, time_id=slice(None)):

    if not feature_set:
        feature_set = ['events', 'actions', 'position',
                          'health', 'score', 'flags']

    features, feature_labels = [], []

    if 'events' in feature_set:
        events, event_labels = get_events(wrap_f, map_id=map_id,
                                          matchup_id=matchup_id,
                                          repeat_id=repeat_id,
                                          player_id=player_id,
                                          time_id=time_id)
        features.append(events)
        feature_labels.extend(event_labels)

    if 'actions' in feature_set:
        actions, action_labels = get_actions(wrap_f, map_id=map_id,
                                             matchup_id=matchup_id,
                                             repeat_id=repeat_id,
                                             player_id=player_id,
                                             time_id=time_id)
        features.append(actions)
        feature_labels.extend(action_labels)

    if 'position' in feature_set:
        position, position_labels = get_position(wrap_f, map_id=map_id,
                                                 matchup_id=matchup_id,
                                                 repeat_id=repeat_id,
                                                 player_id=player_id,
                                                 time_id=time_id)
        features.append(position)
        feature_labels.extend(position_labels)

    if 'health' in feature_set:
        health, health_labels = get_health(wrap_f, map_id=map_id,
                                           matchup_id=matchup_id,
                                           repeat_id=repeat_id,
                                           player_id=player_id,
                                           time_id=time_id)
        features.append(health)
        feature_labels.extend(health_labels)

    if 'score' in feature_set:
        score, score_labels = get_score(wrap_f, team=team, map_id=map_id,
                                          matchup_id=matchup_id,
                                          repeat_id=repeat_id,
                                          time_id=time_id)
        features.append(score)
        feature_labels.extend(score_labels)

    if 'flags' in feature_set:
        flags, flag_labels = get_flags(wrap_f, team=team, map_id=map_id,
                                       matchup_id=matchup_id,
                                       repeat_id=repeat_id,
                                       time_id=time_id)
        features.append(flags)
        feature_labels.extend(flag_labels)

    features = np.column_stack(features)

    return features, feature_labels

features, feature_labels = get_features(wrap_f)