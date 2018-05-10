import auth

# There are basically 4 different lists to manage:
# 1. MNG.Main: contains followed-back users who aren't in any of the relevant to-check lists. Unfollows should be controlled in this list (in both directions, users who unfollowed the authenticated user and visceversa)
# 2. MNG.Unfollowed: contains users before in the NPI list who were unfollowed by the authenticated. User unfollows should be controlled in this list (users who unfollowed the authenticated user)
# 3. MNG.Unfollowed.Back: contains users previously in the NPI.Unfollowed list who unfollowed back the authenticated user. This list can be processed in order to get stats about how many unfollowed users unfollowed back auth user (bots?)
# 4. MNG.Unfollowed.Me: contains users before in the NPI list who unfollowed the authenticated user for no apparent reason. This list can be processed in order to get stats about how many users unfollowed auth user (bots?)

mngmnt_lists = {
    "MNG.Main" : "Followed-back users who aren't in any of the relevant lists",
    "MNG.Unfollowed" : "Users previously in the MNG.Main list who were unfollowed by me",
	"MNG.Unfollowed.Back" : "Users previously in the MNG.Unfollowed list who unfollowed me back (bots?)",
	"MNG.Unfollowed.Me" : "Users previously in the MNG list who unfollowed me for no reason (bots?)"
}

# Management lists slug names
MNG_MAIN = "mng-main"
MNG_UNFOLLOWED = "mng-unfollowed"
MNG_UNFOLLOWED_BACK = "mng-unfollowed-back"
MNG_UNFOLLOWED_ME = "mng-unfollowed-me"

# searches the list with name list_name in the set of lists
# returns true if found, false otherwise
def search_list(list_name, lists):
    
    for l in lists:
        if (l.name == list_name):
            return True
    
    return False

# creates the four lists mentioned above , including description and stuff. It's worth noting that the user is the one in charge of filling
# the main NPI list with users as they are friended all the remaining tasks can be done automatically by this bot (unfriending, removing
# users from list, moving users between lists, etc)
def create_mngnt_lists():
    
    lists = auth.api.GetLists()

    for (list_name,list_desc) in mngmnt_lists.items():
        if (not search_list(list_name,lists)):
            auth.api.CreateList(list_name,'private',list_desc)
            print("List %s created successfully" % list_name)
        else:
            print("List %s already exists" % list_name)

# prints the different lists of the authenticated user, including basic stats for each one. This function is useful to check whether the
# management lists were created properly and if they are ready to be processed
def query_lists():
    print("User lists stats")

    if auth.authenticated():
        print("User is authenticated. User lists stats will be listed...")

        lists = auth.api.GetLists()
        i = 0
        for l in lists:
            i = i + 1
            list_dict = l.AsDict()

            print("##### List %d #####" % i)
            print("Name: %s (slug: %s)" % (list_dict["name"], list_dict["slug"]))
            
            if "description" in list_dict:
                print("Description: %s" % list_dict["description"])
            else:
                print("Description: -")

            print("Member count: %s" % list_dict["member_count"])

    else:
        print("Please, check authentication tokens")

# The list slug is the list word in the list URL (e.g.: the slug for the list https://twitter.com/matinassi/lists/mng-main is mng-main and the list owner is matinassi
def get_list_members(slug,user):
    list_members = auth.api.GetListMembers(None,slug,user,None,False,False)

    return list_members

def print_list_stats(list):
    total_members = len(list)
    print("The list has %s members" % total_members)

