import sys
import os
from validate_email import validate_email
import shutil
import csv
import pandas as pd
import re
from datetime import datetime

admin_id = 1234


def main():
    # Check core_file.
    if verify_core_file() == False:
        add_core_file()

    # set user.
    user = initialize_user()

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







#FILE FUNCTIONS:
def add_core_file(admin_id):
    """Asks for administrator password (3 attempts) and, if logged in, asks if want to add a core file to the ./csv_files/core_csv_file path"""

    count = 0
    while count < 3:
        password = input(
            f"You need to be administrator in order to use this software for the first time.\nType your password ({3-count} attempts remaining): "
        )
        if int(password) == admin_id:
            have_file = input(
                "Do you want to add a file with students and professors data?\n"
            ).lower()
            if have_file in ["yes", "y"]:
                file = get_file()
                if check_column_names(file):
                    core_file_name = "./csv_files/core_csv_file/core.csv"
                    shutil.copy(file, core_file_name)
                    create_general_file()
                    print("Core file added and general file created")
                    return core_file_name
                else:
                    #raise ValueError("Incorrect column names")
                    sys.exit("Exiting program")

            else:
                sys.exit("No data\ninterrupting program\n...\n...\n...")

        else:
            print("Incorrect password")
            count += 1

    quit_program()

def check_column_names(file):
    """Verifies if core file has columns: name, id and mail"""
    with open(file, "r") as core_file:
        reader = csv.reader(core_file)
        rows = [i for i in reader]
        column_names = (i for i in rows[0])
        if "name" in column_names and "id" in column_names and  "mail" in column_names:
            return True

        else:
            input("Your file has to have the following columns names:\nname\nid\nrol\nmail\nPlease check your column names and retry\n\nPress enter key to continue")
            return False





def create_general_file():
    """Create a general file (file with thesis information), from core file"""

    path_general = "./csv_files/general_file/general.csv"
    path_core = "./csv_files/core_csv_file/core.csv"
    csv_row_titles = [
        "title",
        "id_author",
        "author",
        "mail_author",
        "director",
        "director_mail",
        "project_date",
        "project_correction_date",
        "Thesis_date",
        "thesis_correction_date",
        "Dissertation_date",
    ]

    # Open core file an general file
    with open(path_core, "r") as core_file:
        with open(path_general, "w") as general_file:
            # create a dict writer for general file
            writer_general = csv.DictWriter(general_file, fieldnames=csv_row_titles)
            writer_general.writeheader()

            # Create a dict reader for core file
            reader_core = csv.DictReader(core_file)

            # copy every row, from core to general file
            for i in reader_core:
                writer_general.writerow(
                    {
                        "id_author": i["id"],
                        "author": i["name"],
                        "mail_author": i["mail"],
                    }
                )

def get_general_file():
    """Returns the last general file saved in the corresponding folder"""

    path_general = "./csv_files/general_file/general.csv"
    general_file = pd.read_csv(path_general)
    # Dissable warning when assigning values in a direct copy:
    pd.options.mode.chained_assignment = None
    return general_file

def get_file():
    """Prompts the user for a file path and returns that path if there is file, otherwise loops"""

    while True:
        file_path = input("Write file path:\n")
        if os.path.isfile(file_path):
            return file_path
        print("Not such file or directory")


def save_general_file(file):
    """saves or updates the general file in the corresponding folder"""

    file.to_csv("./csv_files/general_file/general.csv", index=False)


def update_core_file():
    """Updates core file in correspondig path"""

    new_file = get_file()
    if check_column_names(new_file):
        core_file_name = "./csv_files/core_csv_file/core.csv"
        shutil.copy(new_file, core_file_name)
        input("Core file updated\nPress enter key to continue")




def verify_core_file():
    """Verifies if there is core.csv file in ./csv_files/core_csv_file path"""

    folder_path = "./csv_files/core_csv_file"
    file_name = "core.csv"
    file_path = os.path.join(folder_path, file_name)

    # If no files in corresponding folder, print warning and return false; otherwise return file:
    if not os.path.isfile(file_path):
        print("There is no file with data about students and professors")
        return False
    return file_path


