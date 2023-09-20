from lib.file_functions import *
from lib.user_actions_functions import *

admin_id = 1234


def main():
    # Check core_file.
    if verify_core_file() == False:
        add_core_file(admin_id)

    # set user.
    user = initialize_user(admin_id)

    # if user is administrator
    if user == -1:
        print("Welcome, system administrator")

        while True:
            match admin_action():
                case 1:
                    update_core_file()
                case 2:
                    set_date()
                case 3:
                    assign_director()
                case 4:
                    create_message()
                case 5:
                    quit_program()
                case _:
                    print("\nYou need to select an available option\n")

    # If user is student (number is index in dataframe)
    elif user >= 0:
        print("Welcome, student\n")
        while True:
            match student_action():
                case 1:
                    register_title_thesis(user)
                case 2:
                    view_student_information(user)
                case 3:
                    view_dates_thesis(user)
                case 4:
                    quit_program()
                case _:
                    print("\n You need to select an availabe option")


    else:
        input("You don't have access to this program yet.\nAsk to be added to your thesis secretary.\n\nPress enter key to exit")
        quit_program()



if __name__ == "__main__":
    main()
