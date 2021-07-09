import sqlite3
import hashlib
import bcrypt
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from tkinter import simpledialog
from functools import  partial
import os
import pickle
from cryptography.fernet import Fernet

# Database code
with sqlite3.connect("steele_trap.db") as db:
    cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS masterpassword(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS vault(
        id INTEGER PRIMARY KEY,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        user_id INTEGER NUT NULL
    );
""")

fa = None

# Create a salt
salt = bcrypt.gensalt()

class MainApp(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.title('Password Manager')
        self.geometry('710x600')

        self.menubar = UserMenu(self)
        self.config(menu=self.menubar)

        self._frame = None
        self.switch_frame(LoginScreen)

    def switch_frame(self, frame_class):
        global new_frame
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(anchor='center')

class UserMenu(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)

        fileMenu = Menu(self, tearoff=False, bg='white', fg='black', activeforeground='black',
                        activebackground='slateblue')
        self.add_cascade(label="Menu", underline=0, menu=fileMenu)
        fileMenu.add_command(label="Login", underline=1, command=lambda: parent.switch_frame(LoginScreen))
        fileMenu.add_command(label="Sign up", underline=1, command=lambda: parent.switch_frame(FirstScreen))
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", underline=1, command=lambda: parent.destroy())

class LoginScreen(Frame, Menu):
    def __init__(self, master):
        Frame.__init__(self, master)

        global fa
        fa = LoginScreen

        Style1 = ttk.Style()
        Style1.configure('TLabel')

        global user, passs
        user = StringVar()
        passs = StringVar()



        frame1 = Frame(self)
        frame1.grid(row=0, column=0)

        ttk.Label(frame1).grid(row=0, column=0, pady=(150, 5))
        ttk.Label(frame1, text='LOGIN', style='login.TLabel').grid(row=0, column=1, pady=(150, 5), padx=(8, 0))

        frame3 = Frame(self)
        frame3.grid(row=1, column=0)
        ttk.Label(frame3, text='USERNAME', style='TLabel').grid(row=1, column=0, pady=(50, 10))
        ttk.Label(frame3, text='PASSWORD ', style='TLabel').grid(row=2, column=0, )
        ttk.Entry(frame3, textvariable=user, width=20).grid(row=1, column=2, pady=(50, 10), padx=(20, 10))
        p = ttk.Entry(frame3, textvariable=passs, width=20)
        p.grid(row=2, column=2, padx=(12, 2))
        p.config(show='*')

        style = ttk.Style()
        style.configure('a.TButton', borderwidth=10)

        frame2 = Frame(self)
        frame2.grid(row=2, column=0, pady=20)
        ttk.Button(frame2, text='Sign Up', command=lambda: master.switch_frame(FirstScreen), style='a.TButton').pack(
            side=LEFT, padx=8)
        ttk.Button(frame2, text='Login', style='a.TButton', command=lambda : self.login_page(master)).pack(side=RIGHT, padx=8)

    def login_page(self, master):
        hash1 = hash_(passs.get())
        hash2 = cursor.execute('SELECT password FROM masterpassword WHERE username = ?', (user.get(),))
        row = str(hash2.fetchone()[0])
        if(hash1 == row):
            master.switch_frame(UserPage)
        else:
            msg.showerror('ERROR', "Wrong user or password")
            user.set('')
            passs.set('')


class FirstScreen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        global fa
        fa = FirstScreen

        global newUser, newPass
        newUser = StringVar()
        newPass = StringVar()

        frame1 = Frame(self)
        frame1.grid(row=0, column=0)

        ttk.Label(frame1.grid(row=0, column=0, pady=(150, 5)))
        ttk.Label(frame1, text='SIGN UP', style='login.TLabel').grid(row=0, column=1, pady=(150, 5), padx=(8, 0))

        frame3 = Frame(self)
        frame3.grid(row=1, column=0)
        ttk.Label(frame3, text='NEW USERNAME', style='TLabel').grid(row=1, column=0, pady=(50, 10))
        ttk.Label(frame3, text='NEW PASSWORD ', style='TLabel').grid(row=2, column=0, )
        ttk.Entry(frame3, textvariable=newUser, width=20).grid(row=1, column=2, pady=(50, 10), padx=(20, 10))
        p = ttk.Entry(frame3, textvariable=newPass, width=20)
        p.grid(row=2, column=2, padx=(12, 2))
        p.config(show="*")

        frame2 = Frame(self)
        frame2.grid(row=2, column=0, pady=20)
        ttk.Button(frame2, text='Sign Up', command=lambda: self.sign_up(master), style='TButton').grid(row=0, column=0)
        ttk.Button(frame2, text='Back', command=lambda: master.switch_frame(LoginScreen), style='TButton').grid(row=0, column=1, padx=20)

    def sign_up(self, master):
        checkName = cursor.execute("""SELECT username FROM masterpassword WHERE username = ?""", (newUser.get(),))
        row = checkName.fetchone()
        if row:
            msg.showerror("ERROR","You must pick a different user name")
            master.switch_frame(FirstScreen)
        else:
            genwrite_key(newUser.get())
            a = encrypt_(newUser.get(), newUser.get())

            hashedPassword = hash_(newPass.get())
            insertUser = """INSERT INTO masterpassword(username, password) VALUES (?, ?)"""
            data = (newUser.get(), hashedPassword)
            cursor.execute(insertUser, data)
            db.commit()

            master.switch_frame(LoginScreen)

class UserPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        global fa
        fa = UserPage

        Style2 = ttk.Style()
        Style2.configure('title.TLabel', font='Helvetica 24 bold')

        style = ttk.Style()
        style.configure('TButton', background='slateblue', borderwidth=10)

        frame = Frame(self)
        frame.pack(pady=(50, 0))
        title_label = ttk.Label(frame, text='STEELE TRAP PASSWORD MANAGER', style='title.TLabel')
        title_label.grid(row=0, column=1)

        but_frame = Frame(self)
        but_frame.pack()

        def Run(n):
            pass

        but1 = ttk.Button(but_frame, text="Add New Account", command=lambda: master.switch_frame(AddUserAccount))
        but2 = ttk.Button(but_frame, text="Remove an Account")
        but3 = ttk.Button(but_frame, text="List Saved Accounts", command=lambda : master.switch_frame(ShowList))
        but4 = ttk.Button(but_frame, text="Edit Accounts")
        but5 = ttk.Button(but_frame, text="Exit")

        but1.grid(row=1, column=0, pady=(50, 40), padx=(0, 40))
        but2.grid(row=1, column=2, pady=(50, 40), padx=(40, 0))
        but3.grid(row=2, column=0, pady=(40, 0), padx=(0, 40))
        but4.grid(row=2, column=2, pady=(40, 0), padx=(40, 0))
        but5.grid(row=3, column=1, pady=(40, 0), padx=(40,0))

class AddUserAccount(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        global fa
        fa = AddUserAccount

        Style3 = ttk.Style()
        Style3.configure('title2.TLabel', font='Helvetica 24 bold')

        title_frame = Frame(self)
        title_frame.grid(row=0, column=0)
        add = ttk.Label(title_frame, text='ADD', style='title2.TLabel')
        add.grid(row=0, column=1, pady=30)

        self.type = StringVar()
        self.email = StringVar()
        self.phone_num = StringVar()
        self.username = StringVar()
        self.password = StringVar()

        self.type.set('')
        self.email.set('')
        self.phone_num.set('')
        self.username.set('')
        self.password.set('')

        Label_Frame = Frame(self)
        Label_Frame.grid(row=1, column=0, padx=(0, 200))

        Style1 = ttk.Style()
        Style1.configure('TLabel', font='Helvetica 11 bold')
        i = 1

        type_label = ttk.Label(Label_Frame, text=f'{i}] Type:', style="TLabel")
        type_label.grid(row=0, column=0, padx=10, pady=20)
        type_Entry = ttk.Entry(Label_Frame, textvariable=self.type, width=30)
        type_Entry.grid(row=0, column=1, padx=10, pady=10)
        i += 1

        username_label = ttk.Label(Label_Frame, text=f'{i}] Username:', style="TLabel")
        username_label.grid(row=3, column=0, padx=10, pady=20)
        username_Entry = ttk.Entry(Label_Frame, textvariable=self.username, width=30)
        username_Entry.grid(row=3, column=1, padx=10, pady=10)
        i += 1

        password_label = ttk.Label(Label_Frame, text=f'{i}] Password:', style="TLabel")
        password_label.grid(row=4, column=0, padx=10, pady=20)
        password_Entry = ttk.Entry(Label_Frame, textvariable=self.password, width=30)
        password_Entry.grid(row=4, column=1, padx=10, pady=10)
        i += 1
        password_Entry.config(show='*')

        but_frame = Frame(self)
        but_frame.grid(row=2, column=0, pady=20)

        style = ttk.Style()
        style.configure('TButton', borderwidth=0)

        def clear(self):
            self.type.set('')
            self.username.set('')
            self.password.set('')

        def back(master):
            choics = msg.askquestion('Confirm', 'Do you really want to Go Back')
            if choics == 'yes':
                master.switch_frame(UserPage)
            else:
                pass

        def add(self, master):
            if self.type.get() == '' or self.password.get() == '':
                msg.showerror('Wrong Input', 'Please Add Password or its Type')
            else:
                if self.phone_num.get() == '':
                    self.phone_num.set('---')
                    if self.email.get() == '':
                        self.email.set('---')

                    if self.username.get() == '':
                        self.username.set('---')

                    self.dic = {}
                    list_ = [encrypt_(self.username.get(), user.get()),
                             encrypt_(self.password.get(), user.get())]

                    get_ID = cursor.execute("""SELECT id FROM masterpassword WHERE username = ?""", (user.get(),))
                    row = int(get_ID.fetchone()[0])


                    insertAccount = """INSERT INTO vault(website, username, password, user_id) VALUES (?, ?, ?, ?)"""

                    data = (self.type.get(), list_[0], list_[1], row)

                    cursor.execute(insertAccount, data)
                    db.commit()

                    master.switch_frame(UserPage)


        save_but = ttk.Button(but_frame, text='Save', style='TButton', command=lambda: add(self, master)).grid(row=0,
                                                                                                               column=0,
                                                                                                               padx=10)
        clear_but = ttk.Button(but_frame, text='All Clear', style='TButton', command=lambda: clear(self)).grid(row=0,
                                                                                                               column=1,
                                                                                                               padx=10)
        back_but = ttk.Button(but_frame, text='Back', style='TButton', command=lambda: back(master)).grid(row=0,
                                                                                                          column=2,
                                                                                                          padx=10)


class ShowList(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self)
        root = self
        self.key = []
        self.value = []

        global fa
        fa = ShowList

        Style3 = ttk.Style()
        Style3.configure('title2.TLabel', font='Helvetica 30 bold')

        title_frame = Frame(root)
        title_frame.grid(row=0, column=0)

        title_img = ttk.Label(title_frame)
        title_img.grid(row=0, column=0, padx=10)
        title_label = ttk.Label(title_frame, text='VIEW', style='title2.TLabel')
        title_label.grid(row=0, column=1, pady=30)

        root_frame = Frame(root)
        root_frame.grid(row=1, column=0)

        Scrollbar2 = ttk.Scrollbar(root_frame)
        # Scrollbar1 = ttk.Scrollbar(root_frame,orient='horizontal')
        canvas = Canvas(root_frame, yscrollcommand=Scrollbar2.set, width=660, height=400)
        canvas.pack(side=LEFT, anchor='nw', fill=BOTH, padx=(10, 0), pady=10)

        # Scrollbar1.pack(side=BOTTOM, fill=X)
        Scrollbar2.pack(side=LEFT, fill=Y, pady=10)
        # Scrollbar1.config(command=canvas.xview)
        Scrollbar2.config(command=canvas.yview)

        main_frame = Frame(canvas)
        main_frame.config(padx=10)
        main_frame2 = Frame(canvas)
        main_frame2.config(padx=10)
        canvas.create_window(0, 0, window=main_frame, anchor='nw')

        get_ID = cursor.execute("""SELECT id FROM masterpassword WHERE username = ?""", (user.get(),))
        row = int(get_ID.fetchone()[0])

        get_Info = cursor.execute("""SELECT * FROM vault WHERE user_id = ?""", (row,))
        print(get_Info.fetchall())


# ------------------------------------------------------------------GLOBAL FUNCTIONS-----------------------------------------------------------

def hash_(input):
    hash = hashlib.sha256(str.encode(input)).hexdigest()

    return hash

def genwrite_key(username):
    key = Fernet.generate_key()
    with open(f"data/key/{username}.key", "wb") as key_file:
        key_file.write(key)

def encrypt_(msg, username):
    key = call_key(username)
    slogan = msg.encode()
    a = Fernet(key)
    coded_slogan = a.encrypt(slogan)
    return coded_slogan

def call_key(user):
    return open(f"data/key/{user}.key", "rb").read()

def decrypt_(msg, user):
    key = call_key(user)
    b = Fernet(key)
    decoded_slogan = b.decrypt(msg)
    decoded_slogan = decoded_slogan.decode('utf-8')
    return decoded_slogan

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
