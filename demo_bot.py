import random
import sys

from nltk.corpus import wordnet
from utils import remove_phrases, remove_sets, avoid

class SpyBot(object):
    """
    This abstract class represents a bot that acts as a spy master for Codenames and can either be asked to
    give a clue to the guesser or be updated about moves made in the game.
    """


    def __init__(self, vocab, game_board, p_id):
        """
        Initialization for the bot
        Args:
            vocab (List<string>): list of English words that can be used to generate clues. No other clue words allowed!
            game_board (Map<string, Enum:WordType>): a dictionary representing the game board, mapping the words on
                the board with an enum representing whether the word belongs to player 1, player 2, is neutral or a spy word.
                See game_platform.py.
            p_id: (int): integer (0, 1) representing the the id of the bot, player 1 or 2.
        """
        pass

    
    def __str__(self):
        return self.__class__

    
    def update(self, is_my_turn, clue_word, clue_num_guesses, guesses):
        """
        Informs the bot with what happened during a turn.
        Args:
            is_my_turn (bool): True if the turn was the bots or the opponent.
            clue_word (str): String representing the clue word in the round.
            clue_num_guesses (int): int representing the number of words that matched the given clue word.
            guesses: (List<string>): list of words that were guessed in the round.
        """
        pass


    def getClue(self, invalid_words):
        """
        Gives a clue for the turn.
        Args:
            invalid_words (Set<string>): set of words from the original vocab that are not allowed to be clued for this
            turn. Eg. words that share a root with any of the face-up words on the board.
        Returns:
            a tuple (clue, num_guesses) where `clue` is a string clue from the given vocab and but not in the set of
            invalid words, and `num_guesses` is the number of words on the board related to the clue.
        """
        pass


# Example of how to write a bot
class RandomBot(SpyBot):

    def __init__(self, vocab, game_board, p_id):
        self.vocab = set(vocab)


    def getClue(self, invalid_words):
        return (random.choice(list(self.vocab.difference(invalid_words))), 2)


"""TODO[1]: implement your bot here that inherits from SpyBot"""
class DumbBot(SpyBot):

    def __init__(self, vocab, game_board, p_id):
        self.vocab = set(vocab)


    def getClue(self, invalid_words):
        return ('dumb' ,1)


class Paul(SpyBot):
    """ """

    def __init__(self, vocab, game_board, p_id):
        # permanent structures
        self.vocab = set(vocab)
        self.words = game_board
        self.p_id = p_id

        # mutable structures  
        self.my_words = set()
        self.their_words = set()
        self.bad_word = ''
        self.given_words = set()

        # Sort words
        for word, team in game_board.items():
            if team == p_id:
                self.my_words.add(word)
                continue
            elif team == (1 - p_id):
                self.their_words.add(word)
                continue
            elif team == 3:
                self.bad_word = word
   
 
    def update(self, is_my_turn, clue_word, clue_num_guesses, guesses):
 
        # Ensure representation of relevant words is updated 
        guess_set = {guess for guess in guesses}
        self.my_words -= guess_set     
        self.their_words -= guess_set

        self.given_words.add(clue_word)
    

    def getClue(self, invalid_words):
        synonym_set = set()

        # Keep thinking until one has an idea
        while len(synonym_set) < 1:
            
            # Select one word to focus on
            mind_word = random.sample(self.my_words, 1)[0] 

            # Find similar words
            synonyms = wordnet.synsets(mind_word)
            for syn in synonyms:
               synonym_set.add(syn.lemmas()[0].name().lower())
            # Ensure they are valid
            synonym_set = remove_sets(synonym_set, \
                                    [invalid_words, self.my_words, self.their_words])
            synonym_set = remove_phrases(synonym_set)
        assert(len(synonym_set) > 0)

        # Make selection based on dissimilarity to bad word
        current_best_word = avoid(self.bad_word, synonym_set)    
        word = current_best_word 

        # Ensure selection is still similar to answer
        if word in synonym_set:
            synonym_set.remove(word)
        else:
            word = synonym_set.pop()

        return (word.lower() ,1)

