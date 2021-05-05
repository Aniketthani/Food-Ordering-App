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


Builder.load_file('edit_food_item.kv')

class Content(BoxLayout):
    veg=True
    food_name=StringProperty()
    food_desc=StringProperty()
    food_price=StringProperty()
    food_veg=StringProperty()

    

    def __init__(self,food_name,food_desc,food_price,food_veg,**kwargs):
        super(Content,self).__init__(**kwargs)
       
        self.manager_open = False
        self.image_path=""
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )
        
        self.food_name=food_name
        self.food_desc=food_desc
        self.food_price=food_price
        self.food_veg=food_veg

    def update_data(self,food_name,food_desc,food_price,food_veg,*args):
        self.food_name=food_name
        self.food_desc=food_desc
        self.food_price=food_price
        self.food_veg=food_veg

        
    
    def file_manager_open(self):
        self.file_manager.show(primary_ext_storage)  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''
        try:
            extension=path.split(".")[1]
            if extension=="jpg" or extension=="png" or extension=="jpeg":
                self.image_path=path
                self.ids.choose_image_button.text=path.split(".")[0].split("/")[-1]+"."+extension
                self.exit_manager()
            else:
                toast("please select a valid image file")
        except:
            toast("please select a valid image file")
        
        

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def veg_radio_selection(self,is_veg,*args):
        
        if is_veg:
            if self.ids.veg.active:
                self.veg=True
                
            else:
                self.veg=None
                
        else:
            if self.ids.nonveg.active:
                self.veg=False
                
            else:
                self.veg=None

    

class Edit_Food_Item_Screen(Screen):
    restaurant_id=StringProperty()
    dialog=None
    f_id=""
    def __init__(self,**kwargs):
        super(Edit_Food_Item_Screen,self).__init__(**kwargs)

    def show_confirmation_dialog(self,food_name,food_desc,food_price,food_veg,f_id):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Edit Food Item",
                type="custom",
                content_cls=Content(food_name,food_desc,food_price,food_veg),
                buttons=[
                    MDRaisedButton(
                        text="CANCEL",on_release=lambda x:self.dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="SAVE",on_release=lambda x:self.save_changes()
                    ),
                ],
            )
            if food_veg=="1":
                self.dialog.content_cls.ids.veg.active=True
                self.dialog.content_cls.veg=True
            elif food_veg=="0":
                self.dialog.content_cls.ids.nonveg.active=True
                self.dialog.content_cls.veg=False
        else:
            self.dialog.content_cls.update_data(food_name,food_desc,food_price,food_veg)
            if food_veg=="1":
                self.dialog.content_cls.ids.veg.active=True
                self.dialog.content_cls.veg=True
            elif food_veg=="0":
                self.dialog.content_cls.ids.nonveg.active=True
                self.dialog.content_cls.veg=False
        self.dialog.content_cls.image_path=""
        self.dialog.content_cls.ids.choose_image_button.text="Choose Image"
        self.f_id=f_id
        self.dialog.open() 

    def save_changes(self,*args):
        if not self.dialog.content_cls.image_path:
            sql=f"update food_items set F_Name='{self.dialog.content_cls.ids.food.text}',Price='{self.dialog.content_cls.ids.price.text}',Description='{self.dialog.content_cls.ids.desc.text}',Veg='{int(self.dialog.content_cls.veg)}' Where F_Id='{self.f_id}'"   
            cursor.execute(sql)
            mydb.commit()
            self.dialog.dismiss()
            toast("Edited Successfully")
        
        else:
            sql="update food_items set F_Name=%s,Price=%s,Description=%s,Veg=%s,Image=%s Where F_Id=%s"

            with open(self.dialog.content_cls.image_path,"rb") as f:
                binarydata=f.read()
            cursor.execute(sql,(self.dialog.content_cls.ids.food.text,self.dialog.content_cls.ids.price.text,self.dialog.content_cls.ids.desc.text,int(self.dialog.content_cls.veg),binarydata,self.f_id))
            mydb.commit()
            self.dialog.dismiss()
            toast("Edited Successfully")
        self.display_food_items()
        self.ids.search_text.text=""

        self.dialog.content_cls.image_path=""
        self.dialog.content_cls.ids.choose_image_button.text="Choose Image"

    def display_food_items(self,*args):
        global food_items_list
        self.ids.food_list.clear_widgets()
        self.ids.search_text.text=""
        sql=f"Select * from food_items Where Restaurant_Id='{self.restaurant_id}'"
        cursor.execute(sql)
        res=cursor.fetchall()
        food_items_list=res[:]
        mydb.commit()
        
        
        for item in res:
            
            c=MDCard(orientation='horizontal',elevation=50,ripple_behavior=True,on_release=partial(self.edit_food,item[0]),size_hint=(1,None),height=self.parent.height/6)
            c.add_widget(Image(texture=CoreImage(BytesIO(item[5]),ext="jpg").texture,size_hint=(0.9,0.9 ),allow_stretch=True))
            c.add_widget(MDLabel(text=str(item[1]),halign="center"))
            if item[6]=="1":
                c.add_widget(Image(source='images/veg.png'))
            elif item[6]=="0":
                c.add_widget(Image(source='images/nonveg.png'))
            self.ids.food_list.add_widget(c)

    def edit_food(self,f_id,*args):
        sql=f"Select * from food_items Where F_Id='{f_id}'"
        cursor.execute(sql)
        res=cursor.fetchall()[0]
        mydb.commit()

        self.show_confirmation_dialog(food_name=str(res[1]),food_desc=str(res[4]),food_price=str(res[3]),food_veg=str(res[6]),f_id=str(res[0]))
    def search_food(self,text,*args):
        global food_items_list
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
            c=MDCard(orientation='horizontal',elevation=30,ripple_behavior=True,on_release=partial(self.edit_food,item[0]),size_hint=(1,None),height=self.parent.height/6)
            c.add_widget(Image(texture=CoreImage(BytesIO(item[5]),ext="jpg").texture,size_hint=(0.9,0.9 ),allow_stretch=True))
            c.add_widget(MDLabel(text=str(item[1]),halign="center"))
            if item[6]=="1":
                c.add_widget(Image(source='images/veg.png'))
            elif item[6]=="0":
                c.add_widget(Image(source='images/nonveg.png'))
            self.ids.food_list.add_widget(c)


class MainApp(MDApp):
    def build(self):
        return Edit_Food_Item_Screen()

#MainApp().run()