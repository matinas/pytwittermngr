# Python Twitter Manager

A simple Twitter management application made with [Python Twitter](https://github.com/bear/python-twitter) library and Twitter API which processes different lists of suspicious/unwanted users and check follows/unfollows, remove friendships, move user's through different lists in the pipeline, show stats, etc. The main goal of the application is keep track of eventual bots that a user may follow and some time later they automatically unfollow him. Instead of constantly checking for this kind of cases through the Twitter interface, the program will automatically process user's friendships and make the required actions to avoid the previous scenario to happen (i.e.: a user follows a lot of users/bots which have unfollowed him later)

In oder to obtain some stats from time to time the aplication requires suspicious/unwanted users to be organized in a specific list named MNG.Main. This list will contain users that the user wants to keep track of. Selected users from this list, once processed, will be moved to another list called MNG.Unfollowed.Me, which in turn can be processed to get stats about how many users have unfriended the authenticated user (bots?). A user can also manually unfriend users from the main management list using the Twitter interface, and as part of the main processing the program will move them to another list called MNG.Unfollowed. This list contains users that were unfollowed by the authenticated user but are still following him, so the program will process it in search of users that unfollowed back the authenticated users after he unfriend them. All this sounds somewhat chaotic, so a summary of the required lists can be found below. Note that for a very basic track of suspicious/unwanted users only the MNG.Main has to be processed, without even paying attention to what happens in the other lists.

1. **MNG.Main**: contains followed-back users who aren't in any of the relevant to-check lists unfollows should be controlled in this list (in both sides, list's user unfollows authenticated user and visceversa)
2. **MNG.Unfollowed**: contains users before in the NPI list who were unfollowed by the authenticated user unfollows should be controller in this list (list's users who unfollowed authenticated user)
3. **MNG.Unfollowed.Back**: contains users before in the NPI.Unfollowed list who unfollowed back the authenticated user this list can be processed just in order to get stats about how many unfollowed users unfollowed back auth user (bots?)
4. **MNG.Unfollowed.Me**: contains users before in the NPI list who unfollowed the authenticated user for no reason this list can be processed just in order to get stats about how many users unfollowed auth user after a while (bots?)

The program includes an option to create all these lists automatically after the user has successfully authenticated (option 1 in the menu). For now the lists names must match the ones mentioned, but in the future the user will be able to name their management lists upon convenience.

# How it works

TODO

# How to use it

## Binaries

The most straightforward way to execute the program is using the provided .exe (Win) binary file in the /dist folder. The binary file is generate with PyInstaller for Windows, so it packs together all the needed files to execute the program (you don't even need to have the Python interpreter installed). We can enter the following **arguments to the program**:

- *--generate-access-token* : as Twitter API uses OAuth to authenticate the user, we will need an access token in order to authenticate the user propertly in the app. This flag will state the program that the access token should by generated on-the-fly during execution (some interaction from the user is required though). Check first example below for a step-by-step of the authentication process.
- *--consumer-key* : this is the consumer key used by OAuth. This key can be obtained by creating a new Twitter application in the Twitter application manager. Check [here](https://python-twitter.readthedocs.io/en/latest/getting_started.html#getting-your-application-tokens) for a step-by-step guide on how to generate this token. If not entered, it will use the default consumer key (the one associated with my own test instance of the app)
- *--consumer-secret* : this is the consumer secret used by OAuth. This key can be obtained by creating a new Twitter application in the Twitter application manager. Step-by-step guide on how to generate this token linked above. If not entered, it will use the default consumer secret (the one associated with my own test instance of the app). You should't share this key if you obtained yours.
- *--access-key* : this is the access key used by OAuth. This key can be obtained by creating a new Twitter application in the Twitter application manager and then request the Access Token for the user. Step-by-step guide on how to generate this token linked above. If not entered, the flag --generate-access-token needs to be present so to generate a valid access key.
- *--access-secret* : this is the access secret used by OAuth. This key can be obtained by creating a new Twitter application in the Twitter application manager and then request the Access Token for the user. Step-by-step guide on how to generate this token linked above. If not entered, the flag --generate-access-token needs to be present so to generate a valid access secret.

So, for example the following command will use the default consumer/app token (my own test app instance) and will try to generate the user's access token as automatically as possible. The user will have to enter a PIN-code that will be obtained from a browser that will open during the process:

> *main.exe --generate-access-token*

Once executed, a browser will be opened in order to request the access token to the Twitter backend. Consdering you are already logged into Twitter in that browser (otherwise it will first ask you for credentials), you'll have to give the required permissions to the app:

<img src="https://user-images.githubusercontent.com/5633645/39858693-b4f6bd0a-540d-11e8-9edb-7d9d43b97ce6.png" alt="scene1to7_3" style="max-width:100%">

Once you authorized the app to use some of your account's information you'll receive a PIN code. At this point, the Python program should be asking you to enter this PIN, so copy-paste it or just write it into the commanda line. If all went fine, you should have all set for the app to communicate with your account and the program main menu will be shown.

<img src="https://user-images.githubusercontent.com/5633645/39858697-b7eebaee-540d-11e8-8579-3ebf6f12ed42.png" alt="scene1to7_3" style="max-width:100%">

In case we already have generated our own consumer token and our access token through the Twitter app manager (https://apps.twitter.com/) following the guide linked before, we can include all tokens using the following command:

> *main.exe --consumer-key=YOUR_CONSUMER_KEY_HERE --consumer-secret=YOUR_CONSUMER_SECRET_HERE --access-key=YOUR_ACCESS_TOKEN_HERE --access-secret=YOUR_ACCESS_SECRET_HERE*

## From Source

In case you want to use the application starting from the source code you need to have a few things installed and woking on your system beforehand:

1. [Python 3](https://www.python.org) interpreter
2. [Python Twitter] wrapper for the Twitter API. Check the Installing section on the README; installation is pretty straightforward using the pip install command
3. [Request-OAuth lib] library for managing OAuth request. Check the Installation section on the README; installation is pretty straightforward using the pip install command

Once you have all this installed and working, you can just execute the main module of the Twitter Management App from the command line with the following command:

> *python main.py*

In what refers to passing the required arguments to the program to work, you can use the same flags detailed in the Binaries section above to tell the application whether you need to generate the access token or you will be passing them in another way (flags --generate-access-token, --consumer-key, --consumer-secret, --access-key, and --access-secret). In this case there are a few more ways you can retrieve the required arguments:

1. Tokens module: the *tokens.py* module includes one variable for each one of the required keys. Fill them with the proper values and just execute the program without arguments so it can retrieve them from here.
2. Environment variables: the program also supports setting the keys as OS environment variables. The names should be CONSUMERKEY, CONSUMERSECRET, ACCESSKEY and ACCESSSECRET, for the consumer key, consumer secret, access key and access secret, respectively. If you fill these variables and execute the program with no arguments, even if you have defined the tokens in the *tokens.py* module, the values will be taken from the envionment variables. By the way, this approach should also apply for the binary file execution (except that the environment variables values will be ovewritten in case you pass the values as arguments).
3. If you are using Visual Studio Code, you can install the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and execute the program directly from the IDE. In this scenario, in case you want to pass arguments to the program you'll have to modify the VS Code *launch.json* file , adding an args attribute to the configuration as follows:

<img src="https://user-images.githubusercontent.com/5633645/39859828-95102c02-5411-11e8-8f1f-18098ada5bdd.png" alt="scene1to7_3" style="max-width:100%">
