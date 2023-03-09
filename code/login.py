from tkinter import *
import sqlite3
import os

# Change cwd
os.chdir(os.path.dirname(__file__))


class Login:
    def __init__(self):
        self.loggedin = False

        self.Window = Tk()
        self.Window.geometry("450x180")
        self.Window.title("Login menu")

        self.message = Message(text="", width=300)
        self.message.place(x=30, y=10)
        self.message.config(padx=0)

        self.db = sqlite3.connect("database.db")
        self.cursor = self.db.cursor()

        self.cursor.execute(
            """ CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY AUTOINCREMENT, 
            username text NOT NULL, 
            password text NOT NULL)"""
        )

        self.UsernameEntry = Entry(text="")
        self.UsernameEntry.place(x=150, y=40, width=200, height=25)

        self.PasswordEntry = Entry(text="")
        self.PasswordEntry.place(x=150, y=80, width=200, height=25)

        # GUI
        UsernameLabel = Label(text="Username: ")
        UsernameLabel.place(x=30, y=40)
        UsernameLabel.config(padx=0)

        PasswordLabel = Label(text="Password: ")
        PasswordLabel.place(x=30, y=80)
        PasswordLabel.config(padx=0)

        RegisterButton = Button(text="Register", command=self.register)
        RegisterButton.place(x=100, y=120, width=75, height=35)

        LoginButton = Button(text="Login", command=self.login)
        LoginButton.place(x=200, y=120, width=75, height=35)

        GuestButton = Button(text="Play as Guest", command=self.guest)
        GuestButton.place(x=300, y=120, width=100, height=35)

    def displaymessage(self, text):
        self.message["text"] = text

    def register(self):
        NewUsername = self.UsernameEntry.get()
        NewPassword = self.PasswordEntry.get()
        print(NewUsername, NewPassword)

        self.cursor.execute("SELECT COUNT(*) from users WHERE username = '" + NewUsername + "' ")
        result = self.cursor.fetchone()

        if len(NewUsername) < 4:
            self.displaymessage("Error: Username has to be at least 4 characters long")
            return
        if len(NewPassword) < 8:
            self.displaymessage("Error: Password has to be at least 8 characters long")
            return

        if int(result[0]) > 0:
            self.displaymessage("Error: Username already exists")
            return
        else:
            self.displaymessage("Added new user")
            self.cursor.execute(
                "INSERT INTO users(username, password) VALUES(?,?)",
                (NewUsername, NewPassword),
            )
            self.db.commit()

    def login(self):
        Username = self.UsernameEntry.get()
        Password = self.PasswordEntry.get()
        print(Username, Password)

        self.cursor.execute(f"SELECT * FROM users WHERE username='{Username}'")
        UserEntry = self.cursor.fetchall()
        print(UserEntry)  # Returns the list of entries with entered username

        if len(UserEntry) == 0:
            self.displaymessage(f"Error: No user with username '{Username}' found")

        elif len(UserEntry) == 1:
            User = UserEntry[0]  # Tuple of the entry
            if Password == User[2]:
                self.displaymessage(f"Succesfully logged in, launching game...")
                print("Succesfully logged in, launching game...")
                self.destroy()
            else:
                self.displaymessage(f"Incorrect password")
        else:
            self.displaymessage(f"Error: database contain entries with the same Username")

    def guest(self):
        self.displaymessage("Play as guest")
        print("Playing as guest")
        self.destroy()

    def run(self):
        self.Window.mainloop()

    def destroy(self):
        self.Window.destroy()


if __name__ == "__main__":
    login1 = Login()
    login1.run()

    login1.db.close()
