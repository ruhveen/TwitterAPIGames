from utils.wordnet_wrapper import WordnetWrapper
from models.unified_group import UnifiedGroup
from utils.environment_consts import DEBUG_MODE
import json
from datetime import datetime
SECONDS_INTERVAL = 2
TOP_N_GROUPS = 5


class BusinessLogic(object):
    '''
    Main class that handles words from the Twitter API -
    Adds them to the appropriate structure while keeping them sorted by their weight
    '''
    top_n_groups = TOP_N_GROUPS

    # Dictionary of word to the group object that contains it
    word_to_group = {}

    # Sortet group list
    sorted_groups = []

    start_timestamp = datetime.now()
    last_timestamp_was_printed = None

    @staticmethod
    def handle_groups(words):

        for word in words:

            # If the word is found in one of the groups
            if word in BusinessLogic.word_to_group:

                # Get the group that contains the word
                curr_group = BusinessLogic.word_to_group[word]

                # Add the new word to it
                curr_group.add_word(word)

            # If the word is not in any of the groups
            else:

                # Get all lemmas of the word
                lemmas = WordnetWrapper.get_all_lemmas(word)

                # If lemmas were found, (It might be 0 if it is a verb,
                # and per task instructions - it supposed to handle only nouns)
                if len(lemmas) > 0:

                    group_that_contains_lemma = None
                    for lemma in lemmas:
                        if lemma in BusinessLogic.word_to_group:
                            group_that_contains_lemma = BusinessLogic.word_to_group[lemma]

                    if group_that_contains_lemma is not None:
                        group_that_contains_lemma.add_lemmas(lemmas)
                        for lemma in lemmas:
                            BusinessLogic.word_to_group[lemma] = group_that_contains_lemma

                        group_that_contains_lemma.add_word(word)


                    else:

                        # Create a new unified group of all the synnonims of all the synsets of the word
                        new_group = UnifiedGroup(word, lemmas)

                        # If this is the first group
                        if len(BusinessLogic.sorted_groups) == 0:
                            BusinessLogic.sorted_groups = [new_group]
                        else:
                            BusinessLogic.sorted_groups = [new_group] + BusinessLogic.sorted_groups

                        # Add every word in the new unified group to the word to group dictionary
                        # So that every word points to the new group
                        for word in lemmas:
                            try:

                                BusinessLogic.word_to_group[word] = new_group
                            except Exception as err:
                                print "Exception when setting new word to group: %s" % err
                else:

                    # Probably it is not a noun
                    if DEBUG_MODE:
                        print "Word: '%s' didn't return lemmas, probably it is not a noun" % word

        try:

            # Sort all of the groups according to the new weight,
            # VERY IMPORTANT - Obviously this could have been done much more efficent,
            # Maybe with a red black tree which everytime I add the word it automatically stays balanced
            # and there's no need to sort everything in O(N) every time, but I didn't want to spend any more
            # Time on this task.
            BusinessLogic.sorted_groups.sort(key=lambda group: group.calculate_weight(),reverse = True)
        except  Exception as err:
            print err

        now = datetime.now()

        if ((now - BusinessLogic.start_timestamp).seconds % SECONDS_INTERVAL == 0):

            # Make sure it prints only once every SECONDS_INTERVAL seconds
            if BusinessLogic.last_timestamp_was_printed is None or\
                ((now - BusinessLogic.last_timestamp_was_printed).seconds >= SECONDS_INTERVAL):

                BusinessLogic.print_all_groups(now)
                BusinessLogic.last_timestamp_was_printed = now


    @staticmethod
    def print_all_groups(now):

        print '\n\n%s | ' % now + ('=' * 100)
        for group in BusinessLogic.sorted_groups[:BusinessLogic.top_n_groups]:
            print '\nGroup ID: %s | Weight: %s | Created: %s | Newest Word Timestamp: %s | First Word: %s | \nWords: %s' %\
                  (group.id, group.calculate_weight(), group.created, group.newest_word_timestamp,
                   group.first_word.text, json.dumps(group.lemmas_with_count()))