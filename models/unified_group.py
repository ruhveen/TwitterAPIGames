from datetime import datetime
from word import Word
SECONDS_TO_CHECK = 60


class UnifiedGroup(object):
    '''
    Represents a unified group of all of the lemmas of all of the sysnsets of a specific word
    '''
    latest_group_id = 1

    def __init__(self, new_word_text, lemmas):
        '''
        Constructor
        :param new_word_text: the new word
        :param lemmas: All of the The lemmas of the word (Of all of the synsets
        the word appeared in)
        :return:
        '''
        self.created = datetime.now()
        self.lemmas = [lemma.lower() for lemma in lemmas]
        new_word = Word(new_word_text.lower())
        self.words = [new_word]
        self.id = UnifiedGroup.latest_group_id
        self.newest_word_timestamp = new_word.timestamp
        self.first_word = new_word
        UnifiedGroup.latest_group_id+=1

    def add_word(self, new_word_text):
        new_word = Word(new_word_text.lower())
        self.words.append(new_word)
        self.newest_word_timestamp = new_word.timestamp

    def calculate_weight(self):
        '''
        Removes all words that were not added in the past SECONDS_TO_CHECK
        VERY IMPORTANT: This could also be more efficient, I could use a datastructure that would always
        have the relevant words - for example expiringdict But I didn't want to spend more time on this task.
        :return:
        '''
        self.words = [word for word in self.words if (datetime.now() - word.timestamp).seconds < SECONDS_TO_CHECK]
        return len(self.words)

    def lemmas_with_count(self):
        '''
        Returns a dictionary with each lemma in the group and the number of times it appears
        :return:
        '''
        lemmas_with_count = {lemma:0 for lemma in self.lemmas}

        for word in self.words:
            if word.text in lemmas_with_count:
                lemmas_with_count[word.text] +=1

        return lemmas_with_count


