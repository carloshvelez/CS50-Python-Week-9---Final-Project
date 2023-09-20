import lib.file_functions as ff


import sys
from validate_email import validate_email
import pandas as pd
import re
from datetime import datetime

#GENERAL ACTIONS:
def initialize_user(admin_id):
    """Initialices user. For admin, looks for 1234 password"""

    file = ff.get_general_file()
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
    ff.save_general_file(file)
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

    file = ff.get_general_file()
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

    file = ff.get_general_file()
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
    file = ff.get_general_file()
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

    file = ff.get_general_file()
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
    ff.save_general_file(file)
    feedback_output(index)


def create_message():
    """Suggest messages to send to students and professors"""

    # CHECK IF THERE IS ENOUGH INFORMATION TO BE ABLE TO SEND EMAILS:
    file = ff.get_general_file()
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

    file = ff.get_general_file()

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
    ff.save_general_file(file)
    feedback_output(index, "a", 0, 2, 1, 3)


def view_student_information(index):
    """Shows student general information"""

    feedback_output(index, "b", 2, 1, 0, 3, 4, 5)


def view_dates_thesis(index):
    """Show thesis dates information"""

    feedback_output(index, "b", 2, 1, 0, 6, 7, 8, 9, 10)