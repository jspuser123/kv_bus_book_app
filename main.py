from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivymd.uix.pickers import MDDatePicker
from kivy.clock import Clock
from kivymd.uix.card import MDCard
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout 
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.behaviors import HoverBehavior
from kivymd.toast import toast
from kivymd.uix.list import OneLineListItem

from kivymd.uix.datatables import MDDataTable
from typing import Union
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar

from kivy.network.urlrequest import UrlRequest
import sqlite3
import webbrowser
import json


import login
import home



class Loading_screen(Screen):
    pass
class Mcrd3(MDCard,HoverBehavior):
    ti=.4
    def on_enter(self, *args):
       
        Animation(size_hint=(0.8, .4),pos_hint={'center_x': 0.5,'center_y': 0.5},d=self.ti).start(self)
        
    def on_leave(self, *args):
       
        Animation(size_hint=(.7, .5),pos_hint={'center_x': 0.5,'center_y': 0.01},d=self.ti).start(self)
class Mcrd4(MDCard,HoverBehavior):
    def on_enter(self, *args):
        self.md_bg_color="red"
    def on_leave(self, *args):
        self.md_bg_color="blue"
       
        
class Content(Screen):
    pass
        

class MainApp(MDApp):

    sm = ScreenManager()
    x=0     
    
    def build(self):
        self.theme_cls.theme_style='Dark'
        self.theme_cls.primary_palette='Blue'
        Builder.load_file("loading.kv")
        self.sm.add_widget(Loading_screen(name='loading'))
                   
        return self.sm
    
    def on_start(self):
        Clock.schedule_interval(self.execute_fun, 1)
       # Clock.schedule_once(self.login_page,10)
        self.edit_id=None
        self.date_booking=None
        self.from_select =None
        self.to_select =None
        self.bus_select =None
        self.seet_count =None
        self.passanger =None
        self.bus_ticket_list=None
    def on_leave(self,*args):
        self.db.commit()
        self.db.close()
       
    def execute_fun(self,dt,*args):
      
        self.x+=10
        self.sm.get_screen('loading').ids.process_bar.value=self.x
        self.scr_loading(dt)
        print(self.x)
        if self.x == 50:
            Clock.unschedule(self.execute_fun)
            self.login_page(dt)
                
     
    def scr_loading(self,dt):
        if self.x == 20:
            Builder.load_file("login.kv")
            self.sm.add_widget(login.Login_page(name='login1'))
        elif self.x == 30:
            Builder.load_file("home.kv")
            self.sm.add_widget(home.Frist_screen(name='home'))   
        elif self.x == 40:
            self.date_dialog = MDDatePicker(min_year=2000, max_year=2040)
            self.show_bottom_info()
    def login_page(self,dt):
        print("log fun")
        self.sm.current = 'login1'
        Clock.schedule_interval(self.next_slide, 4)

    def show_bottom_info(self):
        show_news_dict=[
            {'loc_id':'thanjavur','title':'thanjavur','body':'thanjavur is wonder full city','imgs':'img/t1.jpg'}, 
            {'loc_id':'trichy','title':'trichy','body':'trichy is wonder full city','imgs':'img/t2.jpeg'},
            {'loc_id':'kovi','title':'kovi','body':'kovi is wonder full city','imgs':'img/t3.jpeg'},
            {'loc_id':'kaniyakumari','title':'kaniyakumari','body':'kaniyakumari is wonder full city','imgs':'img/t4.jpeg'},
            {'loc_id':'channai','title':'channai','body':'channai is poor full city','imgs':'img/t6.jpeg'},
        ]  
        self.sm.get_screen('home').ids.show_news_list.clear_widgets()
        for news in show_news_dict:
            lbl_title=MDLabel(text=str(news.get('title')),bold=True,font_style="Subtitle1",halign="left",pos_hint={"center_y": .8})
            lbl_content=MDLabel(text=str(news.get('body')),opposite_colors=True,bold=True,font_style="Body1",halign="left",pos_hint={"center_y": .5})
            img_news=FitImage(source=news.get('imgs') ,radius=(10,10,10,10))
            lyt1=MDRelativeLayout(radius=(10,10,10,10))
            show_news_crd=Mcrd4(id=str(news.get('loc_id')),size_hint_y=None,radius=(10,10,10,10),ripple_behavior=True,md_bg_color="blue")
            lyt1.add_widget(lbl_title)
            lyt1.add_widget(lbl_content)
            show_news_crd.add_widget(img_news)
            show_news_crd.add_widget(lyt1)
            show_news_crd.opacity=0
            self.sm.get_screen('home').ids.show_news_list.add_widget(show_news_crd)
            Animation(opacity=1,duration=.50).start(show_news_crd)
        
    def next_slide(self,dt):
        self.sm.get_screen('home').ids.change_carosel_id.index+=1


    def change_screen_bus(self):
        self.sm.get_screen('home').ids.bottom_nav.switch_tab("screen 2")
        
    def show_date_picker(self):
        self.date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        self.date_dialog.open()
    def on_cancel(self, instance, value):
        print(value)

    def on_save(self, instance, value, date_range):     
        self.sm.get_screen('home').ids.date_display.text=str(value)
        self.date_booking=str(value)
        self.from_list_select()
    def from_list_select(self):
        self.sm.get_screen('home').ids.from_list.clear_widgets()
        self.dict1=[{"place_id":"thanjavur","place":"thanjavur","icon_name":"heart-outline","place_img":"img/t1.jpg"},{"place_id":"trichy","place":"trichy","icon_name":"heart","place_img":"img/t2.jpeg"},{"place_id":"kovai","place":"kovai","icon_name":"heart-outline","place_img":"img/t3.jpeg"},{"place_id":"kaniyakumari","place":"kaniyakumari","icon_name":"heart-outline","place_img":"img/t4.jpeg"},{"place_id":"channai","place":"channai","icon_name":"heart-outline","place_img":"img/t5.jpeg"},]    
        for plce in self.dict1:
            lbl=MDLabel(text=str(plce.get('place')),pos_hint={"x": .1, "center_y": .15},opposite_colors=True,bold=True,font_style="H5")
            icn=MDIconButton(icon=plce.get('icon_name'),theme_text_color="Custom",text_color="red",pos_hint= {"center_x": .8, "center_y": .9},on_press=self.heart_teach)
            im=FitImage(source=plce.get('place_img') ,radius=(25,25,25,25))
            slyt=MDRelativeLayout(radius=(25,25,25,25))
            im.opacity=0
            slyt.add_widget(im)
            slyt.add_widget(lbl)
            slyt.add_widget(icn)
            x=MDCard( orientation='vertical',md_bg_color='blue',id=plce.get('place_id'),on_press=self.to_list_screen,size_hint_y=None,height=300,radius=(25,25,25,25),ripple_behavior=True)
            x.opacity=0
            x.add_widget(slyt)
                                    
            self.sm.get_screen('home').ids.from_list.add_widget(x)
            
            Animation(opacity=1,duration=.50).start(x)
            Animation(opacity=1,duration=.50).start(im)
        # self.dict1 = dict(zip(datas, values1))    
    def to_list_screen(self, instance):
	       
	       self.from_select = instance.id
	       self.sm.get_screen('home').ids.tabs.switch_tab("To Loc")
	       self.sm.get_screen('home').ids.to_list.clear_widgets()
	       for plce in self.dict1:
	       	lbl=MDLabel(text=str(plce.get('place')),pos_hint={"x": .1, "center_y": .15},opposite_colors=True,bold=True,font_style="H5")
	       	icn=MDIconButton(icon=plce.get('icon_name'),theme_text_color="Custom",text_color="red",pos_hint= {"center_x": .8, "center_y": .9},on_press=self.heart_teach)
	       	im=FitImage(source=plce.get('place_img') ,radius=(25,25,25,25))
	       	slyt=MDRelativeLayout(radius=(25,25,25,25))
	       	im.opacity=0
	       	slyt.add_widget(im)
	       	slyt.add_widget(lbl)
	       	slyt.add_widget(icn)
	       	x=MDCard( orientation='vertical',md_bg_color='blue',id=plce.get('place_id'),on_press=self.avl_bus_screen,size_hint_y=None,height=300,radius=(25,25,25,25),ripple_behavior=True)
	       	x.opacity=0
	       	x.add_widget(slyt)
	       	self.sm.get_screen('home').ids.to_list.add_widget(x)
	       	Animation(opacity=1,duration=.50).start(x)
	       	Animation(opacity=1,duration=.50).start(im)
    def avl_bus_screen(self,instance):


            if self.from_select == instance.id:
                toast("from to address same")

            else:
                self.to_select=instance.id
                self.sm.get_screen('home').ids.tabs.switch_tab("avl bus")
                self.sm.get_screen('home').ids.avl_bus_id.clear_widgets()
                self.avl_bus_seet_get_list=[
                    {'bus_id':'mera','bus':'mera','bus_img':'img/bus_bid1.png','seet_total':'40','booking_seet':[4,5],'pending_set':None,},
                    {'bus_id':'sks','bus':'sks','bus_img':'img/bus_bid2.png','seet_total':'40','booking_seet':[5,7,8],'pending_set':None,}, 
                
                ]   
                for bus in self.avl_bus_seet_get_list:
                    lbl_bus=MDLabel(text=str(bus.get('bus')),opposite_colors=True,bold=True,font_style="H5")
                    im_bus=FitImage(source=bus.get('bus_img') ,radius=(25,25,25,25))
                    bus_add_list=Mcrd4(id=bus.get('bus_id'),on_press=self.bus_seet_fun,size_hint_y=None,radius=(25,25,25,25),ripple_behavior=True,md_bg_color="blue")
                    bus_add_list.add_widget(lbl_bus)
                    bus_add_list.add_widget(im_bus)
                    bus_add_list.opacity=0
                    self.sm.get_screen('home').ids.avl_bus_id.add_widget(bus_add_list)
                    Animation(opacity=1,duration=.50).start(bus_add_list)
    def bus_seet_fun(self,instance):
        #self.img_path=instance.im_bus
        self.bus_select=instance.id
        self.seet_list=[]
        self.seet_lists=None
        self.sm.get_screen('home').ids.tabs.switch_tab( "seet bus")
        self.sm.get_screen('home').ids.seet_list_add_id.clear_widgets()
        for seet_get in self.avl_bus_seet_get_list:
            if instance.id == seet_get.get("bus_id"):
                self.seet_lists=seet_get
        for seet in range(int(self.seet_lists.get('seet_total'))):
            seet_icn=MDIconButton(icon="checkbox-blank",theme_text_color="Custom",text_color="blue",id=f"bus seet:{str(seet)}",on_press=self.seet_booking,icon_size="30sp")
            slyt2=MDRelativeLayout(size_hint=(None,None),width=50,height=50)
            if seet in self.seet_lists.get('booking_seet'):
                seet_icn=None
                seet_icn=MDIconButton(icon="checkbox-blank",theme_text_color="Custom",text_color="gray",icon_size="30sp")
            slyt2.add_widget(seet_icn)
            if seet == 1:
                slyt2.width=100
            self.sm.get_screen('home').ids.seet_list_add_id.add_widget(slyt2)
        self.sm.get_screen('home').ids.conform_seeet_btn.opacity=1 
    def seet_booking(self,instance):
        if instance.text_color == [0.0, 0.0, 1.0, 1.0]:
            self.sm.get_screen('home').ids.seet_booking_id.add_widget(OneLineListItem(text=str(instance.id),theme_text_color="Custom",text_color="blue"))
            instance.text_color=[1,0,2,3]
            self.seet_list.append(instance.id)
            total_price=len(self.seet_list)*140
            self.sm.get_screen('home').ids.price_display.text=str(total_price)
        else:
            instance.text_color=[0.0, 0.0, 1.0, 1.0]
            print(str(self.seet_list))
            self.seet_list.remove(instance.id)
            total_price=len(self.seet_list)*140
            self.sm.get_screen('home').ids.price_display.text=str(total_price)
            self.sm.get_screen('home').ids.seet_booking_id.clear_widgets()
            for seets in self.seet_list:
                self.sm.get_screen('home').ids.seet_booking_id.add_widget(OneLineListItem(text=str(seets),theme_text_color="Custom",text_color="blue"))
    def table_fun(self):
        self.sm.get_screen('home').ids.tabs.switch_tab( "table screen")
        self.sm.get_screen('home').ids.table_add.clear_widgets()
        self.sm.get_screen('home').ids.add_table_btn.opacity=1
        self.sm.get_screen('home').ids.edit_table_btn.opacity=1
        self.sm.get_screen('home').ids.delete_table_btn.opacity=1
        self.sm.get_screen('home').ids.checkout_table_btn.opacity=1
        
        self.db = sqlite3.connect('main1.db')
        self.conn=self.db.cursor()
        self.conn.execute('SELECT * from passanger')
        self.data_tables = MDDataTable(
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            size_hint=(1,1),
            use_pagination=True,
            check=True,
            column_data=[
                ("Name", dp(30)),
                ("Gender", dp(20)),
                ("Age", dp(20)),
            
            ],
            row_data=[(i) for i in self.conn],
            )
        
        self.data_tables.bind(on_check_press=self.on_check_press) 
        self.sm.get_screen('home').ids.table_add.add_widget(self.data_tables)
        self.db.commit()
        
        
        
        
        # self.db.close()
    def on_check_press(self, instance_table, current_row ):
        pass
       
    def dialogfun(self):
        self.dialog = MDDialog(
                    title="Address:",
                    type="custom",
                    content_cls=Content(),
                    buttons=[
                        MDRaisedButton(
                            text="CANCEL",
                            on_press=self.cancel_fun
                            
                        ),
                        MDRaisedButton(
                            text="ok",
                            on_press=self.form_submit
                           
                        
                        ),
                    ],
                )
        self.dialog.open()
    def form_submit(self ,instance_button: MDRaisedButton,*args):
        #print(Content().ids['sc'].MDTextField.text)
        self.dialog.dismiss()
        a=self.dialog.content_cls.ids['sc'].text
        ch1=self.dialog.content_cls.ids['passager_male_true'].active
        ch2=self.dialog.content_cls.ids['passager_female_true'].active
        c=self.dialog.content_cls.ids['passager_age'].text
        if ch1 == True:
            b = 'male'
        elif ch2 == True:
            b = 'female'
        # self.db = sqlite3.connect('main1.db')
        # self.conn=self.db.cursor()
        sql = ("insert into passanger(name,gender,age) values(?,?,?);")
        self.conn.execute(sql, (a, b,c))    
        self.db.commit()
        
        self.conn.execute('SELECT * from passanger')
        self.data_tables.row_data=[(i) for i in self.conn]
        self.db.commit()
        
        
    def cancel_fun(self,instance_button: MDRaisedButton):
        self.dialog.dismiss()
    def on_check_press(self, instance_table, current_row ):
        self.edit_id=current_row[0]
        self.edit_name=current_row[0]
        self.edit_gender=current_row[1]
        self.edit_age=current_row[2]
        #print(self.data_tables.check)
    
 
    def form_edit(self):
        self.dialog1 = MDDialog(
                    title="Address:",
                    type="custom",
                    content_cls=Content(),
                    buttons=[
                        MDRaisedButton(
                            text="CANCEL",
                            on_press=self.form_edit_close
                            
                        ),
                        MDRaisedButton(
                            text="ok",
                            on_press=self.form_edit_submit
                           
                        
                        ),
                    ],
                )
        self.dialog1.open()
        self.dialog1.content_cls.ids['sc'].text=self.edit_name
        if self.edit_gender == 'male':
            self.dialog1.content_cls.ids['passager_male_true'].active = True
        else:
            self.dialog1.content_cls.ids['passager_female_true'].active= True
        self.dialog1.content_cls.ids['passager_age'].text =self.edit_age
    def form_edit_submit(self,*args):
        self.dialog1.dismiss()
        a=self.dialog1.content_cls.ids['sc'].text
        ch1=self.dialog1.content_cls.ids['passager_male_true'].active
        ch2=self.dialog1.content_cls.ids['passager_female_true'].active
        c=self.dialog1.content_cls.ids['passager_age'].text
        if ch1 == True:
            b = 'male'
        elif ch2 == True:
            b = 'female'
        if self.edit_id:
            sql = "update passanger set name=?,gender=?,age=? where name=?"
            self.conn.execute(sql, (a,b,c,self.edit_id))
            self.db.commit()
            self.conn.execute('SELECT * from passanger')
            self.data_tables.row_data=[(i) for i in self.conn]
            self.db.commit()
    def form_edit_close(self,*args):
        self.dialog1.dismiss()
    def remove_row(self,*args):
        if  self.edit_id:           
            qry="delete from passanger where name=?"
            self.conn.execute(qry,(self.edit_id,))
            self.db.commit()
            self.conn.execute('SELECT * from passanger')
            self.data_tables.row_data=[(i) for i in self.conn]
            self.db.commit()
            self.edit_id=None
            print("is id",self.edit_id) 
        else:
            print("row data in none ")
            toast("Delete pls one row select")
    def checkout(self):
        self.sm.get_screen('home').ids.tabs.switch_tab( "check_screen")
        self.sm.get_screen('home').ids.check_screen_id.clear_widgets()
        self.seet_count=len(self.seet_list)
        self.conn.execute('SELECT * from passanger')
        self.passanger=[(i) for i in self.conn]
        self.price=self.seet_count*140
        self.db.commit()
        slyt1=MDRelativeLayout(radius=(25,25,25,25))

        if self.from_select and self.to_select and self.bus_select and self.seet_count and self.passanger and self.date_booking:
            lbl1=MDLabel(text=f"From:{str(self.from_select)}",halign="left",pos_hint={"center_y": .2},opposite_colors=True,bold=True,font_style="H4")
            lbl2=MDLabel(text=f"To:{str(self.to_select)}",halign="left",pos_hint={"center_y": .3},opposite_colors=True,bold=True,font_style="H4")
            lbl3=MDLabel(text=str(self.bus_select),halign="left",pos_hint={"center_y": .4},bold=True,font_style="H6")
            lbl4=MDLabel(text=f"bus seet:{str(self.seet_count)}",halign="left",pos_hint={"center_y": .45},bold=True,font_style="H6")
            lbl5=MDLabel(text=f"passenger:{str(len(self.passanger))}",halign="left",pos_hint={"center_y": .5},bold=True,font_style="H6")
            lbl6=MDLabel(text=f"Date:{str(self.date_booking)}",halign="left",pos_hint={"center_y": .55},bold=True,font_style="H5")
            lbl7=MDLabel(text=f"Price:{str(self.price)}",halign="right",pos_hint={"center_y": .55},bold=True,font_style="H5")
            slyt1.add_widget(lbl1)
            slyt1.add_widget(lbl2)
            slyt1.add_widget(lbl3)
            slyt1.add_widget(lbl4)
            slyt1.add_widget(lbl5)
            slyt1.add_widget(lbl6)
            slyt1.add_widget(lbl7)

        icn1=MDRaisedButton(text="process to pay",md_bg_color="red",pos_hint= {"center_x": .5, "center_y": .08},on_press=self.process_to_pay)
        im1=FitImage(source="img/t2.jpeg" ,radius=(25,25,25,25),size_hint=(1,.4),pos_hint= {"top":1})
        
        im1.opacity=0
        slyt1.add_widget(im1)
       
        slyt1.add_widget(icn1)
        x1=MDCard( orientation='vertical',size_hint=(.9,.8),pos_hint= {"center_x": .5, "center_y": .55},radius=(25,25,25,25),ripple_behavior=True, spacing="5dp",padding="5dp")
        x1.opacity=0
        x1.add_widget(slyt1)
        self.sm.get_screen('home').ids.check_screen_id.add_widget(x1)
        Animation(opacity=1,duration=.50).start(x1)
        Animation(opacity=1,duration=.50).start(im1)
    def process_to_pay(self,*args):
        self.sm.get_screen('home').ids.check_screen_id.clear_widgets()
        values={
            "from":self.from_select, 
            "To":self.to_select, 
            "bus":self.bus_select, 
            "seet":self.seet_list, 
            "passger":self.passanger, 
            "date":self.date_booking,
            "price":self.price,
            }
        # values = {'email':'wilson@gmail.com', 'pass1':'wilson'}
        params = json.dumps(values)
        headers = {'Content-type': 'application/json','Accept': 'text/plain'}
        self.req = UrlRequest('http://127.0.0.1:5000/payment',on_error=self.error_fun,on_failure=self.fail_fun,on_success=self.scuess_full, req_body=params,req_headers=headers)
        self.req.wait()
       
        
    def scuess_full(self,*args):
        d=self.req.result
        a=d['data']
        print(a)
        webbrowser.open("http://127.0.0.1:5000/payment_link")
        self.sm.get_screen('home').ids.bottom_nav.switch_tab("screen 3")
        
    def error_fun(self,*args):
        print("error reponse")
        toast("Network Error pls Try Agin")
       # plyer.notification.notify(title='RequestService', message="error reponse")
    def fail_fun(self,*args):
        print("fail reponse")
        toast("Network Error pls Try Agin")
        # plyer.notification.notify(title='RequestService', message="fail reponse")
    def tickets_get_fun(self,*args):
        values={
            "userid":"js" 
            }
        # values = {'email':'wilson@gmail.com', 'pass1':'wilson'}
        params = json.dumps(values)
        headers = {'Content-type': 'application/json','Accept': 'text/plain'}
        self.req1 = UrlRequest('http://127.0.0.1:5000/tickets',on_error=self.error_fun1,on_failure=self.fail_fun1,on_success=self.scuess_full1, req_body=params,req_headers=headers)
        self.req1.wait()
    def scuess_full1(self,*args):
        self.bus_ticket_list=self.req1.result
        print(self.bus_ticket_list)
        self.tickets_add_card()     
    def error_fun1(self,*args):
        print("error reponse")
        self.fail_reponse_fun()

    def fail_fun1(self,*args):
        print("fail reponse")
        self.fail_reponse_fun()
    def fail_reponse_fun(self):
        self.sm.get_screen('home').ids.tickets_showing_id.clear_widgets()
        lbl1=MDLabel(text="Network Error Pls Try Agin",halign="center",valign="center",opposite_colors=True,bold=True,font_style="H2")
        t_card=MDCard( orientation='vertical',size_hint_y=None,height="300dp",radius=(25,25,25,25),ripple_behavior=True, spacing="5dp",padding="5dp")
        t_card.opacity=0
        t_card.add_widget(lbl1)
        self.sm.get_screen('home').ids.tickets_showing_id.add_widget(t_card)
       


    def tickets_add_card(self):
        if self.bus_ticket_list == None:
            self.bus_ticket_list={
                "From":"trupur",
                "To":"Thanjavr",
                "bus":"meera",
                "seet":"2seets",
                "passerger detalis":"jagan",
                "Date": self.date_booking,
                "price":"140"
            }

        self.sm.get_screen('home').ids.tickets_showing_id.clear_widgets()
        slyt1=MDRelativeLayout(radius=(25,25,25,25))
        lbl1=MDLabel(text=self.bus_ticket_list['From'],halign="left",pos_hint={"center_y": .55},opposite_colors=True,bold=True,font_style="H4")
        lbl2=MDLabel(text=self.bus_ticket_list["To"],halign="right",pos_hint={"center_y": .55},opposite_colors=True,bold=True,font_style="H4")
        lbl3=MDLabel(text=self.bus_ticket_list['bus'],halign="left",pos_hint={"center_y": .4},bold=True,font_style="H6")
        lbl4=MDLabel(text=self.bus_ticket_list['seet'],halign="right",pos_hint={"center_y": .4},bold=True,font_style="H6")
        lbl5=MDLabel(text=f"passerger detalis:\n{self.bus_ticket_list['passerger detalis']}",halign="left",pos_hint={"center_y": .3},bold=True,font_style="H6")
        lbl6=MDLabel(text=f"Date:{self.bus_ticket_list['Date']}",halign="center",pos_hint={"center_y": .9},bold=True,font_style="H5")
        lbl7=MDLabel(text=self.bus_ticket_list['price'],halign="center",pos_hint={"center_y": .1},bold=True,font_style="H5")
        slyt1.add_widget(lbl1)
        slyt1.add_widget(lbl2)
        slyt1.add_widget(lbl3)
        slyt1.add_widget(lbl4)
        slyt1.add_widget(lbl5)
        slyt1.add_widget(lbl6)
        slyt1.add_widget(lbl7)
        t_card=MDCard( orientation='vertical',size_hint_y=None,height="400dp",radius=(25,25,25,25),ripple_behavior=True, spacing="5dp",padding="5dp")
        t_card.opacity=0
        t_card.add_widget(slyt1)
        self.sm.get_screen('home').ids.tickets_showing_id.add_widget(t_card)
        Animation(opacity=1,duration=.50).start(t_card)
        
    def heart_teach(self,instance):
		   if instance.icon == "heart-outline":
		   	instance.icon="heart"
		   else:
		   	instance.icon="heart-outline"

if __name__ == "__main__":
    MainApp().run()