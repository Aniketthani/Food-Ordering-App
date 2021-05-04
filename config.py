from mysql.connector import connect


def connect_to_database():
    try:
        mydb=connect(
            host='192.168.1.6',user='root',password='aniket',database='food'

        )

        return mydb.cursor(),mydb
    except:
        return 0,0
