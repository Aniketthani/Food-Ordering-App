from mysql.connector import connect

def connect_to_database():
    mydb=connect(
        host='sql6.freemysqlhosting.net',user='sql6406384',password='9gPfJMtqiW',database='sql6406384'

    )

    return mydb.cursor(),mydb
