# Importar librerías necesarias.
#Probablemente sys (para salidas y prompts en líneas de comandos), os (para archivos), shutil (para copiar archivos).
import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from validate_email import validate_email
import shutil
import csv
import pandas as pd
import re
from datetime import datetime

admin_id = 1234
header_general = 0
class Tesis:
    def __init__(self, id_author):
        self.title = ""
        self.abstract = ""
        self.author = ""
        self.id_author = id_author
        self.director = ""
        self.jurado1 = ""
        self.jurado2 = ""
        self.path = ""
        self.file_name = ""


def main():

    #Verificar si hay archivo principal, si no, salir con un mensaje de error
    if initialize_user() == "admin":
        print("Welcome, system administrator")
        file = verify_core_file()
        if file is False:
            file = add_core_file()

        while True:
            match admin_action():
                case 1:
                    update_core_file()
                case 2:
                    set_date()
                case 3:
                    assign_director()
                case 4:
                    send_mail()
                case 5:
                    quit_program()
                case _:
                    print("\nYou need to select an available option\n")

            #else:
             #   print("\nYou need to select an available option\n")







def update_core_file():
    file = get_file()
    core_file_name = "./csv_files/core_csv_file/core.csv"
    shutil.copy(file, core_file_name)
    print("Core file updated")


def set_limit_date():
    path = "./csv_files/general_file"
    if len(os.listdir(path)) == 0:
        print("In order to set limit date, you need to assign directors")


def set_general_file():
    path_general = "./csv_files/general_file/general.csv"
    file = pd.read_csv(path_general)
    pd.options.mode.chained_assignment = None
    return file

def select_index():
    file = set_general_file()
    n_rows = file.shape[0]

    while True:
        try:
            print(file)
            index = int(input("Write the record number on which you want to operate.: "))
            if index < n_rows and index >= 0:
                print("You have selected:\n____________")
                print(file.iloc[index])
            else:
                print("\n\n\nThere is not such record in database. Select a right record...\n\n\n")
                continue

            confirmation = input("______________\n\nis it correct?").lower()
            if confirmation in list(["yes", "y"]):
                return index
            else:
                print("\nReturning to data base...\n______")
                continue

        except ValueError:
            print("You have to type a numer record")





def assign_director():
    file = set_general_file()
    index = select_index()

    while True:
        try:
            name = input("What is the director name?: ")
            break
        except ValueError:
            print("You have to type a name")

    while True:
        mail = input("What is the director mail?: ")
        if validate_email(mail):
            break
        else:
            print("You have to type a valid mail")
            continue

    file["director"][index] = name
    file["director_mail"][index] = mail
    save_general_file(file)

    confirmation_output(index)




def confirmation_output(index):
    file = set_general_file()
    print("Informations has been added and file, updated:")
    print(file.iloc[index])


def select_date():
    while True:
        date_str = input("Type a date in YYYY-MM-DD format: ")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            if date < datetime.now():
                print("You should set a future date")
                continue
            return date
        except ValueError:
            print("The date is invalid, please use YYYY-MM-DD format")


def save_general_file(file):
    file.to_csv("./csv_files/general_file/general.csv", index = False)



def write_date(file, index, date, column):

    file[column][index] = date
    save_general_file(file)
    confirmation_output(index)





def set_date():
    file = set_general_file()
    while True:
        try:
            kind_date = int(input("What is the event you want to set the date for?: \n1. Project submission\n2. Project correction submission\n3. Thesis submission\n4. Thesis correction submission\n5. Dissertation\n "))
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





def create_general_file():
    """Create a general file (file with thesis information), from core file"""
    path_general = "./csv_files/general_file/general.csv"
    path_core = "./csv_files/core_csv_file/core.csv"
    csv_row_titles = ["title", "id_author", "author", "mail_author", "director", "director_mail", "jury1",
                      "jury1_mail", "jury2", "jury2_mail", "semester", "status", "project_date", "project_correction_date",
                      "Thesis_date", "thesis_correction_date", "Dissertation_date"]

    with open(path_core, "r") as core_file:
        with open(path_general, "w") as general_file:
            writer_general = csv.DictWriter(general_file, fieldnames = csv_row_titles)
            writer_general.writeheader()
            reader_core = csv.DictReader(core_file)
            for i in reader_core:
                writer_general.writerow({"id_author": i["id"], "author": i["name"], "mail_author":i["mail"]})









