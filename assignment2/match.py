import numpy as np
from typing import List, Tuple

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    proposers_indexes = []
    receivers_indexes = []
    
    # split into proposers and recievers
    for i in range(len(gender_id)):
        if i < len(gender_id)/2:
            receivers_indexes.append(i)
        else:
            proposers_indexes.append(i)
    
    # take care of pairs that shouldn't be coupled this is probs not the optimal way to do this but oh well
    for i in proposers_indexes:
        for j in receivers_indexes:
            if gender_id[i] == "Male" and gender_pref[i] == "Women":
                if gender_id[j] == "Male" or gender_pref[j] == "Women":
                    scores[i][j] = 0
                    scores[j][i] = 0
            elif gender_id[i] == "Female" and gender_pref[i] == "Men":
                if gender_id[j] == "Female" or gender_pref[j] == "Men":
                    scores[i][j] = 0
                    scores[j][i] = 0
            elif gender_id[i] == "Male" and gender_pref[i] == "Men":
                if gender_id[j] == "Female" or gender_pref[j] == "Women":
                    scores[i][j] = 0
                    scores[j][i] = 0
            elif gender_id[i] == "Female" and gender_pref[i] == "Women":
                if gender_id[j] == "Male" or gender_pref[j] == "Men":
                    scores[i][j] = 0
                    scores[j][i] = 0
            elif gender_id[i] == "Female" and gender_pref[j] == "Men":
                scores[i][j] = 0
                scores[j][i] = 0
            elif gender_id[i] == "Male" and gender_pref[j] == "Women":
                scores[i][j] = 0
                scores[j][i] = 0
            elif gender_pref[i] == "Men" and gender_id[j] == "Female":
                scores[i][j] = 0
                scores[j][i] = 0
            elif gender_pref[i] == "Women" and gender_id[j] == "Male":
                scores[i][j] = 0
                scores[j][i] = 0
                
    unmatched_proposers = []
    for i in range(len(proposers_indexes)):
        unmatched_proposers.append(proposers_indexes[i])
    unmatched_receivers = []
    for i in range(len(receivers_indexes)):
        unmatched_receivers.append(receivers_indexes[i])
        
    test_matches = []
#ahhh forgot commenting was a thing whoops anyways i think this does it 
    while unmatched_proposers:
        preferences = []
        for i in receivers_indexes:
            preferences.append(scores[unmatched_proposers[0]][i])
            
        sort_order = np.argsort(preferences)

        for i in sort_order:
            if i in unmatched_receivers:
                test_matches.append((i, unmatched_proposers[0]))
                unmatched_receivers.pop(unmatched_receivers.index(i))
                break
            index_to_beat = -1
            for j in range(len(test_matches)):
                if test_matches[j][0] == i:
                    index_to_beat = test_matches[j][1]
                    break
                    
            score_to_beat = scores[i][index_to_beat]
                        
            if preferences[i] > score_to_beat:
                test_matches.append((i, unmatched_proposers[0]))
                print(unmatched_receivers, i)
                unmatched_receivers.pop(unmatched_receivers.index(i))
                test_matches.pop(test_matches.index(i, index_to_beat))
                unmatched_proposers.append(index_to_beat)
        unmatched_proposers.pop(0)
    
    matches = test_matches
    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
