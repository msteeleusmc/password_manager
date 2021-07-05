import sqlite3
import hashlib
import bcrypt
from tkinter import *
from tkinter import simpledialog
from functools import  partial

# Database code
with sqlite3.connect("steele_trap.db") as db:
    cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS masterpassword(
        id INTEGER PRIMARY KEY,
        password TEXT NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS vault(
        id INTEGER PRIMARY KEY,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
""")

def popUp(text):
    answer = simpledialog.askstring("input string", text)

    return answer

# Initiate the window
window = Tk()

window.title("Steele Trap")

# Create a salt
salt = bcrypt.gensalt()

def HashPassword(input):
    hash = hashlib.sha512(input)
    hash = hash.hexdigest()

    return hash

def FirstScreen():
    window.geometry("350x150")

    lbl = Label(window, text="Create Master Password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show='*')
    txt.pack()
    txt.focus()

    lbl1 = Label(window, text="Re-enter Password")
    lbl1.pack()

    txt1 = Entry(window, width=20, show='*')
    txt1.pack()
    txt1.focus()

    lbl2 = Label(window)
    lbl2.pack()

    def SavePassword():
        if txt.get() == txt1.get():
            hashedPassword = HashPassword(txt.get().encode('utf-8'))

            insert_password = """INSERT INTO masterpassword(password)
            VALUES(?)"""
            cursor.execute(insert_password, [(hashedPassword)])
            db.commit()

            PasswordVault()
        else:
            lbl2.config(text="Passwords do not match")

    btn = Button(window, text="Save", command=SavePassword)
    btn.pack()

def LoginScreen():
    window.geometry("250x100")

    lbl = Label(window, text="Enter Master Password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show='*')
    txt.pack()
    txt.focus()

    lbl1 = Label(window)
    lbl1.pack()

    def getMasterPassword():
        checkHashedPassword = HashPassword(txt.get().encode('utf-8'))
        cursor.execute('SELECT * FROM masterpassword WHERE id = 1 AND password = ?', [(checkHashedPassword)])

        return cursor.fetchall()

    def CheckPassword():
        password = getMasterPassword()

        if password:
            PasswordVault()
        else:
            txt.delete(0, 'end')
            lbl1.config(text="Wrong Password")

    btn = Button(window, text="Submit", command=CheckPassword)
    btn.pack(pady=10)

def PasswordVault():
    for widget in window.winfo_children():
        widget.destroy()

    def addEntry():
        text1 = "URL"
        text2 = "Username"
        text3 = "Password"

        website = popUp(text1)
        username = popUp(text2)
        password = popUp(text3)

        insert_fields = """INSERT INTO vault(website,username,password)
        VALUES(?, ?, ?)"""

        cursor.execute(insert_fields, (website, username, password))
        db.commit()

        PasswordVault()

    def RemoveEntry(input):
        cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        db.commit()

        PasswordVault()

    window.geometry("700x350")

    lbl = Label(window, text="Password Manager")
    lbl.grid(column=1)

    btn = Button(window, text="+", command= addEntry)
    btn.grid(column=1, pady=10)

    lbl = Label(window, text="URL")
    lbl.grid(row=2, column=0, padx=88)
    lbl = Label(window, text="Username")
    lbl.grid(row=2, column=1, padx=88)
    lbl = Label(window, text="Password")
    lbl.grid(row=2, column=2, padx=88)

    cursor.execute("SELECT * FROM vault")
    if(cursor.fetchall() != None):
        i = 0
        while True:
            cursor.execute("SELECT * FROM vault")
            array = cursor.fetchall()

            lbl1 = Label(window, text=(array[i][1]), font=("Helvetica", 12))
            lbl1.grid(column=0, row=i+3)
            lbl1 = Label(window, text=(array[i][2]), font=("Helvetica", 12))
            lbl1.grid(column=1, row=i + 3)
            lbl1 = Label(window, text=(array[i][3]), font=("Helvetica", 12))
            lbl1.grid(column=2, row=i + 3)

            btn = Button(window, text="Delete", command= partial(RemoveEntry, array[i][0]))
            btn.grid(column=3, row=i+3, pady=10)

            i += 1

            cursor.execute("SELECT * from vault")
            if(len(cursor.fetchall()) <= i):
                break

cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
    LoginScreen()
else:
    FirstScreen()

window.mainloop()