from sqlite3 import connect
import mysql.connector
from utils.status import status
import os
from dotenv import load_dotenv


# Function to connect to the MariaDB database
def connect_to_database():
    load_dotenv()
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_DATABASE")
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
# Function to retrieve and display data from all tables in the database
alldat = {}
tablenames = {}
classes = {}



def main():
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        #grab all table names
        cursor.execute('SHOW TABLES')
        tables = [table[0] for table in cursor.fetchall()]
        for table in tables:
            cursor.execute(f"SELECT * FROM {table} WHERE id != ''")
            data = cursor.fetchall()
            cursor.execute(f"DESCRIBE {table}")
            columns = [column[0] for column in cursor.fetchall()]
            if data:
                #alldat[table]={"items":columns,'data':list(data[0])}
                names = columns
                data = list(data[0])
                tmpdict = {}
                for x in range(0,len(names)):
                    tmpdict[names[x]]=data[x]
                classes[table]=type(table,(object,),tmpdict)

        
        #compitems = alldat['computers']['items']
        #dataitems = alldat['computers']['data']
        #print(compitems,dataitems)
        #print(type(dataitems[0]))
        #searchitem = compitems.index('cpu')
        #print(searchitem)
        #output = dataitems[searchitem]
        #print(output)
        #print(alldat)
        #computers = alldat['computers']
        ##create the dynamic classes
        #cdict = {}
        #for x in range(0,len(compitems)):
        #    cdict[compitems[x]]=dataitems[x]
        
            
        #ComputerClass = type('ComputerClass', (object,), cdict)

        BigClass = type('BigClass',(object,),classes)
        print(vars(BigClass.computers))
        
        
        print(BigClass.keyboards.id)


        #print(ComputerClass.name)


    except mysql.connector.Error as e:
        print(status.ERROR, e)
    finally:
        connection.close()

if __name__ == "__main__":
    main()
    #try:
        #main()
    #except Exception as e:
        #print(status.ERROR,e)
