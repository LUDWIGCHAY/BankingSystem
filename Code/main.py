from tkinter import *
import mysql.connector
from tkinter import simpledialog
from tkinter import messagebox
import time
import os
from PIL import Image, ImageTk
from tkinter import ttk
import platform

os.system('cls')
system_info = platform.uname()

global system
global AppName
global bgcolor
global fgcolor
system = (system_info.system+ ' '+system_info.version+': '+ system_info.node)

AppName = 'EzBank'
bgcolor='#333333'
fgcolor='#ffffff'





host = 'localhost'
user='root'
password = ''
database= '1e'

host = 'sql12.freesqldatabase.com'
user = 'sql12621009'
password = 'tFsfBh1RYV'
database = user



class main:
    
    def __init__(self):
        self.db = mysql.connector.connect(host = host, user = user, passwd = password, database = database, port = '3306')
        self.cur = self.db.cursor()
        self.win=Tk()
        self.win.resizable(False,False)
        self.username = StringVar()
        self.passwd = StringVar()
        self.username.set('')
        self.passwd.set('')
        self.win.geometry("400x600")
        self.win.title("Banking Management System")
        try:
            image = Image.open("logo.png")
            self.tk_image= ImageTk.PhotoImage(image)
            self.win.iconbitmap('logo.ico')
        except:
            messagebox.showwarning('Logo cannot be loaded.','Kung nakita ni nimo ni, Dapat ang logo.ico ug ang logo.png naa pareha sa folder ining imo gi open nga main.exe! ')
        
       

        self.frame1=Frame(self.win, bg = bgcolor,height=600,width=400)
        self.frame1.propagate(False)
        self.frame1.pack()
        try:
            logo = Label(self.frame1,image=self.tk_image,bg=bgcolor)
            logo.pack()
            logo.place(x=100,y=80)
        except:
            ()
        l=Label(self.frame1,text=AppName, font = ('Roboto Thin',40),fg = fgcolor,bg = bgcolor)
        l.pack()
        l.place(x=200,y=100)

        l1=Label(self.frame1,text='username',font=('Roboto', 14), fg = fgcolor,bg = bgcolor)
        l1.pack()
        l1.place(x=30,y=200)

        l2=Label(self.frame1,text='password',font=('Roboto', 14), fg = fgcolor,bg = bgcolor)
        l2.pack()
        l2.place(x=30,y=240)

        self.ee1=Entry(self.frame1,font=('Roboto', 14),width=22,textvariable=self.username)
        self.ee1.pack()
        self.ee1.place(x=130,y=200)

        self.ee2=Entry(self.frame1,font=('Roboto', 14),show='•',textvariable=self.passwd)
        self.ee2.pack()
        self.ee2.place(x=130,y=240)
        def login():

            if self.ee1.get() == 'admin' and self.ee2.get() == 'admin':
                
                def refresh():
                    self.db.reset_session()
                    for item in tv.get_children():
                        tv.delete(item)
                    self.cur.execute("SELECT id,CREDENTIALS.username,name,address,pass,cash,added from balance,CREDENTIALS where CREDENTIALS.username=balance.username")
                    data = self.cur.fetchall()
                    for i in data:
                        tv.insert(parent='',index=END,values=i)

                    for item in tv1.get_children():
                        tv1.delete(item)
                    self.cur.execute("SELECT * from logs")
                    data = self.cur.fetchall()
                    for log in data:
                        tv1.insert('',0,values=log)

                adminwin = Toplevel(self.win)
                adminwin.config(bg=bgcolor)
                adminwin.title("ADMINISTRATOR")
                try:
                    adminwin.iconbitmap('logo.ico')
                except:
                    ()
                tv = ttk.Treeview(adminwin)
                tv.pack(padx=10,pady=10)
                
                tv['show']='headings'
                tv['columns']=('id','username','name','address','password','cash','date')
                tv.heading('id',anchor=CENTER,text='ID')
                tv.heading('username',anchor=CENTER,text='username')
                tv.heading('name',anchor=CENTER,text='Name')
                tv.heading('address',anchor=CENTER,text='Address')
                tv.heading('password',anchor=CENTER,text='Password')
                tv.heading('cash',anchor=CENTER,text='Balance')

                tv.heading('date',anchor=CENTER,text='Date Added')

                tv.column('id',width=30,anchor=CENTER)
                tv.column('username',width=150,anchor=CENTER)
                tv.column('name',width=200,anchor=CENTER)
                tv.column('address',width=150,anchor=CENTER)
                tv.column('password',width=150,anchor=CENTER)
                tv.column('cash',width=100,anchor=CENTER)
                tv.column('date',width=200,anchor=CENTER)
                

                tv1 = ttk.Treeview(adminwin)
                tv1.pack(pady=10,padx=10)

                tv1['columns'] = ('message','time')
                tv1['show'] = 'headings'
                tv1.heading('message',anchor=CENTER,text='Message')
                tv1.column('message',width=800,anchor=CENTER)
                tv1.heading('time',anchor=CENTER,text='timestamp')
                tv1.column('time',width=200,anchor=CENTER)
                Button(adminwin,text='Refresh',font = ("Roboto",13),command=lambda: refresh(),bg = '#df8053',fg=fgcolor).pack(pady=10)
                refresh()
                
            else:

                if self.ee1.get() == '':
                    messagebox.showerror("Error.","There's no such account that has empty username!")
                    return
                AccountExisted = False
                self.cur.execute('select * from CREDENTIALS')
                user = self.cur.fetchall()
                for username in user:
                    if self.ee1.get() == username[1]:
                        AccountExisted = True
                        
                if AccountExisted == False:
                    messagebox.showerror("Account not found.","Seems like username '"+self.ee1.get()+"' does not exist. Register now!")
                    return
                self.cur.execute('select pass from CREDENTIALS where username = "'+self.ee1.get()+'"')
                passwd = self.cur.fetchall()
                AccountExisted = False
                for key in passwd:
                    if key[0] == self.ee2.get():
                        AccountExisted = True
                if AccountExisted == False:
                    messagebox.showerror("Credentials Error.","Username and Password do not match.")
                    return
                self.USERNAME = self.ee1.get()
                sql1 = 'insert into logs (log) values ("%s logged in using %s.");'
                values1 = (self.USERNAME,system)
                self.cur.execute(sql1,values1)
                self.db.commit()
                
                self.mainpage()
                

        loginButton = Button(self.frame1,text='Log In',font = ('Roboto',12),width=20,bg='#df8053',fg='White',command = login)
        loginButton.pack()
        loginButton.place(x=150,y=280)
        

        registerButton = Button(self.frame1,text='Register',font = ('Roboto',12),width=20,command = self.register)
        registerButton.pack()
        registerButton.place(x=150,y=322)
        
        self.win.mainloop()
        

    def register(self):
        
        self.frame1.pack_forget()
        self.frame2=Frame(self.win, bg = bgcolor,height=600,width=400)
        self.frame2.propagate(False)
        self.frame2.pack()
        try:
            logo = Label(self.frame2,image=self.tk_image,bg=bgcolor)
            logo.pack()
            logo.place(x=100,y=80)
        except:
            ()
        l=Label(self.frame2,text=AppName, font = ('Roboto Thin',40),fg = fgcolor,bg = bgcolor)
        l.pack()
        l.place(x=200,y=100)
        

        l1=Label(self.frame2,text='fullname',font=('Roboto', 14), fg = fgcolor,bg = bgcolor)
        l1.pack()
        l1.place(x=30,y=180+20)

        l2=Label(self.frame2,text='address',font=('Roboto', 14), fg = fgcolor,bg = bgcolor)
        l2.pack()
        l2.place(x=30,y=220+20)

        l3=Label(self.frame2,text='username',font=('Roboto', 14), fg = fgcolor,bg = bgcolor)
        l3.pack()
        l3.place(x=30,y=260+20)

        l4=Label(self.frame2,text='password',font=('Roboto', 14), fg = fgcolor,bg = bgcolor)
        l4.pack()
        l4.place(x=30,y=300+20)

        self.e1=Entry(self.frame2,font=('Roboto', 14),width=22)
        self.e1.pack()
        self.e1.place(x=130,y=200)

        self.e2=Entry(self.frame2,font=('Roboto', 14),width=21)
        self.e2.pack()
        self.e2.place(x=130,y=240)

        self.e3=Entry(self.frame2,font=('Roboto', 14))
        self.e3.pack()
        self.e3.place(x=130,y=280)

        self.e4=Entry(self.frame2,font=('Roboto', 14),show='•',width=19)
        self.e4.pack()
        self.e4.place(x=130,y=320)
        def Register():
        
            if self.e1.get() == '':
                messagebox.showerror("Invalid Name",'Name cannot be empty.')
                return
            if len(self.e1.get()) < 5:
                messagebox.showerror("Invalid Name",'Name too short.')
                return
            if self.e2.get() == '':
                messagebox.showerror("Invalid Address",'Address cannot be empty.')
                return
            if self.e3.get() == '':
                messagebox.showerror("Invalid username",'Username cannot be empty.')
                return
            if len(self.e3.get()) < 4:
                messagebox.showerror("Invalid username",'Username too short.')
                return
            if self.e4.get() == '':
                messagebox.showerror("Invalid password",'Password cannot be empty.')
                return
            if len(self.e4.get()) < 4:
                messagebox.showerror("Invalid password",'Password must be at least 4 characters or digits.')
                return
            
            sql = "INSERT INTO CREDENTIALS (username,pass,name,address,added) values (%s,%s,%s,%s,%s)"
            values = self.e3.get(),self.e4.get(),self.e1.get(),self.e2.get(),time.ctime(time.time())
            self.cur.execute(sql,values)
            self.db.commit()
            
            
            self.cur.execute('insert into balance (username,cash) values ("'+self.e3.get()+'",0.00)')
            self.db.commit()
            messagebox.showinfo('Registered Successfully','Thank you for registering, '+self.e1.get()+'! \nYou may now log in with your new account to continue.')
            self.frame2.pack_forget()
            self.frame1.pack()
            sql1 = 'insert into logs (log) values ("New Account registered: %s (username: %s)")'
            values1 = (self.e1.get(),self.e3.get())
            self.cur.execute(sql1,values1)
            self.db.commit()
            
        saveButton = Button(self.frame2,text='Register',font = ('Roboto',12),width=20,bg='#df8053',fg='White',command=Register)
        saveButton.pack()
        saveButton.place(x=150,y=360)

        def cancelReg():
            self.frame2.pack_forget()
            self.frame1.pack()

        backButton = Button(self.frame2,text='Cancel',font = ('Roboto',12),width=20,command = cancelReg)
        backButton.pack()
        backButton.place(x=150,y=402)
        
        def shows():
            self.e4.configure(show = '•')
            show.config(text='Show')
            show.config(command = hide)
        def hide():
            self.e4.configure(show='')
            show.config(text='Hide')
            show.config(command = shows)

        show= Button(self.frame2,text= 'Show', font = ('Roboto',9),command = hide)
        show.pack()
        show.place(x=350,y=321)

    def mainpage(self):

        def refresh():
            updated.config(text='Updated '+time.strftime("%I:%M:%S %p", time.localtime()))
            self.db.reset_session()
            self.cur.execute('select cash from balance where balance.username = "'+self.USERNAME+'"')
            balance = self.cur.fetchall()
            for peso in balance:
                balance = peso[0]
            self.balance = balance
            cash.config(text=('P',balance))
            self.cur.execute('select name from CREDENTIALS where username = "'+self.USERNAME+'"')
            fullname = self.cur.fetchall()
            for z in fullname:
                fullname = z[0]
            l.config(text=fullname)
        
        self.frame1.pack_forget()
        self.frame3=Frame(self.win, bg = bgcolor,height=600,width=400)
        self.frame3.propagate(False)
        self.frame3.pack()
        

        l=Label(self.frame3, font = ('Roboto Light',23),fg = fgcolor,bg = bgcolor)
        l.pack(anchor=W,padx=10,pady=10)

        

        moneyFrame = Frame(self.frame3,height=100,width=380,highlightthickness=2,relief='sunken',bg=bgcolor,highlightbackground='gray')
        moneyFrame.propagate(False)
        moneyFrame.pack()
        cash = Label(moneyFrame,text=('P'),bg=bgcolor,fg=fgcolor,font=('Roboto Bold',39))
        cash.pack(side=BOTTOM,anchor=E,)

        lb = Label(moneyFrame,text='BALANCE',font=("Roboto",12),bg=bgcolor,fg=fgcolor)
        lb.pack()
        lb.place(x=8,y=65)

        buttonFrame = Frame(self.frame3,height=400,width=380,highlightthickness=0,relief='sunken',bg=bgcolor,highlightbackground='gray')
        buttonFrame.propagate(False)
        buttonFrame.pack(pady=10)

        def wd():
            refresh()
            buttonFrame.pack_forget()
            frame = Frame(self.frame3,height=400,width=380,highlightthickness=1,relief='sunken',bg=bgcolor,highlightbackground='gray')
            frame.propagate(False)
            frame.pack(pady=10)

            Label(frame,text='Withdraw Money',font=('Roboto Bold',30),bg=bgcolor,fg=fgcolor).pack(pady=20)

            l1=Label(frame,text='Amount to Withdraw',font=("roboto",13),bg=bgcolor,fg=fgcolor)
            l1.pack()
            l1.place(x=4,y=30+70)
            l2=Label(frame,text='Password',font=("roboto",13),bg=bgcolor,fg=fgcolor)
            l2.pack()
            l2.place(x=4,y=70+70)
            e2string=StringVar()
            e2string.set(0.0)
            e1=Entry(frame,font=("Roboto",13),width=18,textvariable=e2string)
            e1.pack()
            e1.place(x=180,y=30+70)
            
            e2=Entry(frame,font=("Roboto",13),width=18,show='•')
            e2.pack()
            e2.place(x=180,y=70+70)

            def confirm():
                try:
                    if float(e1.get()) < 20:
                        messagebox.showerror('Amount Error','Amount should be minimum of 20.')
                        return
                    if self.balance < float(e1.get()):
                        messagebox.showerror('Insufficient Balance','Not enough money balance to withdraw.')
                        return
                except:
                        messagebox.showerror('Amount Error','Please enter valid amount.')
                self.cur.execute('select pass from CREDENTIALS where username = "'+self.USERNAME+'"')
                Check = False
                passw = self.cur.fetchall()
                for key in passw:
                    if key[0] == e2.get():
                        Check = TRUE
                if Check == False:
                    messagebox.showerror('Error','Password is incorrect.')
                    return
                choice = messagebox.askokcancel('Confirm','Confirm to withdraw ( P'+str(float(e1.get()))+' ) ?')
                if choice == False:
                    return
                if choice:
                    print(self.balance)
                    sql = 'update balance set cash = %s where username = %s'
                    values = (float(self.balance)-float(e1.get()),self.USERNAME)
                    self.cur.execute(sql,values)
                    self.db.commit()
                    refresh()
                    buttonFrame.pack()
                    frame.pack_forget()
                    messagebox.showinfo("Withdrawal Successful","Successfully withdrawed P"+str(float(e1.get()))+" from your account!")
                    sql1 = 'insert into logs (log) values ("%s withdrawed P%s successfully.")'
                    values1 = (self.USERNAME,str(float(e1.get())))
                    self.cur.execute(sql1,values1)
                    self.db.commit()
                
                    

            wdbutton = Button(frame,text='Confirm',font = ("Roboto",13),width=15,bg='#df8053',fg=fgcolor,command=confirm)
            wdbutton.pack()
            wdbutton.place(y=250,x=110)
            def cancel():
                refresh()
                frame.pack_forget()
                buttonFrame.pack(pady=10)
            backbutton = Button(frame,text='Cancel',font = ("Roboto",13),width=15,command=cancel)
            backbutton.pack()
            backbutton.place(y=295,x=110)

        b1 = Button(buttonFrame,text='Withdraw Cash',font=("Roboto Bold",18),width=12,command=wd)
        b1.pack()
        b1.place(x=10,y=10)

        def dc():
            print(self.balance)
            input = simpledialog.askfloat(' ','Enter amount')
            if input:
                sql = 'update balance set cash = %s where username = %s'
                values = (str(float(self.balance+input)),self.USERNAME)
                self.cur.execute(sql,values)
                self.db.commit()
                sql1 = 'insert into logs (log) values ("%s deposited P%s successfully.")'
                values1 = (self.USERNAME,str(float(self.balance+input)))
                self.cur.execute(sql1,values1)
                self.db.commit()
                refresh()

        b2 = Button(buttonFrame,text='Deposit Cash',font=("Roboto Bold",18),width=12,bg = '#df8053', fg = fgcolor,command=dc)
        b2.pack()
        b2.place(x=194,y=10)



        

        def sendonline():
            refresh()
            buttonFrame.pack_forget()
            sendFrame = Frame(self.frame3,height=400,width=380,highlightthickness=1,relief='sunken',bg=bgcolor,highlightbackground='gray')
            sendFrame.propagate(False)
            sendFrame.pack(pady=10)

            Label(sendFrame,text='Send Cash Online',font=('Roboto Bold',30),bg=bgcolor,fg=fgcolor).pack(pady=20)

            l1=Label(sendFrame,text='Recipient (username)',font=("roboto",13),bg=bgcolor,fg=fgcolor)
            l1.pack()
            l1.place(x=4,y=30+70)
            l2=Label(sendFrame,text='Amount to Send (P)',font=("roboto",13),bg=bgcolor,fg=fgcolor)
            l2.pack()
            l2.place(x=4,y=70+70)

            e1=Entry(sendFrame,font=("Roboto",13),width=18)
            e1.pack()
            e1.place(x=180,y=30+70)
            e2string=StringVar()
            e2string.set(0.0)
            e2=Entry(sendFrame,font=("Roboto",13),width=18,textvariable=e2string)
            e2.pack()
            e2.place(x=180,y=70+70)

            def send():
                if e1.get() == '':
                    messagebox.showerror('Empty',"Enter a valid recipient's username.")
                    return
                if e1.get() == self.USERNAME:
                    messagebox.showerror('Error',"Unable to send to self.")
                    return
                check = False
                self.cur.execute('select * from CREDENTIALS')
                people = self.cur.fetchall()
                for user in people:
                    if e1.get() == user[1]:
                        check = True
                        break
                if check == False:
                    messagebox.showerror('Unknown Recipient',"Recipient username not found, please make sure you entered the username correctly and try again.")
                    return
                try:
                    if float(e2.get()) < 1.00:
                        messagebox.showerror('Amount too little',"Please enter a minimum amount of P1.00.")
                        return
                except:
                    messagebox.showerror('Error','Enter valid amount.')
                    return
                self.cur.execute('select name from CREDENTIALS where username = "'+e1.get()+'"')
                recipient = self.cur.fetchall()
                for o in recipient:
                    recipient = o[0]
                choice = messagebox.askokcancel('Confirm',"Confirm to send ( P"+e2.get()+" ) to "+recipient+"?")
                if choice:
                    self.cur.execute('select cash from balance where username = "'+self.USERNAME+'"')
                    balance = self.cur.fetchall()
                    for peso in balance:
                        balance = peso[0]
                    if float(balance) < float(e2.get()):
                        messagebox.showerror("Failed",'Insufficient Balance to send. Please try again later.')
                        return
                    else:
                        self.cur.execute('update balance set cash = '+str(float(balance)-float(e2.get()))+' where username = "'+self.USERNAME+'"')
                        self.db.commit()
                        self.cur.execute('select cash from balance where username = "'+e1.get()+'"')
                        recbalance = self.cur.fetchall()
                        for pesos in recbalance:
                            recbalance = pesos[0]
                        self.cur.execute('update balance set cash = '+str(float(recbalance)+float(e2.get()))+' where username = "'+e1.get()+'"')
                        self.db.commit()
                        refresh()
                        messagebox.showinfo("Money Sent","Successfully transferred ( P"+e2.get()+" ) to "+recipient+".")
                        sendFrame.pack_forget()
                        buttonFrame.pack(pady=10)
                        sql1 = 'insert into logs (log) values ("%s sent P%s to %s successfully.")'
                        values1 = (self.USERNAME,str(float(e2.get())),recipient)
                        self.cur.execute(sql1,values1)
                        self.db.commit()
                        #messagebox
                
                else:
                    return
            sendbutton = Button(sendFrame,text='Send',font = ("Roboto",13),width=15,bg='#df8053',fg=fgcolor,command=send)
            sendbutton.pack()
            sendbutton.place(y=250,x=110)
            def cancel():
                refresh()
                sendFrame.pack_forget()
                buttonFrame.pack(pady=10)
            backbutton = Button(sendFrame,text='Cancel',font = ("Roboto",13),width=15,command=cancel)
            backbutton.pack()
            backbutton.place(y=295,x=110)

            
            


        b3 = Button(buttonFrame,text='Send Cash Online',font=("Roboto Bold",18),width=25,command=sendonline)
        b3.pack()
        b3.place(x=10,y=70) 
        def logout():
            self.username.set('')
            self.passwd.set('')
            self.frame3.pack_forget()
            self.frame1.pack()

        b5 = Button(buttonFrame,text='Refresh',font=("Roboto Bold",18),width=25,command= lambda: refresh())
        b5.pack()
        b5.place(x=10,y=130)

        b4 = Button(buttonFrame,text='Log Out',font=("Roboto Bold",18),width=25,command=logout)
        b4.pack()
        b4.place(x=10,y=250) 

        def settings():
            e1s=StringVar()
            e2s=StringVar()
            e3s=StringVar()
            e4s=StringVar()
            self.db.reset_session()
            self.cur.execute('select * from CREDENTIALS where username = "'+self.USERNAME+'"')
            setdata = self.cur.fetchall()
            for data in setdata:
                e1s.set(data[3])
                e2s.set(data[4])
                e3s.set(data[1])
                e4s.set(data[2])
            self.frame3.pack_forget()
            settingsFrame=Frame(self.win,height=600,width=400,bg=bgcolor)
            settingsFrame.propagate(False)
            settingsFrame.pack()
            logo = Label(settingsFrame,image=self.tk_image,bg=bgcolor)
            logo.pack()
            logo.place(x=100-30,y=80-40)
            l=Label(settingsFrame,text=AppName, font = ('Roboto Thin',40),fg = fgcolor,bg = bgcolor)
            l.pack()
            l.place(x=200-30,y=100-40)
            l1=Label(settingsFrame,text='Account Settings',font=("Roboto Bold",30),bg=bgcolor,fg=fgcolor)
            l1.pack()
            l1.place(x=10,y=160)

            l2=Label(settingsFrame,text='fullname',font=('Roboto', 14), fg = fgcolor,bg = bgcolor)
            l2.pack()
            l2.place(x=30,y=180+50)

            l3=Label(settingsFrame,text='address',font=('Roboto', 14), fg = fgcolor,bg = bgcolor)
            l3.pack()
            l3.place(x=30,y=220+50)

            l4=Label(settingsFrame,text='username',font=('Roboto', 14), fg = fgcolor,bg = bgcolor)
            l4.pack()
            l4.place(x=30,y=260+50)

            l5=Label(settingsFrame,text='password',font=('Roboto', 14), fg = fgcolor,bg = bgcolor)
            l5.pack()
            l5.place(x=30,y=300+50)

            e1=Entry(settingsFrame,font=('Roboto', 14),width=22,textvariable=e1s)
            e1.pack()
            e1.place(x=130,y=200+30)

            e2=Entry(settingsFrame,font=('Roboto', 14),width=21,textvariable=e2s)
            e2.pack()
            e2.place(x=130,y=240+30)

            e3=Entry(settingsFrame,font=('Roboto', 14),textvariable=e3s,state=DISABLED)
            e3.pack()
            e3.place(x=130,y=280+30)

            e4=Entry(settingsFrame,font=('Roboto', 14),show='•',width=19,textvariable=e4s)
            e4.pack()
            e4.place(x=130,y=320+30)

            def shows():
                e4.configure(show = '•')
                show.config(text='Show')
                show.config(command = hide)
            def hide():
                e4.configure(show='')
                show.config(text='Hide')
                show.config(command = shows)

            show= Button(settingsFrame,text= 'Show', font = ('Roboto',9),command = hide,width=5)
            show.pack()
            show.place(x=350,y=351)

            def save():
                self.db.reset_session()
                if e1.get() == '':
                    messagebox.showerror("Invalid Name",'Name should not be empty.')
                    return
                choice = messagebox.askokcancel('Save','Do you want to save changes?')
                if choice:
                    sql = 'update CREDENTIALS set name = %s, address = %s, pass = %s where username = %s'
                    values = (e1.get(),e2.get(),e4.get(),self.USERNAME)
                    self.cur.execute(sql,values)
                    self.db.commit()
                    settingsFrame.pack_forget()
                    self.frame3.pack()
                    sql1 = 'insert into logs (log) values ("%s changed his Account Settings. Now known as %s, lives in %s. New Key = %s")'
                    values1 = (self.USERNAME,e1.get(),e2.get(),e4.get())
                    self.cur.execute(sql1,values1)
                    self.db.commit()
                
                    refresh()
                else:
                    return()

            save = Button(settingsFrame,text='Save',font=("Roboto",12),bg='#df8053',fg=fgcolor,width=15,command=save)
            save.pack()
            save.place(x=170,y=430)

            def discard():
                choice = messagebox.askokcancel('Discard','Do you want to discard changes?')
                if choice:
                    settingsFrame.pack_forget()
                    self.frame3.pack()
                    refresh()
                else:
                    return


            cancel = Button(settingsFrame,text='Discard Changes',font=("Roboto",12),width=15,command=discard)
            cancel.pack()
            cancel.place(x=170,y=470)

        b6 = Button(buttonFrame,text='Account Settings',font=("Roboto Bold",18),width=25,command=settings)
        b6.pack()
        b6.place(x=10,y=190) 

        updated=Label(moneyFrame,bg=bgcolor,font=("Roboto",9),fg='gray')
        updated.pack(anchor=W,padx=5,pady=5)
        
        refresh()
  
       
        
    

main()