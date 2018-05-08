import user_input
import menu
import list_mngmnt
import auth

menu_actions = {
  "1": list_mngmnt.create_mngnt_lists,
  "2": list_mngmnt.query_lists,
  "3": list_mngmnt.process_unfollows,
  "4": list_mngmnt.process_unfollowed,
  "5": list_mngmnt.process_unfollowed_back,
  "6": list_mngmnt.process_unfollowed_me,
}

def process(selection):
   menu_actions[selection]()

def main():
    
    while True:
        menu.print_menu()
        m = user_input.read_selection()
        if (m == "7"):
            break
        process(m)

if __name__ == '__main__': # this states that if this script is executed, main() will be executed
   main()