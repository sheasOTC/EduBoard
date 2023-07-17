from tkinter import *
from tkinter import messagebox
import sqlite3


con = sqlite3.connect("logins.db")
cur = con.cursor()


class Login:
    def __init__(self, master):
        self.master = master
        master.rowconfigure(6,weight=1)
        master.columnconfigure(0,weight=1)
        master.minsize(width=600, height=400)
        master.maxsize(width=1200, height=800)
        master.configure(bg='#717171')
        master.title("EduBoard - Login")

        eduboard = Label(self.master,text="EduBoard", font=("Comic Sans MS", 48),bg='#717171')
        eduboard.grid(column=0,row=0,sticky='n')

        self.loginFrame = LabelFrame(self.master,text="Login", font=("Coolvetica", 24),labelanchor='n',bg='#717171')
        self.loginFrame.grid(column=0,row=1,sticky='n')
        self.labelUser = Label(self.loginFrame,text="Email",justify='center',bg='#717171')
        self.labelUser.grid(column=0,row=2)
        self.entryUser = Entry(self.loginFrame,justify='center')
        self.entryUser.grid(column=0,row=3)
        self.labelPass = Label(self.loginFrame,text="Password",bg='#717171')
        self.labelPass.grid(column=0,row=4)
        self.entryPass = Entry(self.loginFrame,show='*',justify='center')
        self.entryPass.grid(column=0,row=5)
        self.buttonLogin = Button(self.loginFrame,text="Login",command=self.validate_login,bg='#717171')
        self.buttonLogin.grid(column=0,row=7)

        
        buttonSignup = Button(self.master, text='Sign up', command=self.open_signup, bg='#717171')
        buttonSignup.grid(column=0,row=2,pady=10)

    def validate_login(self):
        correctP = False
        correctU = False
        for user in cur.execute("SELECT emails FROM logins").fetchall():
            if user[0] == self.entryUser.get():
                correctU = True
        for password in cur.execute("SELECT passwords FROM logins").fetchall():
            if password[0] == self.entryPass.get():
                correctP = True
        if correctP and correctU == True:
            self.master.quit()
        else:
            if self.entryPass.get() == "" and self.entryUser.get() == "":
                messagebox.showerror("EduBoard","Cannot leave password and email empty. \nPlease try again or contact your administrator.")
            elif self.entryUser.get() == "":
                messagebox.showerror("EduBoard","Cannot leave email empty. \nPlease try again or contact your administrator.")
            elif self.entryPass.get() == "":
                messagebox.showerror("EduBoard","Cannot leave password empty. \nPlease try again or contact your administrator.")
            else:
                messagebox.showerror("EduBoard","Wrong email or password. \nPlease try again or contact your administrator.")

    def open_signup(self):
        self.signupWindow = Toplevel(self.master)
        self.app = Signup(self.signupWindow)
        

class Signup:
    def __init__(self, master):
        self.master = master
        master.rowconfigure(6,weight=1)
        master.columnconfigure(0,weight=1)
        master.minsize(width=600, height=400)
        master.maxsize(width=1200, height=800)
        master.configure(bg='#717171')
        master.title("EduBoard - Signup")

        eduboard = Label(self.master,text="EduBoard", font=("Comic Sans MS", 48),bg='#717171')
        eduboard.grid(column=0,row=0,sticky='n')
    
        self.loginFrame = LabelFrame(self.master,text="Sign Up", font=("Coolvetica", 24),labelanchor='n',bg='#717171')
        self.loginFrame.grid(column=0,row=1,sticky='n')
        self.labelUser = Label(self.loginFrame,text="Email",justify='center',bg='#717171')
        self.labelUser.grid(column=0,row=2)
        self.entryUser = Entry(self.loginFrame,justify='center')
        self.entryUser.grid(column=0,row=3)
        self.labelPass = Label(self.loginFrame,text="Password",bg='#717171')
        self.labelPass.grid(column=0,row=4)
        self.entryPass = Entry(self.loginFrame,show='*',justify='center')
        self.entryPass.grid(column=0,row=5)
        self.buttonLogin = Button(self.loginFrame,text="Sign Up",command=self.create_account,bg='#717171')
        self.buttonLogin.grid(column=0,row=7)

    def create_account(self):
        dupEmail = False
        dupPass = False
        for user in cur.execute("SELECT emails FROM logins").fetchall():
            if user[0] == self.entryUser.get():
                dupEmail = True
        for password in cur.execute("SELECT passwords FROM logins").fetchall():
            if password[0] == self.entryUser.get() :
                dupPass = True
        if dupEmail or dupPass:
            messagebox.showerror('EduBoard', 'An account with this email already exists. \nPlease try again or contact your administrator.')

        if self.entryUser.get() == "" or self.entryUser.get() == "":
            print(self.entryUser.get())
        else:
            cur.execute(f"""INSERT INTO logins VALUES
                            ('{self.entryUser.get()}', '{self.entryUser.get()}')
                            """)
            con.commit()
            self.master.destroy()
            messagebox.showinfo("EduBoard", "Successfully Created Account.")
        

def main(): 
    root = Tk()
    app = Login(root)
    root.mainloop()

if __name__ == '__main__':
    main()