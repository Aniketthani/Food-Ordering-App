from PIL import Image
from config import connect_to_database
from io import BytesIO
import os

#def CompressImage(file):
#    p=Image.open(file)
#    p.save("out"+file,optimized=True,quality=7)
cursor,mydb=connect_to_database()
#
sql="Select F_Id,Image from food_items"
cursor.execute(sql)
res=cursor.fetchall()

for i in res:
    with open(f"{i[0]}.jpg","wb") as f:
        f.write(i[1])
        f.close()

for i in res:
    Image.open(f"{i[0]}.jpg").convert("RGB").save(f"{i[0]}out.jpg",optimized=True,quality=7)
    sql=f"Update food_items set Image=%s Where F_Id='{i[0]}'"
    with open(f"{i[0]}out.jpg","rb") as f:
        bdata=f.read()
    cursor.execute(sql,(bdata,))
    mydb.commit()






