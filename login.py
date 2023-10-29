from kivy.uix.screenmanager import  Screen


class Login_page(Screen):
   
        def login_validate(self):
            a=self.ids.user1.text
            b=self.ids.pass1.text
            if a == 'js' and b == "123":
                self.manager.current = 'home'
            else:
                Snackbar(text="[color=#ddbb34]login failed try agin[/color]",snackbar_x="5dp",snackbar_y="10dp",size_hint_x=.9,bg_color=(0, 0, 1, 1)).open()