#GENERAL ACTIONS:
def initialize_user(admin_id):
    """Initialices user. For admin, looks for 1234 password"""

    file = get_general_file()
    while True:
        try:
            user_id = int(input("Type your user ID\n"))
            if user_id == admin_id:
                return -1
            elif user_id in file["id_author"].values:
                index = file.index[file["id_author"] == user_id]
                return index
            else:
                return -2

        except ValueError:
            print("The user has to be a number")

def write_date(file, index, date, column):
    """Writes date in dataframe. Does not make any validation because it is used with select_date() function, wich makes the validation"""

    file[column][index] = date
    save_general_file(file)
    feedback_output(index)

def select_date():
    """Prompts the user for a date, and validates format. Returns a date in a correct format YYYY-mm-dd posterior to current time"""

    while True:
        date_str = input("Type a date in YYYY-MM-DD format:\n")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            if date < datetime.now():
                print("You should set a future date")
                continue
            return date
        except ValueError:
            print("The date is invalid, please use YYYY-MM-DD format")


def feedback_output(index, feedback="a", *columns):
    """Shows to the user a dataframe or a fragment. The part
    of dataframe is defined by *columns.
    It is possible to configure multiple feedback messages accompanied by the dataframe
    """

    file = get_general_file()
    if feedback == "a":
        print("Information has been added and file, updated:")
    elif feedback == "b":
        print("This is the information you are looking for:\n")

    if columns:
        print(file.iloc[index, list(columns)])
    else:
        print(file.iloc[index])
    input("\nPress enter key to continue\n")


def quit_program():
    """Quit the program"""

    sys.exit("You quit the program successfully")


def select_index():
    """Shows the user the dataframe and select an index to operate on a record."""

    file = get_general_file()
    # get the number of records:
    n_rows = file.shape[0]

    while True:
        try:
            print(file)
            index = int(
                input("Write the record number on which you want to operate.: ")
            )
            if index < n_rows and index >= 0:
                print("You have selected:\n____________")
                print(file.iloc[index])
            else:
                print(
                    "\n\n\nThere is not such record in database. Select a right record...\n\n\n"
                )
                continue

            confirmation = input("______________\n\nis it correct?\n").lower()
            if confirmation in list(["yes", "y"]):
                return index
            else:
                print("\nReturning to data base...\n______")
                continue

        except ValueError:
            print("You have to type a numer record")



#SECRETARY ACTIONS:

def admin_action():
    """Allows admin to chose an action"""

    while True:
        try:
            action = int(
                input(
                    "\n\nWhat do you wanna do?:\n1. Update core file.\n2. Set dates \n3. Assign directors \n4. Send message \n5. Quit\n"
                )
            )
            return action
        except ValueError:
            print("You must select an option")

def set_date():
    """Applies the write_date() function based on match cases to set dates for different types of events."""
    file = get_general_file()
    while True:
        try:
            kind_date = int(
                input(
                    "What is the event you want to set the date for?: \n1. Project submission\n2. Project correction submission\n3. Thesis submission\n4. Thesis correction submission\n5. Dissertation\n"
                )
            )
            break
        except ValueError:
            print("\nYou have to type a number\n")

    index = select_index()
    date = select_date()
    match kind_date:
        case 1:
            column = "project_date"
            write_date(file, index, date, column)
        case 2:
            column = "project_correction_date"
            write_date(file, index, date, column)
        case 3:
            column = "Thesis_date"
            write_date(file, index, date, column)
        case 4:
            column = "thesis_correction_date"
            write_date(file, index, date, column)
        case 5:
            column = "Dissertation_date"
            write_date(file, index, date, column)

def assign_director():
    """Prompts for a director's name, saves the changes and confirms the user"""

    file = get_general_file()
    index = select_index()

    while True:
        name = input("What is the director name?:\n")
        if re.match(r"^[a-zA-Z]+$", name):
            break
        else:
            print("You have to type a name")
            continue

    while True:
        mail = input("What is the director email address?:\n")
        if validate_email(mail):
            break
        else:
            print("You have to enter a valid email address")
            continue

    file["director"][index] = name
    file["director_mail"][index] = mail
    save_general_file(file)
    feedback_output(index)


