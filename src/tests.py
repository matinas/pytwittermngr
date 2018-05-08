# App ID: https://apps.twitter.com/app/15198165

from __future__ import print_function
import twitter

# TODO: pass all this tokens to another separate module and remove the access token and secret before uploading it to Github (then add that file to gitignore)

CONSUMER_KEY = "Le4PLopQivit4bwvhom5ciaW4"
CONSUMER_SECRET = "tfRPndldozZAIJVSUEePPreHCQiKVo1544qN0Nw2bmQsUkeWA2"
ACCESS_TOKEN = "146348980-qbDwLyyY90MyFaLxHOzzHyOjUL2Q6xzO2kw8M0gK"
ACCESS_TOKEN_SECRET = "RVTmh3nBVRsX8Im45xnfXLEoYVb255aerN8naeZBaWE2a"
SLEEP_ON_RATE_LIMIT = False

# TODO: the authentication token and secret should be retrieved someway given the credentials of the user or something
# Some functions that may be useful: SetCredentials, VerifyCredentials, GetAppOnlyAuthToken

# To use authentication, instantiate the twitter.Api class with a consumer key and secret; and the oAuth key and secret
api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET,
                  sleep_on_rate_limit=True)

user = api.GetUser()
print("Usuario: " + user)

# TODO: get the userID from the user's data so we avoid hardcoding it later

lists = api.GetLists()

i = 0
for l in lists:
    i = i + 1
    print("##### List %d #####" % i)
    list_dic = l.AsDict()
    for field,value in list_dic.items():
        print("Field: %s | Value %s" % (field,value))

# The list slug is the list word in the list URL. For example, the slug is npi for the
# list https://twitter.com/matinassi/lists/npi, and the list owner is matinassi

list_members = api.GetListMembers(None,"npi",146348980,None,False,False) # TODO: replace my hardcoded ID by the one obtained at the beginning
total_members = len(list_members)
print("The list has %s members" % total_members)
u = 0
following = 0
not_following_dict = {}
for m in list_members:
    u = u + 1
    print("#### User %d ####" % u)
    user_dict = m.AsDict()
    m_id = user_dict["id"]
    m_screename = user_dict["screen_name"]

    friendship_data = api.ShowFriendship(146348980,None,m_id,None) # Check friendship between the two users (the authenticated user and the one on the list)
    # TODO: Try this one in case is more efficient: LookupFriendship(user_id=None, screen_name=None, return_json=False

    src_tar = friendship_data["relationship"]
    src = src_tar["source"]
    
    if src["followed_by"]:
        print("%s IS following!" % m_screename)
        following += 1
    else:
        print("%s IS NOT following!" % m_screename)
        not_following_dict[m_id] = m_screename
        # TODO: DestroyFriendship(user_id=None, screen_name=None) or UpdateFriendship(user_id=None, screen_name=None, follow=True, retweets=True, **kwargs) # Befriend this user
        # TODO: Remove it from this list and pass it to the following list in the flow

print("Total users following: %s" % following)
print("Total users NOT following: %s %s" % (len(not_following_dict), not_following_dict))