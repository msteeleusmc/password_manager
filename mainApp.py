# -------------------------------------------------------------------------------------------------------------------------------
#                                           CSCE 3550 PASSWORD MANAGER PROJECT 1
#                                                  Name : Michael Steele
#                                                  Student ID : 11198872
#                                              Email : MichaelSteele@my.unt.edu
# -------------------------------------------------------------------------------------------------------------------------------

from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from cryptography.fernet import Fernet
import os, pickle
import hashlib
import os.path
from os import path

# -------------------------------------------------------------------------------------------------------------------------------
#                                           Global variable used for each GUI page
# -------------------------------------------------------------------------------------------------------------------------------

global_variable = None

# -------------------------------------------------------------------------------------------------------------------------------
#                                           Main App Class to set the foundation
# -------------------------------------------------------------------------------------------------------------------------------
class MainApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        global theme
        if os.path.isfile('data/mainApp_data/_data.p'):
            f1 = open('data/mainApp_data/_data.p', 'rb')
            theme = pickle.load(f1)
            f1.close()

        self.title('CSCE_3550 Password Manager')
        self.geometry('710x600')

        global user, act_pass
        user = StringVar()
        act_pass = StringVar()
        user.set('a')

        menubar = AppFileMenu(self)
        self.config(menu=menubar)

        self._frame = None
        self.switch_frame(AppLoginPage)

    def switch_frame(self, frame_class):
        global new_frame
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(anchor='center')

# -------------------------------------------------------------------------------------------------------------------------------
#                                           Menu Class used for the file menu
# -------------------------------------------------------------------------------------------------------------------------------
class AppFileMenu(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)
        global theme

        fileMenu = Menu(self, tearoff=False, background='white', fg='black', activeforeground='black')
        self.add_cascade(label="User Options", underline=0, menu=fileMenu)
        fileMenu.add_command(label="Login", underline=1, command=lambda: parent.switch_frame(AppLoginPage))
        fileMenu.add_command(label="Sign up", underline=1, command=lambda: parent.switch_frame(AppSignUpPage))
        fileMenu.add_command(label="Delete Account", underline=1, command=lambda: parent.switch_frame(DeleteUserAcount))
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", underline=1, command=lambda: parent.destroy())


# -------------------------------------------------------------------------------------------------------------------------------
#                                               Login Page Class
# -------------------------------------------------------------------------------------------------------------------------------
class AppLoginPage(Frame, Menu):

    def __init__(self, master):
        Frame.__init__(self, master)

        global global_variable
        global_variable = AppLoginPage

        Style1 = ttk.Style()
        Style1.configure('TLabel')

        global user, act_pass
        user = StringVar()
        act_pass = StringVar()

        frame1 = Frame(self)
        frame1.grid(row=0, column=0)

        ttk.Label(frame1,).grid(row=0, column=0, pady=(0, 5))
        ttk.Label(frame1, text='LOGIN', style='login.TLabel', font='Times 30 bold').grid(row=0, column=1, pady=(150, 5), padx=(8, 0))

        frame3 = Frame(self)
        frame3.grid(row=1, column=0)
        ttk.Label(frame3, text='USERNAME', style='TLabel').grid(row=1, column=0, pady=(50, 10))
        ttk.Label(frame3, text='PASSWORD ', style='TLabel').grid(row=2, column=0, )
        ttk.Entry(frame3, textvariable=user, width=20).grid(row=1, column=2, pady=(50, 10), padx=(20, 10))
        p = ttk.Entry(frame3, textvariable=act_pass, width=20)
        p.grid(row=2, column=2, padx=(12, 2))
        p.config(show='*')
        self.x = 1

        def showHiddenPassword(input):
            global x
            if input == 1:
                p.config(show='')
                self.x = input + 1

            elif input == 2:
                p.config(show='*')
                self.x = input - 1

        b = Button(frame3, text='Show Password', command=lambda: showHiddenPassword(self.x), width=0, bd=0)
        b.grid(row=2, column=3)

        style = ttk.Style()
        style.configure('a.TButton', borderwidth=10)

        frame2 = Frame(self)
        frame2.grid(row=2, column=0, pady=20)
        ttk.Button(frame2, text='Sign Up', command=lambda: master.switch_frame(AppSignUpPage), style='a.TButton').pack(side=LEFT, padx=8)
        ttk.Button(frame2, text='Login', command=lambda: self.enter(master), style='a.TButton').pack(side=RIGHT, padx=8)

    def enter(self, master):
        if os.path.isfile(f'data/user_data/{user.get()}_pass_file.p'):
            with open(f'data/user_data/{user.get()}_pass_file.p', 'rb') as f:
                listt = pickle.load(f)
            a = decrypt_(listt[0], user.get())
            # Here is where the password is checked against the saved hash
            b = check_hash_(act_pass.get(), listt[1])
            if user.get() == a and b:
                master.switch_frame(AppUserVault)
            else:
                msg.showerror('Wrong', "Wrong user or password")
                user.set('')
                act_pass.set('')
        else:
            msg.showerror('Wrong', "Wrong user or password")
            user.set('')
            act_pass.set('')