# processes the NPI list in search of unfollows. For each unfollow it removes the user from this list and add it to the NPI.Unfollowed.Me.
# it also unfollows the user and prints basic information about the process results additionally, it processes unfollowed users and moves
# them to the NPI.Unfollowed list
def process_unfollows():
    print("Process unfollows")

    if auth.authenticated():
        print("User is authenticated. Unfollows will be processed...")

        list_members = get_list_members(MNG_MAIN, auth.get_user_id())
        print_list_stats(list_members)

        u = 0
        following = 0
        not_following_dict = {}
        unfollowed_dict = {}
        for m in list_members:
            u = u + 1
            print("#### User %d ####" % u)
            user_dict = m.AsDict()
            m_id = user_dict["id"]
            m_screename = user_dict["screen_name"]

            # TODO: LookupFriendship() should be a bit more efficient
            friendship_data = auth.api.ShowFriendship(auth.get_user_id(),None,m_id,None) # Check friendship between the two users (the authenticated user and the one on the list)

            src_tar = friendship_data["relationship"]
            src = src_tar["source"]
            
            if src["followed_by"]:
                print("%s IS following!" % m_screename)
                following += 1

                if not src["following"]:
                    # Remove user from this list and pass it to the following list in the pipeline
                    auth.api.DestroyListsMember(None,MNG_MAIN,None,auth.get_user_id(),m_id,None)
                    auth.api.CreateListsMember(None,MNG_UNFOLLOWED,m_id,None,None,auth.get_user_id())
                    print("User %s deleted from %s list and added to %s" % (m_screename,MNG_MAIN,MNG_UNFOLLOWED))

                    unfollowed_dict[m_id] = m_screename
            else:
                print("%s IS NOT following!" % m_screename)
                not_following_dict[m_id] = m_screename
                
                # Unfriend user
                auth.api.DestroyFriendship(m_id,None)
                print("User %s unfriended" % m_screename)

                # Remove user from this list and pass it to the following list in the pipeline
                auth.api.DestroyListsMember(None,MNG_MAIN,None,auth.get_user_id(),m_id,None)
                auth.api.CreateListsMember(None,MNG_UNFOLLOWED_ME,m_id,None,None,auth.get_user_id())
                print("User %s deleted from %s list and added to %s" % (m_screename,MNG_MAIN,MNG_UNFOLLOWED_ME))

        print("Total users following: %s" % following)
        print("Total users NOT following (unfriended and moved): %s %s" % (len(not_following_dict), not_following_dict))
        print("Total users unfollowed: %s %s" % (len(unfollowed_dict), unfollowed_dict))

    else:
        print("Please, check authentication tokens")

# processes the NPI.Unfollowed list in search of unfollows. For each unfollow it removes the user from this list and add it to the
# NPI.Unfollowed.Back. it also prints basic information about the process results
def process_unfollowed():
    print("Process unfollowed")

    if auth.authenticated():
        print("User is authenticated. Unfollowed will be processed...")

        list_members = get_list_members(MNG_UNFOLLOWED, auth.get_user_id())
        print_list_stats(list_members)

        u = 0
        following = 0
        not_following_dict = {}
        for m in list_members:
            u = u + 1
            print("#### User %d ####" % u)
            user_dict = m.AsDict()
            m_id = user_dict["id"]
            m_screename = user_dict["screen_name"]

            # TODO: LookupFriendship() should be a bit more efficient
            friendship_data = auth.api.ShowFriendship(auth.get_user_id(),None,m_id,None) # Check friendship between the two users (the authenticated user and the one on the list)

            src_tar = friendship_data["relationship"]
            src = src_tar["source"]
            
            if not src["followed_by"]:
                print("%s IS NOT following!" % m_screename)
                not_following_dict[m_id] = m_screename
                
                # Unfriend user
                auth.api.DestroyFriendship(m_id,None)
                print("User %s unfriended" % m_screename)

                # Remove user from this list and pass it to the following list in the pipeline
                auth.api.DestroyListsMember(None,MNG_UNFOLLOWED,None,auth.get_user_id(),m_id,None)
                auth.api.CreateListsMember(None,MNG_UNFOLLOWED_BACK,m_id,None,None,auth.get_user_id())
                print("User %s deleted from %s list and added to %s" % (m_screename,MNG_UNFOLLOWED,MNG_UNFOLLOWED_BACK))
            else:
                following += 1

        print("Total users following: %s" % following)
        print("Total users NOT following (and moved): %s %s" % (len(not_following_dict), not_following_dict))

    else:
        print("Please, check authentication tokens")

# processes the NPI.Unfollowed.Back and prints some basic stats
def process_unfollowed_back():
    print("Unfollowed back stats")

    if auth.authenticated():
        print("User is authenticated. Unfollowed back stats will be listed...")

        list_members = get_list_members(MNG_UNFOLLOWED_BACK, auth.get_user_id())
        print_list_stats(list_members)
    else:
        print("Please, check authentication tokens")

# processes the NPI.Unfollowed.Me list and prints some basic stats
def process_unfollowed_me():
    print("Unfollowed stats")

    if auth.authenticated():
        print("User is authenticated. Unfollowed stats will be listed...")

        list_members = get_list_members(MNG_UNFOLLOWED_ME, auth.get_user_id())
        print_list_stats(list_members)
    else:
        print("Please, check authentication tokens")