from tweepy.streaming import StreamListener
import json
import time
from utils.environment_consts import DEBUG_MODE
LANG_PARAMETER_NAME = "lang"
ENGLISH_LANGUAGE_ID = "en"
TEXT_PARAMETER_NAME = "text"


class TwitterWrapper(StreamListener):
    '''
    Wrapps all interaction with the Twitter API
    '''

    def __init__(self, on_data_handler):
        '''
        :param on_data_handler: Handler to be invoked everytime the on_data event is raised
         By the Twitter Stream API
        :return:
        '''
        self.on_data_handler = on_data_handler

    @staticmethod
    def filter_non_words(potential_words):
        '''
        Filter out sequence of characters that are not words according the isalpha
                obviously if this was production code it would have been much more accurate.
        :param potential_words:
        :return: real words
        '''
        return [word for word in potential_words if word.isalpha()]

    def on_data(self, data):
        '''
        handler for the on_data event from Twitter API,
        invokes the self.on_data_handler with the tokenized words and runs each
        SECONDS_INTERVAL seconds
        :param data: the data from Twitter
        :return:
        '''

        res = json.loads(data)
        if LANG_PARAMETER_NAME in res:

            # Status is in english
            if res[LANG_PARAMETER_NAME]==ENGLISH_LANGUAGE_ID:

                tokenized_words = res[TEXT_PARAMETER_NAME].split(' ')
                tokenized_words = TwitterWrapper.filter_non_words(tokenized_words)
                if DEBUG_MODE:
                    print "Current Tokenized Words: %s" % json.dumps(tokenized_words)

                self.on_data_handler(tokenized_words)
                # time.sleep(SECONDS_INTERVAL)

            # Data is not in english, Ignore it
            else:
                if DEBUG_MODE:
                    print "Data is not english, Ignoring"

        # Stream structure is not a Twitter status structure, Ignore it
        else:
            if DEBUG_MODE:
                print "%s parameter was not found, Ignoring" % LANG_PARAMETER_NAME

        return True

    def on_error(self, status):
        print "ERROR:"
        print status

    def on_status(self, status):
        print "STATUS:"
        print status.text