# -------------------------------------------------------------------------------------------------------------------------------
#                                           Create User Account Class
# -------------------------------------------------------------------------------------------------------------------------------
class AppSignUpPage(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self)
        global global_variable
        global_variable = AppSignUpPage

        global newuser, newact_pass
        newuser = StringVar()
        newact_pass = StringVar()

        frame1 = Frame(self)
        frame1.grid(row=0, column=0)
        style = ttk.Style()
        style.configure('TButton', borderwidth=10)

        Style1 = ttk.Style()
        Style1.configure('TLabel')


        ttk.Label(frame1).grid(row=0, column=0, pady=(150, 5))
        ttk.Label(frame1, text='Create User Account', style='login.TLabel', font='Times 30 bold').grid(row=0, column=1, pady=(150, 5), padx=(8, 0))

        frame3 = Frame(self)
        frame3.grid(row=1, column=0)
        ttk.Label(frame3, text='NEW USERNAME', style='TLabel').grid(row=1, column=0, pady=(50, 10))
        ttk.Label(frame3, text='NEW PASSWORD ', style='TLabel').grid(row=2, column=0, )
        ttk.Entry(frame3, textvariable=newuser, width=20).grid(row=1, column=2, pady=(50, 10), padx=(20, 10))
        p = ttk.Entry(frame3, textvariable=newact_pass, width=20)
        p.grid(row=2, column=2, padx=(20, 10))
        p.config(show="*")
        self.x = 1

        def showHiddenPassword(input):
            if input == 1:
                p.config(show='')
                self.x = input + 1

            elif input == 2:
                p.config(show='*')
                self.x = input - 1

        b = Button(frame3, text='Show Password', command=lambda: showHiddenPassword(self.x), bd=0)
        b.grid(row=2, column=3)

        frame2 = Frame(self)
        frame2.grid(row=2, column=0, pady=20)
        ttk.Button(frame2, text='Sign Up', command=lambda: self.sign_up(master), style='TButton').grid(row=0, column=0)
        ttk.Button(frame2, text='Back', command=lambda: master.switch_frame(AppLoginPage), style='TButton').grid(row=0, column=1, padx=20)

    def sign_up(self, master):
        if newuser.get() == '' or len(newact_pass.get()) < 8:
            msg.showerror('Invalid Input',
                          'Please Enter Valid Username or Password.\n'
                          'Ensure password is 8 characters or more')
        else:
            if (path.exists(f'data/user_data/{newuser.get()}_pass_file.p')):
                msg.showerror('Invalid Input',
                              'Please choose a different user name.\n'
                              'Ensure password is 8 characters or more')
            else:
                genwrite_key(newuser.get())

                a = encrypt_(newuser.get(), newuser.get())
                #Here is were the sign up password is hashed and saved into the file
                b = hash_(newact_pass.get())

                with open(f'data/user_data/{newuser.get()}_pass_file.p', 'wb') as f:
                    pickle.dump([a, b], f)

                msg.showinfo('Account Added Successfully', 'Your Account has been Added\nPlease Login you account to access')
                master.switch_frame(AppLoginPage)

