import twitter
import tokens

api = {}

# TODO: check it the authentication token and secret can be retrieved someway given the credentials of the user or something (without the need of creating a Twitter app)
# Some functions that that might be useful: SetCredentials, VerifyCredentials, GetAppOnlyAuthToken

# To use authentication, instantiate the twitter.Api class with a consumer key and secret; and the oAuth key and secret
api = twitter.Api(consumer_key=tokens.CONSUMER_KEY,
                  consumer_secret=tokens.CONSUMER_SECRET,
                  access_token_key=tokens.ACCESS_TOKEN,
                  access_token_secret=tokens.ACCESS_TOKEN_SECRET,
                  sleep_on_rate_limit=tokens.SLEEP_ON_RATE_LIMIT)

auth_user = api.VerifyCredentials()
auth_user_id = auth_user.AsDict()["id"] # Get authenticated user ID to use from now on

def authenticated():
    return api != ""