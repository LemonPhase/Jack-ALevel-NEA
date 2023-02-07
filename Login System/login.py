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
    NewUsername = UsernameEntry.get()
    NewPassword = PasswordEntry.get()
    print(NewUsername, NewPassword)

    cursor.execute("SELECT COUNT(*) from users WHERE username = '" + NewUsername + "' ")
    result = cursor.fetchone()

    if int(result[0]) > 0:
        message["text"] = "Error: Username already exists"
    else:
        message["text"] = "Added new user"
        cursor.execute(
            "INSERT INTO users(username, password) VALUES(?,?)",
            (NewUsername, NewPassword),
        )
        db.commit()


def login():
    Username = UsernameEntry.get()
    Password = PasswordEntry.get()
    print(Username, Password)

    cursor.execute()


window = Tk()
window.geometry("450x180")

message = Message(text="", width=160)
message.place(x=30, y=10)
message.config(padx=0)

UsernameLabel = Label(text="Username: ")
UsernameLabel.place(x=30, y=40)
UsernameLabel.config(padx=0)
# bg="lightgreen",

UsernameEntry = Entry(text="")
UsernameEntry.place(x=150, y=40, width=200, height=25)


PasswordLabel = Label(text="Password: ")
PasswordLabel.place(x=30, y=80)
PasswordLabel.config(padx=0)
# bg="lightgreen",

PasswordEntry = Entry(text="")
PasswordEntry.place(x=150, y=80, width=200, height=25)

RegisterButton = Button(text="Register", command=register)
RegisterButton.place(x=150, y=120, width=75, height=35)

LoginButton = Button(text="Login", command=login)
LoginButton.place(x=250, y=120, width=75, height=35)
window.mainloop()
