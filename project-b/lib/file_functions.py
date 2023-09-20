from lib.user_actions_functions import *


import sys
import os
import shutil
import csv
import pandas as pd

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