# -------------------------------------------------------------------------------------------------------------------------------
#                                        Displays User Interface after Login
# -------------------------------------------------------------------------------------------------------------------------------
class AppUserVault(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self)

        global global_variable
        global_variable = AppUserVault

        Style2 = ttk.Style()
        Style2.configure('title.TLabel', font='Times 30 bold')

        style = ttk.Style()
        style.configure('TButton', borderwidth=10)

        frame = Frame(self)
        frame.pack(pady=(50, 0))


        title_label = ttk.Label(frame, text='MY VAULT', style='title.TLabel')
        title_label.grid(row=0, column=1)

        but_frame = Frame(self)
        but_frame.pack()


        def Run(n):
            if os.path.isfile(f'data/password_data/{user.get()}_pass.p'):
                if n == 1:
                    master.switch_frame(Show_Pass)
                elif n == 2:
                    master.switch_frame(Delete_Pass)
                elif n == 3:
                    master.switch_frame(Change_Pass)
            else:
                msg.showwarning('Nothing to show', 'You haven\'t save any thing')

        but1 = ttk.Button(but_frame, text='Add Account to Vault', command=lambda: master.switch_frame(Add_Pass))
        but2 = ttk.Button(but_frame, text='Remove Account from Vault', command=lambda: Run(2))
        but3 = ttk.Button(but_frame, text='Edit an Account in Vault', command=lambda: Run(3))
        but4 = ttk.Button(but_frame, text='Show My Accounts', command=lambda: Run(1))
        but5 = ttk.Button(but_frame, text='Exit', command = lambda: master.switch_frame(AppLoginPage))

        but1.grid(row=1, column=0, pady=(50, 40), padx=(0, 40))
        but2.grid(row=1, column=2, pady=(50, 40), padx=(40, 0))
        but3.grid(row=2, column=0, pady=(40, 0), padx=(0, 40))
        but4.grid(row=2, column=2, pady=(40, 0), padx=(40, 0))
        but5.grid(row=5, column=1, pady=(50, 40), padx=(40, 40))


# -------------------------------------------------------------------------------------------------------------------------------
#                                           Display stored account data
# -------------------------------------------------------------------------------------------------------------------------------
class Show_Pass(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self)
        root = self
        self.key = []
        self.value = []

        global global_variable
        global_variable = Show_Pass

        Style3 = ttk.Style()
        Style3.configure('title2.TLabel', font='Times 30 bold')

        title_frame = Frame(root)
        title_frame.grid(row=0, column=0)

        title_label = ttk.Label(title_frame, text='VIEW', style='title2.TLabel')
        title_label.grid(row=0, column=1, pady=30)

        root_frame = Frame(root)
        root_frame.grid(row=1, column=0)

        Scrollbar2 = ttk.Scrollbar(root_frame)
        canvas = Canvas(root_frame, yscrollcommand=Scrollbar2.set, width=660, height=400)
        canvas.pack(side=LEFT, anchor='nw', fill=BOTH, padx=(10, 0), pady=10)

        Scrollbar2.pack(side=LEFT, fill=Y, pady=10)
        Scrollbar2.config(command=canvas.yview)

        main_frame = Frame(canvas)
        main_frame.config(padx=10)
        main_frame2 = Frame(canvas)
        main_frame2.config(padx=10)
        canvas.create_window(0, 0, window=main_frame, anchor='nw')
        with open(f'data/password_data/{user.get()}_pass.p', 'rb') as f:
            self.dic = pickle.load(f)

        for k, v in self.dic.items():
            self.key.append(k)
            self.value.append(v)

        style = ttk.Style()
        style.configure('TLabel', font='Helvetica 10 ')
        style1 = ttk.Style()
        style1.configure('title.TLabel', font='Helvetica 11 bold')

        ttk.Label(main_frame, text=f'URL/ACCOUNT', style='title.TLabel').grid(row=0, column=2, padx=(0, 50), pady=(0, 15))
        ttk.Label(main_frame, text=f'USERNAME', style='title.TLabel').grid(row=0, column=4, padx=(10, 44), pady=(0, 15))
        ttk.Label(main_frame, text=f'PASSWORD', style='title.TLabel').grid(row=0, column=5, padx=(20, 0), pady=(0, 15))

        for i in range(0, len(self.dic)):
            ttk.Label(main_frame, text=f'{i + 1}]').grid(row=i + 1, column=1, pady=(15, 0))
            ttk.Label(main_frame, text=f'{decrypt_(self.key[i], user.get())}',
                        style='TLabel').grid(row=i + 1, column=2, padx=(10, 40),pady=(15, 0))
            ttk.Label(main_frame, text=f'{decrypt_(self.value[i][0], user.get())}',
                      style='TLabel').grid(row=i + 1, column=4, padx=(0, 30), pady=(15, 0))
            ttk.Label(main_frame, text=f'{decrypt_(self.value[i][1], user.get())}',
                      style='TLabel').grid(row=i + 1, column=5, padx=(0, 30), pady=(15, 0))

        def back(master):
            master.switch_frame(AppUserVault)

        style = ttk.Style()
        style.configure('TButton', borderwidth=5)

        ttk.Button(root, text='Back', command=lambda: back(master), style='TButton').grid(row=2, column=0)

        root.update()
        canvas.config(scrollregion=canvas.bbox("all"))


