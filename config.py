from mysql.connector import connect

def connect_to_database():
    mydb=connect(
        host='localhost',user='root',password='',database='food'

    )

    return mydb.cursor(),mydb
