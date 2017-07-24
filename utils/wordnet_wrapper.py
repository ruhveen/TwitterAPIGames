from nltk.corpus import wordnet as wn
import nltk
nltk.data.path.append('./nltk_data/')
WORDNET_ENGLISH_LANGUAGE_ID = "eng"


class WordnetWrapper(object):
    '''
    Wraps all interaction with the wordnet
    '''

    @staticmethod
    def get_all_lemmas(word):
        '''
        Returns all the lemmas of a word -
        as per task instructions - unifies all the lemmas of all the sysnets of the given word
        :param word: word to search
        :return: unified lemmas
        '''

        unified_lemmas_group = []
        res = wn.synsets(word,pos=wn.NOUN,lang=WORDNET_ENGLISH_LANGUAGE_ID)

        for synset in res:
            for lemma in synset.lemma_names(WORDNET_ENGLISH_LANGUAGE_ID):
                if lemma not in unified_lemmas_group and lemma.isalpha():
                    unified_lemmas_group.append(lemma)
        return unified_lemmas_group


# TESTING:
# print WordnetWrapper.get_all_lemmas('Test')

# if __name__ == '__main__':
#     word = 'Help'
#     res = wn.synsets(word)
#
#     print "The word: %s is a member of %s synsets\n" % (word, len(res))
#
#     for synset in res:
#         print "for %s the similar words are(lemmas): %s" % (synset, synset.lemma_names())
    # print res



