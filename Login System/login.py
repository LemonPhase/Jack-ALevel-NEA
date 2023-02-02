from tkinter import *

import sqlite3

import os
# Change cwd
os.chdir(os.path.dirname(__file__))


with sqlite3.connect("database.db") as db:
    cursor = db.cursor()


cursor.execute(
    """ CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY AUTOINCREMENT, 
    username text NOT NULL, 
    password text NOT NULL)"""
)


def register():
    newUsername = username.get()
    newPassword = password.get()
    print(newUsername, newPassword)

    cursor.execute("SELECT COUNT(*) from users WHERE username = '" + newUsername + "' ")
    result = cursor.fetchone()

    if int(result[0]) > 0:
        message["text"] = "Error: Username already exists"
    else:
        message["text"] = "Added new user"
        cursor.execute(
            "INSERT INTO users(username, password) VALUES(?,?)",
            (newUsername, newPassword),
        )
        db.commit()


window = Tk()
window.geometry("450x180")

message = Message(text="", width=160)
message.place(x=30, y=10)
message.config(padx=0)

label1 = Label(text="Username: ")
label1.place(x=30, y=40)
label1.config(bg="lightgreen", padx=0)

username = Entry(text="")
username.place(x=150, y=40, width=200, height=25)


label2 = Label(text="Password: ")
label2.place(x=30, y=80)
label2.config(bg="lightgreen", padx=0)

password = Entry(text="")
password.place(x=150, y=80, width=200, height=25)


button1 = Button(text="Register", command=register)
button1.place(x=150, y=120, width=75, height=35)

window.mainloop()