def create_message():
    """Suggest messages to send to students and professors"""

    # CHECK IF THERE IS ENOUGH INFORMATION TO BE ABLE TO SEND EMAILS:
    file = get_general_file()
    index = select_index()
    record = file.loc[index, ["director", "director_mail"]]
    missing_info = record.isnull().any()

    if missing_info:
        print(
            """In order to be able generate message, the following information needs to be complete:\n- Director name.\n- Director mail address.\nReturning to main interfaz"""
        )
        return False

    # Messages to send:
    message_director_assignment = (
        f"Dear {file['author'][index]},\n"
        f"I am pleased to inform you that Professor {file['director'][index]} has been assigned as "
        f"your thesis supervisor. Professor {file['author'][index]} has extensive experience in your "
        f"field of study, and I am confident that he/she will provide you with effective guidance "
        f"throughout the development of your research.\n"
        f"I recommend that you contact Professor {file['author'][index]} as soon as possible "
        f"to discuss the details of your thesis project and establish a work plan. If you have "
        f"any questions or concerns, please do not hesitate to contact me.\n"
        f"I wish you an excellent experience working with Professor {file['author'][index]}. Good luck with your thesis project!\nSincerely,\n"
    )

    subject_director_assignment = "Assignment of Thesis Supervisor"

    message_student_assignment = (
        f"Dear Professor {file['director'][index]},\n"
        "I am pleased to inform you that student "
        f"{file['author'][index]} has been assigned to your thesis supervision. Student "
        f"{file['author'][index]} is a dedicated and enthusiastic student, and I am confident "
        "that he/she will work diligently on his/her thesis project.\n"
        "I would like to thank you for agreeing to be the thesis supervisor for student "
        f"{file['author'][index]}. Your expertise and knowledge will be of great help "
        "in guiding the student in his/her research.\n"
        f"If there is anything that student {file['author'][index]} "
        "can do to prepare for working with you, please let us know. "
        "I am sure he/she would be delighted to receive any guidance "
        "or suggestions you can provide.\n"
        "Thank you again for agreeing to be the thesis "
        f"supervisor for student {file['author'][index]}. "
        "We are looking forward to working together on this exciting project.\n"
        "Sincerely,\n"
    )

    subject_student_assignment = "Assignment of Student for Thesis Supervision"

    recipient_student = file["mail_author"][index]
    recipient_professor = file["director_mail"][index]

    # print suggested messages
    print(
        f"This is the mail message we suggest you for STUDENT:\n\n"
        f"Subject: {subject_director_assignment}\nRecipient: {recipient_student}\n"
        f"Message: {message_director_assignment}\n\n"
        f"This is the mail message we suggest you for PROFESSOR:\nSubject: "
        f"{subject_student_assignment}\n"
        f"Recipient: {recipient_professor}\n"
        f"Message: {message_student_assignment}\n\n"
    )

    input("We hope these messages are useful to you\nPress enter to continue\n")


#STUDENT ACTIONS:

def student_action():
    """Allows students to chose an action"""
    while True:
        try:
            action = int(
                input(
                    "\n\nWhat do you wanna do?:\n1. Register the title of your thesis\n2. View your thesis data\n3. View the dates related to your thesis\n4. Quit\n"
                )
            )
            return action
        except ValueError:
            print("You must select an option")


def register_title_thesis(index):
    """Adds the title of the student's thesis and returns feedback"""

    file = get_general_file()

    # add a simple verification for thesis title
    while True:
        title = input("Add the title of your thesis:\n")
        if len(title) < 10 or len(title.split()) < 3:
            print(
                "Title of your thesis has to have at least three words and ten letters"
            )
            continue
        break

    file["title"][index] = title
    save_general_file(file)
    feedback_output(index, "a", 0, 2, 1, 3)


def view_student_information(index):
    """Shows student general information"""

    feedback_output(index, "b", 2, 1, 0, 3, 4, 5)


def view_dates_thesis(index):
    """Show thesis dates information"""

    feedback_output(index, "b", 2, 1, 0, 6, 7, 8, 9, 10)






if __name__ == "__main__":
    main()