# -------------------------------------------------------------------------------------------------------------------------------
#                                           Delete stored account data
# -------------------------------------------------------------------------------------------------------------------------------
class Delete_Pass(Show_Pass):
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self)
        root = self
        key = []
        value = []

        global global_variable
        global_variable = Delete_Pass

        Style3 = ttk.Style()
        Style3.configure('title2.TLabel', font='Times 30 bold')


        title_frame = Frame(root)
        title_frame.grid(row=0, column=0)

        title_label = ttk.Label(title_frame, text='DELETE', style='title2.TLabel')
        title_label.grid(row=0, column=1, pady=30)

        root_frame = Frame(root)
        root_frame.grid(row=1, column=0)

        Scrollbar2 = ttk.Scrollbar(root_frame)
        canvas = Canvas(root_frame, yscrollcommand=Scrollbar2.set, width=660, height=400)
        canvas.pack(side=LEFT, anchor='nw', fill=Y, padx=(10, 0), pady=10)

        Scrollbar2.pack(side=LEFT, fill=Y, pady=10)
        Scrollbar2.config(command=canvas.yview)

        main_frame = Frame(canvas)
        main_frame.config(padx=10)
        main_frame2 = Frame(canvas)
        main_frame2.config(padx=10)
        canvas.create_window(0, 0, window=main_frame, anchor='nw')
        with open(f'data/password_data/{user.get()}_pass.p', 'rb') as f:
            self.dic = pickle.load(f)

        for k, v in self.dic.items():
            key.append(k)
            value.append(v)

        style = ttk.Style()
        style.configure('TLabel', font='Times 10')
        style1 = ttk.Style()
        style1.configure('title.TLabel', font='Times 11 bold')

        ttk.Label(main_frame, text=f'TYPE', style='title.TLabel').grid(row=0, column=1, padx=(0, 50), pady=(0, 15))
        ttk.Label(main_frame, text=f'USERNAME', style='title.TLabel').grid(row=0, column=4, padx=(10, 44), pady=(0, 15))
        ttk.Label(main_frame, text=f'PASSWORD', style='title.TLabel').grid(row=0, column=5, padx=(0, 0), pady=(0, 15))

        for i in range(0, len(self.dic)):
            ttk.Label(main_frame, text=f'{decrypt_(key[i], user.get())}', style='TLabel').grid(row=i + 1, column=1, padx=(0, 40), pady=(15, 0))
            ttk.Label(main_frame, text=f'{decrypt_(value[i][0], user.get())}',
                      style='TLabel').grid(row=i + 1, column=4,padx=(0, 30), pady=(15, 0))
            ttk.Label(main_frame, text=f'{decrypt_(value[i][1], user.get())}',
                      style='TLabel').grid(row=i + 1, column=5, padx=(0, 0), pady=(15, 0))

        Checkbutton_style = ttk.Style()
        Checkbutton_style.configure('checkbutton.TCheckbutton')
        for i in range(0, len(self.dic)):
            globals()['checkbutton%s' % i] = IntVar()
            ttk.Checkbutton(main_frame, style='checkbutton.TCheckbutton', variable=globals()['checkbutton%s' % i],
                            onvalue=i + 1, offvalue=0).grid(row=i + 1, column=0, padx=10, pady=(15, 0))
        but_frame = Frame(root)
        but_frame.grid(row=2, column=0)

        def back(master):
            master.switch_frame(AppUserVault)

        def delete(self, master):
            self.delete_list = []
            choics = msg.askquestion('Confirm', 'Do you really want to delete')
            if choics == 'yes':
                for i in range(0, len(self.dic)):
                    if globals()['checkbutton%s' % i].get() > 0:
                        self.delete_list.append(key[i])
                for i in self.delete_list:
                    self.dic.pop(i)
                with open(f'data/password_data/{user.get()}_pass.p', 'wb') as f:
                    pickle.dump(self.dic, f)
                msg.showinfo('Deleted Sucessfully', 'Selected  Passwords has been Deleted')
            else:
                pass
            master.switch_frame(AppUserVault)

        style = ttk.Style()
        style.configure('TButton',  borderwidth=0)

        b1 = ttk.Button(but_frame, text='Delete', command=lambda: delete(self, master), style='TButton')
        b1.grid(row=0, column=0, padx=(0, 100))
        b2 = ttk.Button(but_frame, text='Back', command=lambda: back(master), style='TButton')
        b2.grid(row=0, column=1, padx=(100, 0))

        root.update()
        canvas.config(scrollregion=canvas.bbox("all"))