def send_mail():

     #CHECK IF THERE IS ENOUGH INFORMATION TO BE ABLE TO SEND EMAILS:
    file = set_general_file()
    index = select_index()
    record = file.loc[index, ["director", "director_mail"]]
    missing_info = record.isnull().any()

    if missing_info:
        print('''In order to be able to send any email, the following information needs to be complete:\n- Director name.\n- Director mail address.\nReturning to main interfaz''')
        return False



    #Messages to send:
    message_director_assignment = f'''Dear {file["author"][index]},\n
I am pleased to inform you that Professor {file["director"][index]} has been assigned as your thesis supervisor. Professor {file["author"][index]} has extensive experience in your field of study, and I am confident that he/she will provide you with effective guidance throughout the development of your research.\n
I recommend that you contact Professor {file["author"][index]} as soon as possible to discuss the details of your thesis project and establish a work plan. If you have any questions or concerns, please do not hesitate to contact me.\n
I wish you an excellent experience working with Professor {file["author"][index]}. Good luck with your thesis project!\n
Sincerely,\n'''

    subject_director_assigment = "Assignment of Thesis Supervisor"

    message_student_assignment = f'''Dear Professor {file["author"][index]},\n
I am pleased to inform you that student {file["author"][index]} has been assigned to your thesis supervision. Student {file["author"][index]} is a dedicated and enthusiastic student, and I am confident that he/she will work diligently on his/her thesis project.\n
I would like to thank you for agreeing to be the thesis supervisor for student {file["author"][index]}. Your expertise and knowledge will be of great help in guiding the student in his/her research.\n
If there is anything that student {file["author"][index]} can do to prepare for working with you, please let us know. I am sure he/she would be delighted to receive any guidance or suggestions you can provide.\n
Thank you again for agreeing to be the thesis supervisor for student {file["author"][index]}. We are looking forward to working together on this exciting project.\n
Sincerely,\n'''

    subject_student_assignment = "Assignment of Student for Thesis Supervision"







    """Sends e-mail messages to professors and students"""
    #Details SMTP GMAIL
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    smtp_username = "psicopatologiainfantilus2018@gmail.com"
    smtp_password = "estudiantes2018"

    #Message for student details:
    sender = "psicopatologiainfantilus2018@gmail.com"
    recipient_student = file["mail_author"][index]
    subject_student = subject_director_assigment
    body_student = message_director_assignment


    # Mesagge for student creation
    message_student = MIMEMultipart()
    message_student["From"] = sender
    message_student["To"] = recipient_student
    message_student["Subject"] = subject_student
    message_student.attach(MIMEText(body_student, "plain"))

    #Message for professor details:
    sender = "psicopatologiainfantilus2018@gmail.com"
    recipient_professor = file["director_mail"][index]
    subject_professor = subject_student_assignment
    body_professor = message_student_assignment


    # Mesagge for student creation
    message_student = MIMEMultipart()
    message_student["From"] = sender
    message_student["To"] = recipient_professor
    message_student["Subject"] = subject_professor
    message_student.attach(MIMEText(body_professor, "plain"))

    # Mesagge for professor creation
    message_student = MIMEMultipart()
    message_student["From"] = sender
    message_student["To"] = recipient_student
    message_student["Subject"] = subject_student
    message_student.attach(MIMEText(body_student, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender, recipient_student, message_student.as_string())

    except smtplib.SMTPAuthenticationError:
        print("No se pudo atenticar en el servidor")
        input("Press enter key to continue")
        return False



def quit_program():
    """Quit the program"""
    sys.exit("You quited successfully")


def verify_core_file():
    """Verifiye if there is core.csv file in ./csv_files/core_csv_file path"""

    folder_path = "./csv_files/core_csv_file"
    file_name = "core.csv"
    file_path = os.path.join(folder_path, file_name)
    if not os.path.isfile(file_path):
         print("There is no file with data about students and professors")
         return False
    return file_path

def get_file():
    """Prompts the user for a file path and returns that path if there is file, otherwise loops"""
    while True:
        file_path = input("Write file path: ")
        if os.path.isfile(file_path):
            return file_path
        print("Not such file or directory")


def add_core_file():
    """Asks if admin wants to add a core file to the ./csv_files/core_csv_file path"""
    have_file = input("Do you want to add a file with students and professors data? ").lower()
    if have_file in ["yes", "y"]:
        file = get_file()
        core_file_name = "./csv_files/core_csv_file/core.csv"
        shutil.copy(file, core_file_name)
        create_general_file()
        print("Core file added and general file created")
        return core_file_name
    else:
        sys.exit("No data\ninterrupting program\n...\n...\n...")

def initialize_user():
    """Initialices user. For admin, looks for """
    while True:
        try:
            user_id = int(input("Type your user ID "))
            if user_id == admin_id:
                return "admin"
            #if user_id in #archivo:
             #   return "tipo de usuario"
            else:
                print("User id is not in database")



        except ValueError:
            print("The user has to be a number")

def admin_action():
    """Allow admin to chose an action"""
    while True:
        try:
            action = int(input("\n\nWhat do you wanna do?:\n1. Update core file.\n2. Set dates \n3. Assign directors \n4. Send message \n5. Quit\n"))
            return action
        except ValueError:
            print("You must select an option")

















if __name__ == "__main__":
    main()




# Decidir si trabajaré con clases, por ejemplo, una clase para una tesis. En ese entendido, tendré que crearla.


# Diseñar la funcionalidad para el administrador:
    #Agregar un archivo con datos de estudiantes.
    #Agregar fechas límite.
    #Asignar directores.
    #Enviar mensajes (smtplib permite hacer esto (chatgpt)).
    #Programar tesis.

# Diseñar la funcionalidad para el estudiante:
    #registrarse.
    #registrar título de su proyecto
    #Registrar el resumen de su proyecto
    #Subir un archivo

    #Descargar anteproyecto evaluado.
    #registrar correcciones
    #Subir archivo con correcciones.
    #consultar estado de anteproyecto.

    #registrar el título de la tesis.
    #registrar el resumen de la tesis.
    #subir archivo de tesis.
    #consultar estado de tesis.
    #subir archivo de tesis con correcciones.

#Diseñar funcionalidad para el director:
    #Revisar estado de estudiante.
    #Aprobar documento.

#Diseñar funcionalidad para el jurado:
    #Descargar archivo de tesis.
    #Seleccionar estudiante.
    #Subir archivo con sugerencias.
    #Escribir concepto.

