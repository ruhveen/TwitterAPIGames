from utils.twitter_wrapper import TwitterWrapper
from business_logic import BusinessLogic, TOP_N_GROUPS

from tweepy import OAuthHandler
from tweepy import Stream

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""

def get_user_input(parameter_name, default_value):
    user_input = raw_input("Please enter %s or press enter to use default value (%s)" %
                                  (parameter_name, default_value))
    if user_input:
        return user_input
    else:
        return default_value

if __name__ == '__main__':

    access_token = get_user_input('access_token', ACCESS_TOKEN)
    access_token_secret = get_user_input('access_token_secret', ACCESS_TOKEN_SECRET)
    consumer_key = get_user_input('consumer_key', CONSUMER_KEY)
    consumer_secret = get_user_input('consumer_secret', CONSUMER_SECRET)
    top_n_groups = get_user_input('TOP_N_GROUPS', TOP_N_GROUPS)

    print "Starting..."

    # This handles Twitter authetification and the connection to Twitter Streaming API
    BusinessLogic.top_n_groups = int(top_n_groups)
    l = TwitterWrapper(BusinessLogic.handle_groups)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.sample()