import twitter
import tokens
import os
import sys

SLEEP_ON_RATE_LIMIT = True # Set this to True in case we want to sleep for a while on a RATE_LIMIT_EXCEEDED msg from Twitter API instead of return an error msg

def GetConsumerKeyEnv():
    return os.environ.get("CONSUMERKEY", None)

def GetConsumerKeyHardcoded():
    return tokens.CONSUMER_KEY

def GetConsumerSecretEnv():
    return os.environ.get("CONSUMERSECRET", None)

def GetConsumerSecretHardcoded():
    return tokens.CONSUMER_SECRET 

def GetAccessKeyEnv():
    return os.environ.get("ACCESSKEY", None)

def GetAccessKeyHardcoded():
    return tokens.ACCESS_TOKEN_KEY

def GetAccessSecretEnv():
    return os.environ.get("ACCESSSECRET", None)

def GetAccessSecretHardcoded():
    return tokens.ACCESS_TOKEN_SECRET

api = None
auth_user_id = None

def authenticate(consumer_key, consumer_secret, access_token_key, access_token_secret):

    global api, auth_user_id

    try:

        # To use authentication, instantiate the twitter.Api class with a consumer key and secret; and the oAuth key and secret
        api = twitter.Api(consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=access_token_key,
                          access_token_secret=access_token_secret,
                          sleep_on_rate_limit=SLEEP_ON_RATE_LIMIT)

        auth_user = api.VerifyCredentials()
        auth_user_id = auth_user.AsDict()["id"] # Get authenticated user ID to use from now on

    except twitter.TwitterError:
        print("Couldn't verify credentials")

def get_user_id():

    global auth_user_id

    if not auth_user_id:
        if api:
            auth_user = api.VerifyCredentials()
            auth_user_id = auth_user.AsDict()["id"] # Get authenticated user ID to use from now on
        else:
            print("Can't get user ID because it's not correctly authenticated. Please check authentication")
            return None

    return auth_user_id
        
def authenticated():

    return auth_user_id != None