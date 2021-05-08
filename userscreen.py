from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from config import pass_cursor
from kivymd.uix.card import MDCard
from kivy.graphics import Color,RoundedRectangle
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivymd.uix.label import MDLabel
from io import BytesIO
from functools import partial
from kivymd.uix.list import OneLineAvatarIconListItem,IconRightWidget,IconLeftWidget
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from datetime import datetime,timedelta
from datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
#from loginscreen import pass_cursor




cursor,mydb=pass_cursor()
rest_list=[]
Builder.load_file('userscreen.kv')

class MyCard(MDCard):
    def __init__(self,**kwargs):
        super(MyCard,self).__init__(**kwargs)

class FoodCard(MDCard):
    def __init__(self,**kwargs):
        super(FoodCard,self).__init__(**kwargs)

class CartCard(MDCard):
    def __init__(self,**kwargs):
        super(CartCard,self).__init__(**kwargs)


class Quantity_Input(BoxLayout):
    pass

class Dialog_Content(BoxLayout):
    pass

class User_Screen(Screen):
    userid=StringProperty()
    username=StringProperty()
    dialog = None
    cart={}
    edit_cart_item_dialog=None
    place_order_confirm_dialog=None
    city=StringProperty()
    state=StringProperty()
    def __init__(self,**kwargs):
        super(User_Screen,self).__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        
        mydb.commit()
        sql="Select Distinct city_state from cities"
        cursor.execute(sql)
        res=cursor.fetchall()
        self.city_menu = MDDropdownMenu(
            caller=self.ids.city,
            items=[],
            position="center",
            width_mult=8,
        )
        self.state_menu_items=[
            {
                "viewclass": "OneLineListItem",
                
                "text": f"{i[0]}",
                "height": dp(56),
                "on_release": lambda x=f"{i[0]}": self.set_state_item(x),
            } for i in res
        ]
        self.state_menu = MDDropdownMenu(
            caller=self.ids.state,
            items=self.state_menu_items,
            position="center",
            width_mult=8,
        )

        self.state_menu.bind()
        

        
        self.place_order_confirm_dialog=MDDialog(
            title="Confirm Place Order",
                buttons=[
                    MDRaisedButton(
                        text="NO", on_release=lambda x:self.place_order_confirm_dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="YES",on_release=lambda x:self.place_order()
                    ),
                ],
        )

    def set_state_item(self, text_item):
        self.ids.state.set_item(text_item)
        self.ids.state.text=text_item
        self.state_menu.dismiss()

        self.ids.city.text="City"
        

        sql=f"Select Distinct city_name from cities Where city_state='{text_item}' "
        cursor.execute(sql)
        cities=cursor.fetchall()

        self.city_menu_items=[
            {
                "viewclass": "OneLineListItem",
                
                "text": f"{i[0]}",
                "height": dp(56),
                "on_release": lambda x=f"{i[0]}": self.set_city_item(x),
            } for i in cities
        ]
        self.city_menu = MDDropdownMenu(
            caller=self.ids.city,
            items=self.city_menu_items,
            position="center",
            width_mult=8,
        )

        self.city_menu.bind()

    def set_city_item(self, text_item):
        self.ids.city.set_item(text_item)
        self.ids.city.text=text_item
        self.city_menu.dismiss()

    def logout(self,*args):
        self.parent.current="login"
        self.ids.orders_sm.current="restaurant"
        self.ids.account_manager.current="account_screen"
        self.ids.bottom_nav.switch_tab("order")
        with open("session.txt","w") as f:
            f.write("")
            f.close()

    def show_account_screen(self,*args):
        mydb.commit()
        sql=f"Select Mobile from users Where Id='{self.userid}'"
        cursor.execute(sql)
        mobile=cursor.fetchall()[0][0]
        self.ids.account_name.text=f""" [b][size=70]{self.username}[/size]
        
    [color=#1700c7]Mobile : {mobile}[/color][/b]"""



    def show_previous_orders(self,*args):
        
        mydb.commit()
        tdate=datetime.now()
        fdate=timedelta(days=10)
        fdate=tdate-fdate
        fdate=fdate.strftime("%Y-%m-%d")
        tdate=tdate.strftime("%Y-%m-%d")
        
        sql=f"Select * from orders Where Cust_Id='{self.userid}' and Date Between'{fdate}' and '{tdate}'  Order By ONO DESC"
       
        cursor.execute(sql)
        res=cursor.fetchall()
        
        self.ids.previous_order_list.clear_widgets()
        for order in res:
            item=OneLineAvatarIconListItem(text=f"Order No : {order[0]}",on_release=partial(self.show_particular_order_details,order))
            item.add_widget(IconLeftWidget(icon="receipt"))
            self.ids.previous_order_list.add_widget(item)
    
    def show_particular_order_details(self,order,*args):
        self.ids.history_manager.current="particular_order_screen"
        sql=f"Select * from users where Id='{order[8]}'"
        cursor.execute(sql)
        res=cursor.fetchall()[0]

        self.ids.order_header_details.text=f"""ONO : {order[0]}  Customer : {res[3]} \n Mobile : {res[4]}  Address : {res[6]}\n
City : {res[7]}  State : {res[8]} \n Pincode : {res[9]}"""

        self.ids.total_bill.text=f"Total : Rs {order[7]}"
        
        f_items=tuple(order[5].split("-"))
        f_quantity=order[6].split("-")

        if len(f_items)==1:
            sql=f"Select F_Name,Price from food_items Where F_Id='{f_items[0]}' "
        else:
            sql=f"Select F_Name,Price from food_items Where F_Id In {f_items}"
        cursor.execute(sql)
        res=cursor.fetchall()

        rows=[]
        
        for i in range(len(f_items)):
            t=(res[i][0],res[i][1],f_quantity[i],int(res[i][1])*int(f_quantity[i]))
            rows.append(t)
        rows.append(("","","",""))






        try:
            self.ids.particular_order_screen.remove_widget(self.ordertable)
        except:
            pass
        self.ordertable=MDDataTable(size_hint=(0.9,0.5),column_data=[
                ("Food", dp(20)),
                ("Price", dp(15)),
                
                ("Quantity", dp(15)),
                ("Total", dp(15)),
                
            ],
            pos_hint={'top':0.5,'center_x':0.5},row_data=rows
            )
        self.ids.particular_order_screen.add_widget(self.ordertable)

        if order[9]==1:
            self.ids.dispatched_order_label.text="[b]Order Dispatched From Restaurant[/b]"
        elif order[9]==0:
            self.ids.dispatched_order_label.text="[b]Order in process[/b]"
    

    def place_order(self,*args):
        sql="Insert Into orders (Date,Time,Restaurant_Id,Restaurant_Name,Food_Items,Quantity,Bill,Cust_Id,Dispatched) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        date=datetime.now().strftime("%Y-%m-%d")
        time=str(datetime.now().strftime("%I:%M:%S%p")).lower()

        res_list=[]
        for i in self.cart.keys():
            if self.cart[i][1] not in res_list:
                res_list.append(self.cart[i][1])

        for o in res_list:
            food_items=""
            food_quantity=""
            bill=0
            for i in self.cart.keys():
                if self.cart[i][1]==o:
                    food_items+=str(i)+"-"
                    food_quantity+=str(self.cart[i][3])+"-"
                    bill=bill+int(self.cart[i][2])*int(self.cart[i][3])
            food_items=food_items[:-1]
            food_quantity=food_quantity[:-1]

            sql_res_name=f"Select Name from restaurants Where Restaurant_Id='{o}'"
            cursor.execute(sql_res_name)
            res_name=cursor.fetchall()[0][0]
            dispatched=0
            cursor.execute(sql,(date,time,o,res_name,food_items,food_quantity,bill,self.userid,dispatched))
            mydb.commit()
        

        self.cart=[]
        self.ids.cart_items.clear_widgets()
        self.place_order_confirm_dialog.dismiss()
        toast("Order Placed Successfully")
        self.total=0
        self.ids.place_order_btn.disabled=True
        self.ids.cart_total.text="Total : Rs 0"
        self.ids.orders_sm.current="restaurant"
        self.ids.search_food_res.text=""

    def change_quantity(self,change,quantity_widget,*args):
        

        if not quantity_widget.ids.quantity.text:
            quantity_widget.ids.quantity.text="0"
         
        quantity_widget.ids.quantity.text=str(int(quantity_widget.ids.quantity.text)+int(change))
        if int(quantity_widget.ids.quantity.text)<0:
            quantity_widget.ids.quantity.text="0"

    def navigate_back(self,cur_screen,*args):
        if cur_screen=="food_menu":
            self.ids.orders_sm.current="restaurant"
        elif cur_screen=="submenu":
            self.ids.orders_sm.current="food_menu"
        elif cur_screen=="cart":
            self.ids.orders_sm.current="restaurant"
    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.ids.orders_sm.current=="submenu":

                self.ids.orders_sm.current="food_menu"
            elif self.ids.orders_sm.current=="food_menu":
                self.ids.orders_sm.current="restaurant"
            elif self.ids.orders_sm.current=="cart":
                self.ids.orders_sm.current="restaurant"
        return True
    def display_food_menu(self,res_id,*args):
        self.ids.food_menu.clear_widgets()
        self.ids.orders_sm.current="food_menu"

        sql=f"Select Distinct Category from food_items Where Restaurant_Id='{res_id}'"
        cursor.execute(sql)
        res=cursor.fetchall()

        for c in res:
            item=OneLineAvatarIconListItem(text=c[0],font_style="Button",on_release=partial(self.display_submenu,c[0],res_id))
            item.add_widget(IconRightWidget(icon="plus"))

            self.ids.food_menu.add_widget(item)

    def display_submenu(self,category,res_id,*args):
        
        self.ids.submenu.clear_widgets()
        sql=f"Select * from food_items Where Restaurant_Id='{res_id}' and Category='{category}'"
        cursor.execute(sql)
        res=cursor.fetchall()

        for item in res:
            
            c=FoodCard(orientation='horizontal',elevation=40,ripple_behavior=True,size_hint=(1,None),height="100dp",on_release=partial(self.select_quantity,item[0],item[1],item[2],item[3],item[4],item[5]))
            
            
            c.add_widget(Image(texture=CoreImage(BytesIO(item[5]),ext="jpg").texture,size_hint=(0.9,0.9 ),allow_stretch=True))
            c.add_widget(MDLabel(text="[b]"+str(item[1])+"[/b]",halign="center",theme_text_color="Custom",text_color=(1,1,1,1),markup=True))

            if item[6]=="1":
                c.add_widget(Image(source="images/veg.png"))
            elif item[6]=="0":
                c.add_widget(Image(source="images/nonveg.png"))
            self.ids.submenu.add_widget(c)
        self.ids.orders_sm.current="submenu"
    
    def select_quantity(self,f_id,f_name,res_id,price,desc,image,*args):

        
        self.dialog = MDDialog(
            title="Order Box",
            type="custom",
            content_cls=Dialog_Content(),
            buttons=[
                MDRaisedButton(
                    text="CANCEL",on_release=lambda x:self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="ADD TO CART",on_release=lambda x:self.add_to_cart(f_id,f_name,res_id,price,image)
                ),
            ],
        )
        
        self.dialog.content_cls.ids.fo_name.text=f"[b]{f_name}[/b]\n\n {desc}"
        self.dialog.content_cls.ids.fo_price.text=f"[b]Rs {price}[/b]"
        self.dialog.content_cls.ids.quantity_input.ids.quantity.text=""
        try:
            if self.cart[f_id][3]:
                self.dialog.content_cls.ids.quantity_input.ids.quantity.text=str(self.cart[f_id][3])
            else:
                self.dialog.content_cls.ids.quantity_input.ids.quantity.text="0"
        except:
            pass
        self.dialog.open()
    
    def add_to_cart(self,f_id,f_name,res_id,price,image,*args):
        if self.dialog.content_cls.ids.quantity_input.ids.quantity.text:
            if int(self.dialog.content_cls.ids.quantity_input.ids.quantity.text)!=0:
                self.cart[f_id]=[f_name,res_id,price,int(self.dialog.content_cls.ids.quantity_input.ids.quantity.text),image]
                self.dialog.dismiss()
                toast("Added To Cart Successfully")
            else:
                del self.cart[f_id]
                toast("Please select a valid quantity")
        else:
            toast("Please select a valid quantity")

    def show_cart_screen(self,*args):
        
        self.ids.orders_sm.current="cart"

        self.ids.cart_items.clear_widgets()
        
        if self.cart:
            self.ids.place_order_btn.disabled=False
        self.total=0
        for i in self.cart.keys():
            
            box=MDBoxLayout(orientation='horizontal',size_hint_x=1,padding=(10,0),size_hint_y=None,height="110dp")
            c=CartCard(orientation='horizontal',elevation=30,size_hint=(0.95,None),height="100dp",ripple_behavior=True,pos_hint={'center_y':0.5},on_release=partial(self.edit_cart_item_quantity,i))
            
            
            c.add_widget(Image(texture=CoreImage(BytesIO(self.cart[i][4]),ext="jpg").texture,size_hint=(0.9,0.9 ),allow_stretch=True))
            c.add_widget(MDLabel(text=str(self.cart[i][0] +"\n" + "Rs "+str(self.cart[i][2])),halign="center",theme_text_color="Custom",text_color=(1,1,1,1),markup=True))
            c.add_widget(MDLabel(text="Qt \n"+str(self.cart[i][3]),halign="center",theme_text_color="Custom",text_color=(1,1,1,1),markup=True))
            c.add_widget(MDLabel(text="Total"+"\n"+"Rs "+str(self.cart[i][3]*self.cart[i][2]),halign="center",theme_text_color="Custom",text_color=(1,1,1,1),markup=True))
            box.add_widget(c)
            box.add_widget(MDIconButton(icon="close-circle",theme_text_color="Custom",text_color=(0,0,0,1),user_font_size="20sp",pos_hint={'center_x':0.5 , 'center_y':0.5 },on_release=partial(self.remove_food_from_cart,i)))
            
            self.ids.cart_items.add_widget(box)

            self.total+=int(self.cart[i][2])*int(self.cart[i][3])
        

        self.ids.cart_total.text=f"[b]Total : Rs {self.total}[/b]"
        


    def remove_food_from_cart(self,f_id,*args):
        l=list(self.cart.keys())
        ind=l.index(f_id)
        self.ids.cart_items.remove_widget(self.ids.cart_items.children[len(self.ids.cart_items.children)-ind-1])
        self.total=self.total-int(self.cart[f_id][2])*int(self.cart[f_id][3])
        self.ids.cart_total.text=f"[b]Total : Rs {self.total}[/b]"
        del self.cart[f_id]

        

        if not self.cart:
            self.ids.place_order_btn.disabled=True
    
    def edit_cart_item_quantity(self,f_id,*args):
        self.edit_cart_item_dialog = MDDialog(
            title="Edit Quantity",
            type="custom",
            content_cls=Dialog_Content(),
            buttons=[
                MDRaisedButton(
                    text="CANCEL",on_release=lambda x:self.edit_cart_item_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="SAVE",on_release=lambda x:self.save_cart_item_quantity(f_id)
                ),
            ],
        )
        
        
        self.edit_cart_item_dialog.content_cls.ids.fo_name.text=f"[b]{self.cart[f_id][0]}[/b]"
        self.edit_cart_item_dialog.content_cls.ids.fo_price.text=f"[b]Rs {self.cart[f_id][2]}[/b]"
        self.edit_cart_item_dialog.content_cls.ids.quantity_input.ids.quantity.text=""
        
        self.edit_cart_item_dialog.content_cls.ids.quantity_input.ids.quantity.text=str(self.cart[f_id][3])
            
        self.edit_cart_item_dialog.open()
    
    def save_cart_item_quantity(self,f_id,*args):
        
        if not int(self.edit_cart_item_dialog.content_cls.ids.quantity_input.ids.quantity.text):
            toast("Please select a valid quantity")
        else:
            self.total=self.total-int(self.cart[f_id][2])*int(self.cart[f_id][3])


            self.cart[f_id][3]=int(self.edit_cart_item_dialog.content_cls.ids.quantity_input.ids.quantity.text)
            l=list(self.cart.keys())
            ind=l.index(f_id)


            self.ids.cart_items.children[len(self.ids.cart_items.children)-ind-1].children[1].children[1].text="Quantity \n\n\n\n"+str(self.cart[f_id][3])

            self.ids.cart_items.children[len(self.ids.cart_items.children)-ind-1].children[1].children[0].text="Total"+"\n\n\n\n"+"Rs "+str(self.cart[f_id][3]*self.cart[f_id][2])
            self.edit_cart_item_dialog.dismiss()

            self.total=self.total+int(self.cart[f_id][2])*int(self.cart[f_id][3])
            self.ids.cart_total.text=f"[b]Total : Rs {self.total}[/b]"


    
    def display_restaurants(self,*args):
        global rest_list
        double=False
        self.ids.res_food_list.clear_widgets()
        
        if not rest_list:
            double=True
            
            mydb.commit()
            sql=f"Select Restaurant_Id,Name,Image from restaurants Where City='{self.city}' and State='{self.state}'"
            cursor.execute(sql)
            res=cursor.fetchall()
            rest_list=res[:]
        else:
            double=False
            
        
        


        
        for i in rest_list:
            c=MyCard(orientation='horizontal',elevation=40,ripple_behavior=True,size_hint=(1,None),height="100dp",on_release=partial(self.display_food_menu,str(i[0])))
            
            
            c.add_widget(Image(texture=CoreImage(BytesIO(i[2]),ext="jpg").texture,size_hint=(0.9,0.9 ),allow_stretch=True))
            c.add_widget(MDLabel(text=str(i[1]),halign="center",theme_text_color="Custom",text_color=(1,1,1,1),font_style="H6"))

            self.ids.res_food_list.add_widget(c)
        if double:
            
            Clock.schedule_once(self.display_restaurants,0)

    def search(self,text,*args):
        global rest_list
        if text and len(text)>=3:
            self.ids.res_food_list.clear_widgets()
            sql=f"Select * from food_items Where (F_Name Like '%{text}%' OR Category Like '%{text}%') and City='{self.city}' and State='{self.state}' LIMIT 10"
            cursor.execute(sql)
            res=cursor.fetchall()

            for item in res:

                c=FoodCard(orientation='horizontal',elevation=40,ripple_behavior=True,size_hint=(1,None),height="100dp",on_release=partial(self.select_quantity,item[0],item[1],item[2],item[3],item[4],item[5]))


                c.add_widget(Image(texture=CoreImage(BytesIO(item[5]),ext="jpg").texture,size_hint=(0.9,0.9 ),allow_stretch=True))
                c.add_widget(MDLabel(text="[b]"+str(item[1])+"[/b]",halign="center",theme_text_color="Custom",text_color=(1,1,1,1),markup=True))

                if item[6]=="1":
                    c.add_widget(Image(source="images/veg.png"))
                elif item[6]=="0":
                    c.add_widget(Image(source="images/nonveg.png"))
                self.ids.res_food_list.add_widget(c)

            #mydb.commit()
            #sql=f"Select Restaurant_Id,Name,Image from restaurants Where Name Like '{text}%' and City='{self.city}' and State='{self.state}' LIMIT 5"
            #cursor.execute(sql)
            #res=cursor.fetchall()
            res=[]
            for r in rest_list:
                if text.lower() in r[1].lower():
                    res.append(r)
            

            for i in res:
                c=MyCard(orientation='horizontal',elevation=40,ripple_behavior=True,size_hint=(1,None),height="100dp",on_release=partial(self.display_food_menu,str(i[0])))


                c.add_widget(Image(texture=CoreImage(BytesIO(i[2]),ext="jpg").texture,size_hint=(0.9,0.9 ),allow_stretch=True))
                c.add_widget(MDLabel(text=str(i[1]),halign="center",theme_text_color="Custom",text_color=(1,1,1,1),font_style="H6"))

                self.ids.res_food_list.add_widget(c)
        elif not text:
            self.display_restaurants()

    def load_address_screen(self,*args):
        mydb.commit()
        sql=f"Select Address,State,City,Pincode from users Where Id='{self.userid}'"
        cursor.execute(sql)
        res=cursor.fetchall()

        self.ids.address.text=res[0][0]
        self.set_state_item(res[0][1])
        self.set_city_item(res[0][2])
        self.ids.pincode.text=str(res[0][3])

        self.ids.account_manager.current="address_screen"
        
    def save_address(self,*args):
        if self.ids.address.text and self.ids.pincode.text and self.ids.city.text!="City" and self.ids.state.text!="State":
            sql=f"Update users set Address='{self.ids.address.text}',City='{self.ids.city.text}',State='{self.ids.state.text}',Pincode='{self.ids.pincode.text}' Where Id='{self.userid}'"
            cursor.execute(sql)
            mydb.commit()

            toast("Saved successfully")
        else:
            toast("Please Fill All Details")
        

class MainApp(MDApp):
    def build(self):
        return User_Screen()

#MainApp().run()