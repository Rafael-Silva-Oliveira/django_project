print("Loading the script... Please wait")
from threading import local
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2 as pg
from tqdm import tqdm
import os
import csv
import random
import numpy as np
random.seed(42)
plt.interactive(False)
import seaborn as sns

#Set the config path file
os.chdir(r'..\interim')
import config


host = config.conn['host']
port = config.conn['port']
database = config.conn['database']
user = config.conn['user']
password = config.conn['password']

files_to_be_inserted_dir = config.files_to_be_inserted['dir']
concat_dinning_files_dir= config.concat_dinning_files['dir']
generate_random_student_data_dir= config.files_to_be_inserted['dir']


db_tables = []
available_ids = []

def pick_random(list):
    n = len(list)
    for i in random.sample(range(0,n),n):
        return(list[i])

def convert(list):
    return tuple(list)

def random_student_data():

    """
    This function will create a random set of attributes for each student given a list of values
    
    """
    id = ["u{:02d}".format(stud_id) for stud_id in range(0,60)]
    gender = ["male", "female"]
    age_group = ["between 18 and 20","between 21 and 23","between 24 and 26","27 and older"]
    year=[i for i in range(1,6)]
    area = ["social sciences","life sciences","engineering","mathematics"]
    lines = [['id','gender','age_group','random_year','random_area']]
    for student in id:
        random_gender = pick_random(gender)
        random_age_group = pick_random(age_group)
        random_year = pick_random(year)
        random_area = pick_random(area)
        lines.append([student,random_gender,random_age_group,random_year,random_area])

    # dir = input("Choose the directory to save the generated data for each student: ")
    # while not os.path.isdir(dir):
    #     print("Directory doesn't exist. Please try again")
    #     dir = input("Choose the directory to save the generated data for each student: ")
    if not os.path.exists('{}'.format(generate_random_student_data_dir)):
        os.makedirs('{}'.format(generate_random_student_data_dir))

    with open('{}\\crudapp_a_student.csv'.format(generate_random_student_data_dir), "w",newline='\n', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in lines:
            writer.writerow(line)
    print("Done!")

def concatenate_txt_to_csv():

    lines = [['timestamp','place','type','id']]
    for path, _, files in os.walk(concat_dinning_files_dir):
        for file in files:
            if file.endswith(".txt"):
                with open('{}\{}'.format(path,file)) as f:
                    for line in f:
                        line=line.rstrip()
                        line+=",{}".format(file[:3])
                        line_lst = line.split(",")
                        lines.append(line_lst)
   
    if not os.path.exists('{}'.format(generate_random_student_data_dir)): 
        os.makedirs('{}'.format(generate_random_student_data_dir))
        
    with open('{}\\crudapp_e_dinning.csv'.format(files_to_be_inserted_dir), "w",newline='\n', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in lines:
            writer.writerow(line)
    print("Done!")
def create_tables():
    """ create tables in the PostgreSQL database"""


    #print("Current connection parameters are: \n localhost: {} \n port: {}\n database: {}\n user: {}\n password: {}\n  ".format(host, port, database, user, password))

    keep_or_update_conn = input("Current connection parameters are: \n localhost: {} \n port: {}\n database: {}\n user: {}\n password: {}\n Do you want update the information? (y/n) ".format(host, port, database, user, password))
    
    if keep_or_update_conn.lower() == "y":

        globals()['host'] = input("Please choose a PostgreSQL host: ")
        host_correct = input("Are you sure the {} host name is correct? (y/n) ".format(globals()['host']))
        while True:
            if host_correct.lower() == "n":
                globals()['host'] = input("Please choose a PostgreSQL host: ")
                host_correct = input("Are you sure the {} host name is correct? (y/n) ".format(globals()['host']))
            else:
                break
        globals()['port'] = int(input("Please choose a PostgreSQL port: "))
        port_correct = input("Are you sure the {} port is correct? (y/n) ".format(globals()['port']))
        while True:
            if port_correct.lower() == "n":
                globals()['port'] = int(input("Please choose a PostgreSQL port: "))
                port_correct = input("Are you sure the {} port is correct? (y/n) ".format(globals()['port']))
            else:
                break
        globals()['database'] = input("Please choose a PostgreSQL database: ")
        database_correct = input("Are you sure the {} database is correct? (y/n) ".format(globals()['database']))
        while True:
            if database_correct.lower() == "n":
                globals()['database'] = input("Please choose a PostgreSQL database: ")
                database_correct = input("Are you sure the {} database is correct? (y/n) ".format(globals()['database']))
            else:
                break
        globals()['user'] = input("Please choose a PostgreSQL user: ")
        user_correct = input("Are you sure the {} user is correct? (y/n) ".format(globals()['user']))
        while True:
            if user_correct.lower() == "n":
                globals()['user'] = input("Please choose a PostgreSQL user: ")
                user_correct = input("Are you sure the {} user is correct? (y/n) ".format(globals()['user']))
            else:
                break
        globals()['password'] = input("Please choose a PostgreSQL password: ")
        password_correct = input("Are you sure the {} password is correct? (y/n) ".format(globals()['password']))
        while True:
            if password_correct.lower() == "n":
                globals()['password'] = input("Please choose a PostgreSQL password: ")
                password_correct = input("Are you sure the {} password is correct? (y/n) ".format(globals()['password']))
            else:
                break
    else:
        print("Information will be maintained as default.")
        

    commands = [
        """
        CREATE TABLE IF NOT EXISTS crudapp_a_student (
            student_id VARCHAR PRIMARY KEY,
            gender VARCHAR,
            age VARCHAR,
            year INT,
            area VARCHAR
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crudapp_b_grade (
            grade_student_id VARCHAR PRIMARY KEY,
            gpa_all FLOAT,
            gpa13s FLOAT,
            cs65 FLOAT,
            FOREIGN KEY(grade_student_id) REFERENCES crudapp_a_student (student_id) ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crudapp_c_lonely (
            lonely_student_id VARCHAR,
            type VARCHAR,
            tune_people_around VARCHAR,
            lack_companionship VARCHAR,
            nobody_to_turn_to VARCHAR,
            no_feeling_alone VARCHAR,
            feels_part_group_friends VARCHAR,
            lot_in_common VARCHAR,
            not_close_to_anyone VARCHAR,
            no_shared_interests VARCHAR,
            outgoing_person VARCHAR,
            people_feel_close_to VARCHAR,
            feels_left_out VARCHAR,
            social_relationship_superficial VARCHAR,
            not_known_well VARCHAR,
            feeling_isolated VARCHAR,
            can_find_companion_whenever VARCHAR,
            people_understand VARCHAR,
            unhappy_from_being_withdrawn VARCHAR,
            people_around_but_now_with_me VARCHAR,
            there_are_ppl_i_can_talk_to VARCHAR,
            there_are_ppl_i_can_turn_to VARCHAR,
            FOREIGN KEY(lonely_student_id) REFERENCES crudapp_a_student (student_id) ON UPDATE CASCADE ON DELETE CASCADE,
            PRIMARY KEY (lonely_student_id, type)

        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crudapp_d_stress (
            stress_student_id VARCHAR,
            type VARCHAR,
            how_often_feeling_upset_from_unexpected_things VARCHAR,
            having_control_over_important_things_in__your_life VARCHAR,
            how_often_felt_stress_nervous VARCHAR,
            how_often_felt_confident_to_handle_problems VARCHAR,
            how_often_felt_things_going_their_way VARCHAR,
            how_often_could_not_cope_with_all_the_things VARCHAR,
            how_often_been_able_to_control_irritations VARCHAR,
            how_often_felt_on_top_of_things VARCHAR,
            how_often_been_angered_on_things_outside_control VARCHAR,
            how_often_felt_difficulties_pilling_up_becoming_overwhelming VARCHAR,
            FOREIGN KEY(stress_student_id) REFERENCES crudapp_a_student (student_id) ON UPDATE CASCADE ON DELETE CASCADE,
            PRIMARY KEY (stress_student_id, type)

        )
        
        """,
        """
        CREATE TABLE IF NOT EXISTS crudapp_e_dinning (
            dinning_date TIMESTAMP,
            place VARCHAR,
            type VARCHAR,
            dinning_student_id VARCHAR,
            FOREIGN KEY(dinning_student_id) REFERENCES crudapp_a_student (student_id) ON UPDATE CASCADE ON DELETE CASCADE,
            PRIMARY KEY (dinning_student_id, dinning_date)
        )
        
        """
        ]
    conn = pg.connect(host=host,port = port, database=database,user=user,password=password)
    try:
        cur = conn.cursor()
        # create table one by one
        for command in tqdm(commands):
            cur.execute(command)
        temp_tables = []
        cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
        for table in cur.fetchall():
            temp_tables.append(table[0])
        print("Current tables in the database {} are: {}. ".format(database,','.join(map(str,temp_tables))))
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, pg.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_csv():
    """Function to insert the csv files from a given path in the database"""

    conn = pg.connect(host=host,port = port, database=database,user=user,password=password)
    try:
        cur = conn.cursor()
        # create table one by one

        cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
        for table in cur.fetchall():
            db_tables.append(table[0])
        print("Current tables in the database are: {}. Please make sure the name of the CSV files are the same as the names of the tables in the database.".format(','.join(map(str,db_tables))))
        for path, _, files in os.walk(files_to_be_inserted_dir):
            for file in tqdm(files):
                table_name_from_file = file.split(".")[0].lower()
                if table_name_from_file not in db_tables:
                    print(" Please, make sure the file has the same name as the tables in PostgreSQL! File name is {} and the current tables in the database are {}. Change the file name and try again.".format(table_name_from_file, db_tables))
                    break
                else:
                    with open(r'{}\{}'.format(path,file)) as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=",")
                        line_count=0
                        for row in csv_reader:
                            for index,element in enumerate(row): #converter os digitos que estao em string para floats
                                try:
                                    if isinstance(row[index],int):
                                        row[index] = int(element)
                                    elif isinstance(row[index],float):
                                        row[index] = float(element)
                                except:
                                    continue
                            if line_count == 0:
                                #print(row)
                                #print(f'Column names are {", ".join(row)}')
                                line_count += 1
                            else:
                                for element in row:
                                    #print(element)
                                    if table_name_from_file == "crudapp_a_student" and type(element) == str and element.startswith("u") :
                                        available_ids.append(element)
                                #print(tuple(row))
                                    if table_name_from_file in db_tables and element in available_ids:
                                        insert = "INSERT INTO " + "{}".format(table_name_from_file.lower()) + " VALUES {}".format(tuple(row))
                                        cur.execute(insert)
                                    else:
                                        continue
                                #Tambem bastava fazer apenas assim: (o for loop anterior serve apenas como percaução para garantir que nao há erros do tipo PK,FK)
                                # insert = "INSERT INTO " + table_name_from_file + " VALUES {}".format(tuple(row))
                                # cur.execute(insert)
                                line_count += 1

                        print(f'Processed {line_count} lines.')
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, pg.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def make_grade_distribution():

    conn = pg.connect(host=host,port = port, database=database,user=user,password=password)
    query = """SELECT grade_student_id,gpa_all, gender
                FROM crudapp_b_grade B
                    INNER JOIN crudapp_a_student A
                        ON grade_student_id = student_id;"""
    data = pd.read_sql(query, conn)
    sns.displot(data=data, x=data['gpa_all'], hue="gender",kind="kde", color = 'darkblue')
    plt.show(block=True)


def main():
	
    """
    Create a menu as following:
    1 - Transformar ficheiros .txt da pasta dinning para um unico ficheiro csv com nome e_dinning
    2 - Criar tabelas na base de dados (ver possibilidade de permitir usuario escrever host, pass, etc)
    3 - Opção para inserir os dados a partir de uma folder
    4 - Opção para visualizar grafico
    """
    option_dict = {1:'Transform .txt files from dinning data into a single .csv file (not required if you already have the crudapp_e_dinning.csv  file in the processed folder)', 2: 'Generate random data for the crudApp_a_student table. This will generate a csv file called crudapp_a_student.csv and saved in the processed folder.',3:'I just want the minimum user input possible! This option will 1) create tables, 2) add the csv files to the tables accordingly with the config path and 3) print the plot. No user input required.',4:'Exit'}
    print("############### \n ATTENTION: If you already have all the csv files in a single folder the only option you need is the 3rd option. If you want to try to concatenate the .txt files from the dinning folder into a single csv file, use option 1. If you want to generate new random data to populate the table called 'crudapp_a_table', press 2 \n ###############")
    print("Please, select one of the following options: ")
    for k,v in option_dict.items():
        print("{} - {}".format(k,v))
    picked_option = input("Choose one of the previous options: ")
    try:
        picked_option = int(picked_option)
    except:
        print("Option not available or incorret. Choose again.")
    while True:
        dict_values = [i for i in option_dict.keys()]
        try:
            picked_option = int(picked_option)
        except:
            print("Incorrect input. Choose again.")
        if picked_option not in dict_values:
            print("Option is not one of the ones available. Please try again.")
            picked_option = input("Choose one of the previous options: ")
        else:
            break
    if picked_option == 1:
        concatenate_txt_to_csv()
        main()
    elif picked_option == 2:
        random_student_data()
        main()
    elif picked_option == 3:
        create_tables()
        insert_csv()
        make_grade_distribution()
        main()
    elif picked_option == 4:
        return(print("Thank you for trying the script =) "))



main()