# -------------------------------------------------------------------------------------------------------------------------------
#                                           Add an account to the vault
# -------------------------------------------------------------------------------------------------------------------------------
class Add_Pass(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self)

        global global_variable
        global_variable = Add_Pass

        Style3 = ttk.Style()
        Style3.configure('title2.TLabel', font='Times 30 bold')

        title_frame = Frame(self)
        title_frame.grid(row=0, column=0)

        add = ttk.Label(title_frame, text='ADD', style='title2.TLabel')
        add.grid(row=0, column=1, pady=30)

        self.type = StringVar()
        self.username = StringVar()
        self.password = StringVar()

        self.type.set('')
        self.username.set('')
        self.password.set('')

        Label_Frame = Frame(self)
        Label_Frame.grid(row=1, column=0, padx=(0, 200))

        Style1 = ttk.Style()
        Style1.configure('TLabel', font='Times 11 bold')
        i = 1

        type_label = ttk.Label(Label_Frame, text=f'{i}] URL/Account:', style="TLabel")
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

        self.x = 1

        def showHiddenPassword(a):
            if a == 1:
                password_Entry.config(show='')
                self.x = a + 1

            elif a == 2:
                password_Entry.config(show='*')
                self.x = a - 1


        b = Button(Label_Frame, text='Show', command=lambda: showHiddenPassword(self.x), bd=0)
        b.grid(row=4, column=2)

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
                master.switch_frame(AppUserVault)
            else:
                pass

        def add(self, master):
            if self.type.get() == '' or self.password.get() == '':
                msg.showerror('Wrong Input', 'Please Add Password or its Type')
            else:
                self.dic = {}
                list_ = [encrypt_(self.username.get(), user.get()),
                         encrypt_(self.password.get(), user.get())]

                if os.path.isfile(f'data/password_data/{user.get()}_pass.p'):
                    with open(f'data/password_data/{user.get()}_pass.p', 'rb') as f:
                        self.dic = pickle.load(f)
                self.dic[encrypt_(self.type.get(), user.get())] = list_
                with open(f'data/password_data/{user.get()}_pass.p', 'wb') as f:
                    pickle.dump(self.dic, f)
                msg.showinfo('Add Sucessfull', 'Your Password data has been added')
                master.switch_frame(AppUserVault)


        ttk.Button(but_frame, text='Save', style='TButton', command=lambda: add(self, master)).grid(row=0, column=0, padx=10)
        ttk.Button(but_frame, text='All Clear', style='TButton', command=lambda: clear(self)).grid(row=0,column=1, padx=10)
        ttk.Button(but_frame, text='Back', style='TButton', command=lambda: back(master)).grid(row=0, column=2, padx=10)


