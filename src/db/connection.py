import mysql.connector
import pandas as pd

#Connection to the database
def connection(creds_path):
   """
   File must follow this structure:
   "username"
   "password"
   "host"
   "database"
   port
   """
   df = pd.read_csv(creds_path, sep=" ", header=None, names=["Value"])

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
   
   alertP1 = pd.read_sql("""SELECT * FROM consultaneurologia201216anon_true""",mydb)
   return(alertP1)

