from mysql.connector import connect
import concurrent.futures

cursor=0
mydb=0
def connect_to_database():
    
    conn=connect(
        #host='192.168.1.6',user='admin',password='',database='food'
        host='bzy54iwxivv9shzsm3oi-mysql.services.clever-cloud.com',user='ucx5vafmemhnaxsx',password='MPgGTDFmMfQPlMVjMdJv',database='bzy54iwxivv9shzsm3oi'
    )

    return conn.cursor(),conn

def pass_cursor():
    global cursor,mydb
    if not  cursor or not mydb:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(connect_to_database)
            cursor,mydb = future.result()
    

        
        return cursor,mydb
    else:
        return cursor,mydb

    