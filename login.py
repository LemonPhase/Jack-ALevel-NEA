from tkinter import *
class login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("800x600")


root = Tk()
obj = login(root)
root.mainloop()