# -------------------------------------------------------------------------------------------------------------------------------
#                                           Edit saved account information in vault
# -------------------------------------------------------------------------------------------------------------------------------
class Change_Pass(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self)
        root = self
        self.key = []
        self.value = []

        global global_variable
        global_variable = Change_Pass

        Style3 = ttk.Style()
        Style3.configure('title2.TLabel', font='Times 30 bold')

        title_frame = Frame(root)
        title_frame.grid(row=0, column=0)

        title_label = ttk.Label(title_frame, text='CHANGE', style='title2.TLabel')
        title_label.grid(row=0, column=1, pady=30)

        root_frame = Frame(root)
        root_frame.grid(row=1, column=0)

        Scrollbar2 = ttk.Scrollbar(root_frame)

        canvas = Canvas(root_frame, yscrollcommand=Scrollbar2.set, width=660, height=400)
        canvas.pack(side=LEFT, anchor='nw', fill=BOTH, padx=(10, 0), pady=10)

        Scrollbar2.pack(side=LEFT, fill=Y, pady=10)
        Scrollbar2.config(command=canvas.yview)

        main_frame = Frame(canvas)
        main_frame.config(padx=10)
        main_frame2 = Frame(canvas)
        main_frame2.config(padx=10)
        canvas.create_window(0, 0, window=main_frame, anchor='nw')
        with open(f'data/password_data/{user.get()}_pass.p', 'rb') as f:
            self.dic = pickle.load(f)

        for k, v in self.dic.items():
            self.key.append(k)
            self.value.append(v)

        style = ttk.Style()
        style.configure('TLabel', font='Times 10 ')
        style1 = ttk.Style()
        style1.configure('title.TLabel', font='Times 11 bold')

        ttk.Label(main_frame, text=f'TYPE', style='title.TLabel').grid(row=0, column=2, padx=(0, 50), pady=(10, 15))
        ttk.Label(main_frame, text=f'USERNAME', style='title.TLabel').grid(row=0, column=4, padx=(10, 44), pady=(0, 15))
        ttk.Label(main_frame, text=f'PASSWORD', style='title.TLabel').grid(row=0, column=5, padx=(0, 0), pady=(0, 15))

        for i in range(0, len(self.dic)):
            ttk.Label(main_frame, text=f' {decrypt_(self.key[i], user.get())}', style='TLabel').grid(row=i + 1, column=2, padx=(10, 40), pady=(15, 0))
            ttk.Label(main_frame, text=f'{decrypt_(self.value[i][0], user.get())}',
                      style='TLabel').grid(row=i + 1, column=4, padx=(0, 30), pady=(15, 0))
            ttk.Label(main_frame, text=f'{decrypt_(self.value[i][1], user.get())}',
                      style='TLabel').grid(row=i + 1, column=5, padx=(0, 30), pady=(15, 0))

        Checkbutton_style = ttk.Style()
        Checkbutton_style.configure('checkbutton.TCheckbutton')
        global change_item
        change_item = IntVar()
        for i in range(0, len(self.dic)):
            ttk.Checkbutton(main_frame, style='checkbutton.TCheckbutton', variable=change_item, onvalue=i, offvalue=0).grid(row=i + 1, column=0, padx=10, pady=(15, 0))

        def back(master):
            master.switch_frame(AppUserVault)

        def change():
            for k, v in self.dic.items():
                if k == self.key[change_item.get()]:
                    global c
                    c = change_item.get()
                    master.switch_frame(Change_pass_label)

        but_frame = Frame(root)
        but_frame.grid(row=2, column=0)

        style = ttk.Style()
        style.configure('TButton', borderwidth=5)

        def back(master):
            master.switch_frame(AppUserVault)

        ttk.Button(but_frame, text='Change', command=lambda: change(), style='TButton').grid(row=0, column=0)
        ttk.Button(but_frame, text='Back', command=lambda: back(master), style='TButton').grid(row=0, column=1, padx=(10, 0))

        root.update()
        canvas.config(scrollregion=canvas.bbox("all"))

