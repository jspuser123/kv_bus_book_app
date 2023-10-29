from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivymd.uix.pickers import MDDatePicker
from kivy.clock import Clock
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import HoverBehavior

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
    def login_page(self,dt):
        print("log fun")
        self.sm.current = 'login1'
        
    def show_date_picker(self):
        self.date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        self.date_dialog.open()
    def on_cancel(self, instance, value):
        print(value)

    def on_save(self, instance, value, date_range):     
       #self.sm.get_screen('sc2').ids.tdate.text=str(value)
        print(value)

if __name__ == "__main__":
    MainApp().run()