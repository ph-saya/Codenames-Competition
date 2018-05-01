import sys

from nltk.corpus import wordnet


def hello():
    """Prints hello"""
    print('hello') 


def remove_phrases(candidates):
    """Removes all strings with an _ in the set of candidates"""
    deletion_set = set()
    for string in candidates:
        if '_' in string:
            deletion_set.add(string)
    candidates -= deletion_set
    return candidates


def remove_sets(candidates, list_of_sets):
    for to_be_removed_set in list_of_sets:
        candidates -= to_be_removed_set
    return candidates


def avoid(bad_word, candidates):
    """Propose candidate that is least similar to bad word""" 
    current_best_score = sys.float_info.max
    current_best_word =  ''
    bad_word = wordnet.synsets(bad_word)
    for candidate in candidates:
        candidate_synset = wordnet.synsets(candidate)[0]
        score = bad_word[0].wup_similarity(candidate_synset)
        if score is None:
            continue
        if score < current_best_score:
            current_best_word = candidate
            current_best_score = score 
    return current_best_word