# -------------------------------------------------------------------------------------------------------------------------------
#                                           Works with editing the stored data
# -------------------------------------------------------------------------------------------------------------------------------
class Change_pass_label(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self)
        self.key = []
        self.value = []

        global global_variable
        global_variable = Change_pass_label

        with open(f'data/password_data/{user.get()}_pass.p', 'rb') as f:
            self.dic = pickle.load(f)

        for k, v in self.dic.items():
            self.key.append(k)
            self.value.append(v)

        Style3 = ttk.Style()
        Style3.configure('title2.TLabel', font='Times 30 bold')

        title_frame = Frame(self)
        title_frame.grid(row=0, column=0)
        add = ttk.Label(title_frame, text='CHANGE', style='title2.TLabel')
        add.grid(row=0, column=1, pady=30)

        self.type = StringVar()
        self.username = StringVar()
        self.password = StringVar()

        self.type.set(decrypt_(self.key[c], user.get()))
        self.username.set(decrypt_(self.value[c][0], user.get()))
        self.password.set(decrypt_(self.value[c][1], user.get()))

        Label_Frame = Frame(self)
        Label_Frame.grid(row=1, column=0, padx=(0, 200))

        Style1 = ttk.Style()
        Style1.configure('TLabel', font='Times 11 bold')
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

        self.x = 1

        def showHiddenPassword(input):
            if input == 1:
                password_Entry.config(show='')
                self.x = input + 1

            elif input == 2:
                password_Entry.config(show='*')
                self.x = input - 1

        b = Button(Label_Frame, text='Show', command=lambda: showHiddenPassword(self.x), bd=0)
        b.grid(row=4, column=2)

        def change():

            if self.type.get() == '' or self.password.get() == '':
                msg.showerror('', 'Please Add Password or its Type')

            if self.username.get() == '':
                self.username.set('---')

            list_ = [encrypt_(self.username.get(), user.get()),
                     encrypt_(self.password.get(), user.get())]
            if os.path.isfile(f'data/password_data/{user.get()}_pass.p'):
                with open(f'data/password_data/{user.get()}_pass.p', 'rb') as f:
                    self.dic = pickle.load(f)
            self.dic.pop(self.key[c])

            self.dic[encrypt_(self.type.get(), user.get())] = list_
            with open(f'data/password_data/{user.get()}_pass.p', 'wb') as f:
                pickle.dump(self.dic, f)

            msg.showinfo('Add Sucessfull', 'Your Password data has been added')
            master.switch_frame(AppUserVault)

        def back(master):
            master.switch_frame(Change_Pass)

        def clear(self):
            self.type.set('')
            self.username.set('')
            self.password.set('')

        but_frame = Frame(self)
        but_frame.grid(row=2, column=0, pady=20)

        style = ttk.Style()
        style.configure('TButton', borderwidth=0)

        ttk.Button(but_frame, text='Save Change', style='TButton', command=lambda: change()).grid(row=0, column=0, padx=10)
        ttk.Button(but_frame, text='All Clear', style='TButton', command=lambda: clear(self)).grid(row=0, column=1, padx=10)
        ttk.Button(but_frame, text='Back', style='TButton', command=lambda: back(master)).grid(row=0, column=2, padx=10)

