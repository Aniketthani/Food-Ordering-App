from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from config import pass_cursor
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from io import BytesIO
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivymd.uix.label import MDLabel
from functools import partial
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
#from loginscreen import pass_cursor
try:
    from android.storage import primary_external_storage_path
    primary_ext_storage = primary_external_storage_path()
except:
    primary_ext_storage="/"


cursor,mydb=pass_cursor()

Builder.load_file('delete_food_item.kv')

class Content(BoxLayout):
    pass

    

class Delete_Food_Item_Screen(Screen):
    restaurant_id=StringProperty()
    dialog=None
    f_id=""
    def __init__(self,**kwargs):
        super(Delete_Food_Item_Screen,self).__init__(**kwargs)

    def show_confirmation_dialog(self,f_id):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Delete Food Item",
                type="custom",
                
                buttons=[
                    MDRaisedButton(
                        text="CANCEL",on_release=lambda x:self.dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="Delete",on_release=lambda x:self.save_changes()
                    ),
                ],
            )
            
        self.f_id=f_id
        self.dialog.open()
        
         

    def save_changes(self,*args):
        sql=f"Delete from food_items Where F_Id='{self.f_id}'"
        cursor.execute(sql)
        mydb.commit()
        self.display_food_items()
        self.ids.search_text.text=""

        self.dialog.dismiss()
        toast("Deleted Successfully")

        

    def display_food_items(self,*args):
        global food_items_list
        self.ids.food_list.clear_widgets()
        self.ids.search_text.text=""
        sql=f"Select * from food_items Where Restaurant_Id='{self.restaurant_id}'"
        cursor.execute(sql)
        res=cursor.fetchall()
        mydb.commit()
        food_items_list=res[:]
        
        
        for item in res:
            
            c=MDCard(orientation='horizontal',elevation=50,ripple_behavior=True,on_release=partial(self.delete_food,item[0]),size_hint=(1,None),height=self.parent.height/6)
            c.add_widget(Image(texture=CoreImage(BytesIO(item[5]),ext="jpg").texture,size_hint=(0.9,0.9 ),allow_stretch=True))
            c.add_widget(MDLabel(text=str(item[1]),halign="center"))
            if item[6]=="1":
                c.add_widget(Image(source='images/veg.png'))
            elif item[6]=="0":
                c.add_widget(Image(source='images/nonveg.png'))
            self.ids.food_list.add_widget(c)

    def delete_food(self,f_id,*args):
        sql=f"Select F_Id from food_items Where F_Id='{f_id}'"
        cursor.execute(sql)
        res=cursor.fetchall()[0][0]
        mydb.commit()

        self.show_confirmation_dialog(f_id=str(res))
    def search_food(self,text,*args):
        self.ids.food_list.clear_widgets()
        
        #sql=f"Select * from food_items Where F_Name Like '%{text}%'"
        #cursor.execute(sql)
        #res=cursor.fetchall()
        #mydb.commit()

        res=[]
        for i in food_items_list:
            if text.lower() in i[1].lower():
                res.append(i)

        for item in res:
            c=MDCard(orientation='horizontal',elevation=30,ripple_behavior=True,on_release=partial(self.delete_food,item[0]),size_hint=(1,None),height=self.parent.height/6)
            c.add_widget(Image(texture=CoreImage(BytesIO(item[5]),ext="jpg").texture,size_hint=(0.9,0.9 ),allow_stretch=True))
            c.add_widget(MDLabel(text=str(item[1]),halign="center"))
            if item[6]=="1":
                c.add_widget(Image(source='images/veg.png'))
            elif item[6]=="0":
                c.add_widget(Image(source='images/nonveg.png'))
            self.ids.food_list.add_widget(c)


