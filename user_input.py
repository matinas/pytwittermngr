# reads and sanitizes the user menu selection
def read_selection():

    #raw_input is no longer available in Python 3.x, it was renamed input
    option = input("Please selected an option: ")

    # TODO: sanitize input (it should be a number falling between the available options, etc)

    return option

    