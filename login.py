from kivy.uix.screenmanager import  Screen
from kivymd.uix.snackbar import Snackbar
from firebase import firebase
class Login_page(Screen):
   
        def login_validate(self):
            a=self.ids.user1.text
            b=self.ids.pass1.text
            db = firebase.FirebaseApplication("https://testfire-47042-default-rtdb.asia-southeast1.firebasedatabase.app/",None)
            # data={"user":"nadn","pass1":"1234"}
            # db.post("https://testfire-47042-default-rtdb.asia-southeast1.firebasedatabase.app/",data)
            result=db.get("https://testfire-47042-default-rtdb.asia-southeast1.firebasedatabase.app/","")
            print(result)

            if a == 'js' and b == "123":
                self.manager.current = 'home'
            else:
                Snackbar(text="[color=#ddbb34]login failed try agin[/color]",snackbar_x="5dp",snackbar_y="10dp",size_hint_x=.9,bg_color=(0, 0, 1, 1)).open()
