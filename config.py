from mysql.connector import connect

def connect_to_database():
    mydb=connect(
        host='192.168.1.8',user='admin',password='',database='food'

    )

    return mydb.cursor(),mydb
