from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label

kv = Builder.load_file("POSSystem.kv")

class SigninWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def validate_user(self):
        user = self.ids.username_field
        pwd = self.ids.pwd_field
        info = self.ids.info
        
        uname = user.text
        passw= pwd.text
        
        if uname == '' or passw == '':
            info.text = '[color=#FF0000]username and/or password required[color=#FF0000]'
        else:
            if user == 'admin' or passw == 'admin':
                info.text = '[color=#00FF00]Logged In successfully[color=#00FF00]'
                App.get_running_app().root.current = "operator"
            else:
                info.text = '[color=#FF0000]invalid username and/or password[color=#FF0000]'

class OperatorWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total = 0.00
        self.prod_qty = {}
        self.prod_total = {}
        self.info = "Domlur Branch,\nBengaluru\nReceipt No. \nDate: \n\n"


    def update_purchases(self):
        pqty = self.ids.qty_inp.text
        pdisc = self.ids.disc_inp.text
        pdiscperc = self.ids.disc_perc_inp.text
        pval = self.ids.val_inp.text
        pprice = self.ids.price_inp.text
        pcode = self.ids.code_inp.text
        ptot = int(pqty)*(int(pprice)-int(pdisc)+int(pval))
        ptotal=str(ptot)
        products_container = self.ids.products
        details = BoxLayout(size_hint_y=None, height=30, pos_hint={'top':1})
        products_container.add_widget(details)
        pname = "Product "+pcode
        code = Label(text=pcode, size_hint_x=.2, color=(.06,.45,.45,1))
        name = Label(text=pname, size_hint_x=.3, color=(.06,.45,.45,1))
        qty = Label(text=pqty, size_hint_x=.1, color=(.06,.45,.45,1))
        disc = Label(text=pdisc, size_hint_x=.1, color=(.06,.45,.45,1))
        price = Label(text=pprice, size_hint_x=.1, color=(.06,.45,.45,1))
        total = Label(text=ptotal, size_hint_x=.2, color=(.06,.45,.45,1))
        details.add_widget(code)
        details.add_widget(name)
        details.add_widget(qty)
        details.add_widget(disc)
        details.add_widget(price)
        details.add_widget(total)
        self.total += int(ptotal)
        self.ids.cur_product.text = pname
        self.ids.cur_price.text = str(pprice)
        if pcode in self.prod_qty:
            self.prod_qty[pcode]=str(int(self.prod_qty[pcode])+int(pqty))
            self.prod_total[pcode]=str(int(self.prod_total[pcode])+int(ptotal))
        else:
            self.prod_qty[pcode]=pqty
            self.prod_total[pcode]=ptotal
        preview = self.ids.receipt_preview
        nu_preview= self.info
        for pc in self.prod_qty:
            nu_preview = "\n"+nu_preview+"Product "+pc+" x"+str(self.prod_qty[pc])+" =  "+str(self.prod_total[pc])+"\n"
        nu_preview= nu_preview + "total=", str(self.total);
        preview.text = ''.join(nu_preview)

class WindowManager(ScreenManager):
    pass

class POSSystemApp(App):
    def build(self):
        return WindowManager()

if __name__=="__main__":
    POSSystemApp().run()