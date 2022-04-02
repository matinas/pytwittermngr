import user_input
import menu
import list_mngmnt
import auth
import sys
import getopt
import get_access_token

USAGE = '''Options:
    -h --help : print this help
    --generate-access-token : asks the program to generate an access token
    --consumer-key : the twitter consumer key to generate the access token
    --consumer-secret : the twitter consumer secret to generate the access token
    --access-key : the twitter access key in case it has been already generated
    --access-secret : the twitter access secret in case it has been already generated
'''

menu_actions = {
  "1": list_mngmnt.create_mngnt_lists,
  "2": list_mngmnt.query_lists,
  "3": list_mngmnt.process_unfollows,
  "4": list_mngmnt.process_unfollowed,
  "5": list_mngmnt.process_unfollowed_back,
  "6": list_mngmnt.process_unfollowed_me,
  "7": sys.exit
}

def process(selection):
   menu_actions[selection]()

def print_usage_and_exit():
    print(USAGE)
    sys.exit(2)

def print_tokens(consumer_key,consumer_secret,access_key,access_secret):
    print("Consumer key flag: {ck}".format(ck=consumer_key))
    print("Consumer secret flag: {cs}".format(cs=consumer_secret))
    print("Access key flag: {atk}".format(atk=access_key))
    print("Access secret flag: {ats}".format(ats=access_secret))

def main():
    
    try:
        shortflags = '-h'
        longflags = ['help', 'generate-access-token', 'consumer-key=', 'consumer-secret=', 'access-key=', 'access-secret=']
        opts, args = getopt.gnu_getopt(sys.argv[1:], shortflags, longflags)
    except getopt.GetoptError:
        print_usage_and_exit()

    #print("Options: {opt}".format(opt=opts))
    #print("Args: {args}".format(args=args))

    consumer_keyflag = None
    consumer_secretflag = None
    access_keyflag = None
    access_secretflag = None

    generate_token = False
    for o, a in opts:
        if o in ("-h", "--help"):
            print_usage_and_exit()
        if o in ("--generate-access-token"):
            generate_token = True
        if o in ("--consumer-key"):
            consumer_keyflag = a
        if o in ("--consumer-secret"):
            consumer_secretflag = a
        if o in ("--access-key"):
            access_keyflag = a
        if o in ("--access-secret"):
            access_secretflag = a

    #print_tokens(consumer_keyflag,consumer_secretflag,access_keyflag,access_secretflag)
    
    consumer_key = consumer_keyflag or auth.GetConsumerKeyEnv() or auth.GetConsumerKeyHardcoded()
    consumer_secret = consumer_secretflag or auth.GetConsumerSecretEnv() or auth.GetConsumerSecretHardcoded()
    access_key = access_keyflag or auth.GetAccessKeyEnv() or auth.GetAccessKeyHardcoded()
    access_secret = access_secretflag or auth.GetAccessSecretEnv() or auth.GetAccessSecretHardcoded()

    #print_tokens(consumer_key,consumer_secret,access_key,access_secret)

    # if we want the program to generate the token for us, we try to generate them based
    # on the consumer tokens and override the access key values
    if generate_token:
        print("An access token will be generated")
        
        if not consumer_key or not consumer_secret:
            print_usage_and_exit()
        else:
            try:
                tmp_access_key, tmp_access_secret = get_access_token.get_access_token(consumer_key, consumer_secret)
            except ValueError as e:
                print("Access token couldn't be generated. Please check the correctness of the provided consumer token: {0}".format(e))
                sys.exit(2)

            if not tmp_access_key and not tmp_access_secret:
                print("Access token couldn't be generated. The given access keys (environment's or hardcoded) will be used instead...")
            else:
                # override the already read access keys
                access_key = tmp_access_key 
                access_secret = tmp_access_secret
    else:
        print("An access token won't be generated. The given access keys (environment's or hardcoded) will be used instead...")

    if not consumer_key or not consumer_secret or not access_key or not access_secret:
        print("At least one of the tokens is missing. Please check and try again")
        print_usage_and_exit()

    auth.authenticate(consumer_key, consumer_secret, access_key, access_secret)

    if not auth.authenticated():
        print("Authentication failed, please check authentication tokens and try again")
        sys.exit(2)
    else:
        print("User correctly authenticated, starting program...\n")

    while True:
        menu.print_menu()
        m = user_input.read_selection()
        process(m)

if __name__ == '__main__': # this states that if this script is executed, main() will be executed
   main()