# -------------------------------------------------------------------------------------------------------------------------------
#                                           Permanetly delete a users account
# -------------------------------------------------------------------------------------------------------------------------------
class DeleteUserAcount(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self)

        global global_variable
        global_variable = DeleteUserAcount

        Style1 = ttk.Style()
        Style1.configure('TLabel')

        global user, act_pass
        user = StringVar()
        act_pass = StringVar()

        frame1 = Frame(self)
        frame1.grid(row=0, column=0)

        ttk.Label(frame1).grid(row=0, column=0, pady=(100, 10))
        ttk.Label(frame1, text='Delete Account', style='login.TLabel').grid(row=0, column=1, pady=(100, 10), padx=(8, 0))

        frame3 = Frame(self)
        frame3.grid(row=1, column=0)
        ttk.Label(frame3, text='USERNAME', style='TLabel').grid(row=1, column=0, pady=(50, 10))
        ttk.Label(frame3, text='PASSWORD ', style='TLabel').grid(row=2, column=0, )
        ttk.Entry(frame3, textvariable=user, width=20).grid(row=1, column=2, pady=(50, 10), padx=(20, 10))
        ttk.Entry(frame3, textvariable=act_pass, width=20).grid(row=2, column=2, padx=(20, 10))

        style = ttk.Style()
        style.configure('TButton', borderwidth=10)

        frame2 = Frame(self)
        frame2.grid(row=2, column=0, pady=20)
        b1 = ttk.Button(frame2, text='Sign Up', command=lambda: master.switch_frame(AppSignUpPage), style='TButton')
        b1.grid(row=0, column=0, pady=20, padx=10)
        b2 = ttk.Button(frame2, text='Login', command=lambda: master.switch_frame(AppLoginPage), style='TButton')
        b2.grid(row=0, column=1, pady=20, padx=10)
        b3 = ttk.Button(frame2, text='Delete', command=lambda: self.enter(master), style='TButton')
        b3.grid(row=0, column=2, pady=20, padx=10)

    def enter(self, master):
        if os.path.isfile(f'data/user_data/{user.get()}_pass_file.p'):
            with open(f'data/user_data/{user.get()}_pass_file.p', 'rb') as f:
                listt = pickle.load(f)
                a = decrypt_(listt[0], user.get())
                #b = decrypt_(listt[1], user.get())
                b = check_hash_(act_pass.get(), listt[1])
            if user.get() == a and b:
                choics = msg.askquestion('Confirm', 'Do you really want to delete')
                if choics == 'yes':
                    self.delete()
                    master.switch_frame(AppLoginPage)
            else:
                msg.showerror('Wrong', "Wrong user or password")
                user.set('')
                act_pass.set('')
        else:
            msg.showerror('Wrong', "Wrong user or password")
            user.set('')
            act_pass.set('')

    def delete(self):
        os.remove(f'data/user_data/{user.get()}_pass_file.p')
        if os.path.isfile(f'data/password_data/{user.get()}_pass.p'):
            os.remove(f'data/password_data/{user.get()}_pass.p')


# -------------------------------------------------------------------------------------------------------------------------------
#                                           Global functions for all classes to use
# -------------------------------------------------------------------------------------------------------------------------------
def genwrite_key(username):
    key = Fernet.generate_key()
    with open(f"data/key/{username}.key", "wb") as key_file:
        key_file.write(key)

def call_key(user):
    return open(f"data/key/{user}.key", "rb").read()

def encrypt_(msg, username):
    key = call_key(username)
    slogan = msg.encode()
    a = Fernet(key)
    coded_slogan = a.encrypt(slogan)
    return coded_slogan

def hash_(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hash_(password, hash):
    if hash_(password) == hash:
        return True

    return False

def decrypt_(msg, user):
    key = call_key(user)
    b = Fernet(key)
    decoded_slogan = b.decrypt(msg)
    decoded_slogan = decoded_slogan.decode('utf-8')
    return decoded_slogan

# -------------------------------------------------------------------------------------------------------------------------------
#                                           Executes Main Program, starts with MainApp()
# -------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

    f1 = open('data/mainApp_data/_data.p', 'wb')
    pickle.dump(theme, f1)
    f1.close()