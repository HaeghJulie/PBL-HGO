import mysql.connector
import pandas as pd
from Functions.AlertP1.data_cleaning import *
from Functions.NLP.alertp1_nlp import *

    #Login Credentials
"""
File must follow this structure:
"username"
"password"
"host"
"database"
port
"""

df = pd.read_csv("credentials.txt", sep=" ", header=None, names=["Value"])

#Connection to the database
host = df["Value"][2]
user = df["Value"][0]
password = df["Value"][1]
database = df["Value"][3]
port = df["Value"][4]
mydb = mysql.connector.connect(host=host, user=user, database=database, port=port, password=password, auth_plugin='mysql_native_password')
mycursor = mydb.cursor()

#Safecheck to guarantee that the connection worked
mycursor.execute('SHOW TABLES;')
print(f"Tables: {mycursor.fetchall()}")
print(mydb.connection_id) #it'll give connection_id,if got connected

#Create a DataFrame
alertP1 = pd.read_sql("""SELECT * FROM consultaneurologia201216anon_true""",mydb)

print("Data Created")

#Data Cleaning
lower_text(alertP1,"Texto","clean_text")
date_format_alertP1(alertP1)
replace_blank(alertP1)

print("Data Cleaned")

### NLP ###

#Medications
categorize_medication(alertP1,"clean_text", "Data/drugs_data_big.xlsx", 75)
add_textcount_columns(alertP1,"clean_text","medication_level_1")
add_textcount_columns(alertP1,"clean_text","medication_level_2")
add_textcount_columns(alertP1,"clean_text","medication_level_3")

print("Medications done")
###

remove_stop_words(alertP1, "clean_text", "clean_text")
spacy_lemmatizer(alertP1, "clean_text", "clean_text")

print(alertP1.head())

#Save the new, clean and ready to slay CSV
load_data("data_with_meds.csv",alertP1)

print("Data Saved")
