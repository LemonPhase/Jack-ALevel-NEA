from tkinter import *
import sqlite3
import os

# Change cwd
os.chdir(os.path.dirname(__file__))


class Login:
    def __init__(self):
        with sqlite3.connect("database.db") as database:
            self.db = database
            self.cursor = self.db.cursor()

            self.cursor.execute(
                """ CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY AUTOINCREMENT, 
            username text NOT NULL, 
            password text NOT NULL)"""
            )

    def DisplayMessage(self, text):
        message["text"] = text

    def Register(self):
        NewUsername = UsernameEntry.get()
        NewPassword = PasswordEntry.get()
        print(NewUsername, NewPassword)

        self.cursor.execute(
            "SELECT COUNT(*) from users WHERE username = '" + NewUsername + "' "
        )
        result = self.cursor.fetchone()

        if int(result[0]) > 0:
            self.DisplayMessage("Error: Username already exists")
        else:
            self.DisplayMessage("Added new user")
            self.cursor.execute(
                "INSERT INTO users(username, password) VALUES(?,?)",
                (NewUsername, NewPassword),
            )
            self.db.commit()

    def Login(self):
        Username = UsernameEntry.get()
        Password = PasswordEntry.get()
        print(Username, Password)

        self.cursor.execute(f"SELECT * FROM users WHERE username='{Username}'")
        UserEntry = self.cursor.fetchall()
        print(UserEntry)  # Returns the list of entries with entered username

        if len(UserEntry) == 0:
            self.DisplayMessage(f"Error: No user with username '{Username}' found")

        elif len(UserEntry) == 1:
            User = UserEntry[0]  # Tuple of the entry
            if Password == User[2]:
                self.DisplayMessage(f"Succesfully logged in")
            else:
                self.DisplayMessage(f"Incorrect password")
        else:
            self.DisplayMessage(
                f"Error: database contain entries with the same Username"
            )


login = Login()

Window = Tk()
Window.geometry("450x180")

message = Message(text="", width=250)
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

RegisterButton = Button(text="Register", command=login.Register())
RegisterButton.place(x=150, y=120, width=75, height=35)

LoginButton = Button(text="Login", command=login.Login())
LoginButton.place(x=250, y=120, width=75, height=35)
Window.mainloop()


Login.db.close()
