from tkinter import *
from tkinter import messagebox
import sqlite3
import hashlib


con = sqlite3.connect("logins.db")
cur = con.cursor()

try:
    open("logins.db","x")
except FileExistsError:
    cur.execute("""CREATE TABLE IF NOT EXISTS
                logins(emails, passwords)""")
    con.commit()
finally:
    pass


class Login:
    def __init__(self, master, offset = 2):
        self.master = master
        self.master.minsize(width=1200, height=800)
        self.master.maxsize(width=1200, height=800)
        self.master.resizable(False, False)
        master.rowconfigure(6,weight=1)
        master.columnconfigure(2,weight=1)
        master.configure(bg='#0079b5')
        master.title("EduBoard - Login")

        self.eduboard = Label(self.master,text="EduBoard", font=("Quicksand Bold", 48),bg='#0079b5', )
        self.eduboard.grid(column=offset,row=2)

        self.loginFrame = LabelFrame(self.master,text="Login", font=("Quicksand Bold", 36),labelanchor='n',bg='#0079b5',width=5,height=5)
        self.loginFrame.grid(column=offset,row=3,sticky='n')
        self.labelUser = Label(self.loginFrame,text="Email",justify='center',bg='#0079b5', font=("Quicksand Bold", 12))
        self.labelUser.grid(column=3,row=2)
        self.entryUser = Entry(self.loginFrame,justify='center',width=24)
        self.entryUser.grid(column=3,row=3)
        self.labelPass = Label(self.loginFrame,text="Password",bg='#0079b5', font=("Quicksand Bold",12))
        self.labelPass.grid(column=3,row=4)
        self.entryPass = Entry(self.loginFrame,show='*',justify='center',width=24)
        self.entryPass.grid(column=3,row=5)
        self.buttonLogin = Button(self.loginFrame,text="Login",command=self.validate_login,bg='#0079b5', font=("Quicksand Bold", 12), bd=0)
        self.buttonLogin.grid(column=3,row=7)
        
        self.buttonSignuppage = Button(self.master, text="Don't have an account? Sign up.", command=self.open_signup, bg='#0079b5',bd=0, font=("Quicksand Bold",12))
        self.buttonSignuppage.grid(column=offset,row=4,pady=10)

    def validate_login(self):
        correctPassword = False
        correctUsername = False
        
        encPassword = self.entryPass.get()
        encUser = self.entryUser.get()
        hashPassword = hashlib.md5(encPassword.encode()).hexdigest()
        hashUser = hashlib.md5(encUser.encode()).hexdigest()
        for user in cur.execute("SELECT emails FROM logins").fetchall():
            if user[0] == hashUser:
                correctUsername = True
        for password in cur.execute("SELECT passwords FROM logins").fetchall():
            if password[0] == hashPassword:
                correctPassword = True
        if correctPassword and correctUsername == True:
            username = self.entryUser.get()
            self.eduboard.destroy()
            self.buttonSignuppage.destroy()
            self.loginFrame.destroy()
            Landing(self.master,username)
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
        self.loginFrame.destroy()
        self.buttonSignuppage.destroy()
        self.eduboard.destroy()
        Signup(self.master)

class Signup:
    def __init__(self, master):
        self.master = master
        self.master.minsize(width=1200, height=800)
        self.master.maxsize(width=1200, height=800)
        master.configure(bg='#0079b5')
        master.title("EduBoard - Signup")

        self.eduboard = Label(self.master,text="EduBoard", font=("Quicksand Bold", 48),bg='#0079b5')
        self.eduboard.grid(column=2,row=0,sticky='n')
    
        self.loginFrame = LabelFrame(self.master,text="Sign Up", font=("Quicksand Bold", 36),labelanchor='n',bg='#0079b5')
        self.loginFrame.grid(column=2,row=1,sticky='n')
        self.loginFrame.columnconfigure(2, weight=1)
        self.labelUser = Label(self.loginFrame,text="Email",justify='center',bg='#0079b5', font=("Quicksand Bold", 12))
        self.labelUser.grid(column=2,row=2)
        self.entryUser = Entry(self.loginFrame,justify='center',width=24)
        self.entryUser.grid(column=2,row=3)
        self.labelPass = Label(self.loginFrame,text="Password",bg='#0079b5', font=("Quicksand Bold", 12))
        self.labelPass.grid(column=2,row=4)
        self.entryPass = Entry(self.loginFrame,show='*',justify='center',width=24)
        self.entryPass.grid(column=2,row=5)
        self.buttonSignup = Button(self.loginFrame,text="Sign Up",command=self.create_account,bg='#0079b5', font=("Quicksand Bold", 12),bd=0)
        self.buttonSignup.grid(column=2,row=6)

        self.buttonLoginpage = Button(self.master, text="Go Back", command=self.login_page,bd=0,bg='#0079b5', font=("Quicksand Bold", 12))
        self.buttonLoginpage.grid(row=2,pady=10,column=2)

    def create_account(self):
        dupEmail = False
        dupPassword = False
        hashPassword = hashlib.md5(self.entryPass.get().encode()).hexdigest()
        hashUser = hashlib.md5(self.entryUser.get().encode()).hexdigest()
        for user in cur.execute("SELECT emails FROM logins").fetchall():
            if user[0] == hashUser:
                dupEmail = True
        if hashPassword == hashUser:
            dupPassword = True
        if dupEmail:
            messagebox.showerror('EduBoard', 'An account with this email already exists. \nPlease try again or contact your administrator.')
        elif dupPassword:
            messagebox.showerror('Eduboard', "Password cannot be the same as username, \nPlease try again or contact your administrator.")
        elif self.entryPass.get() == "" and self.entryUser.get() == "":
                messagebox.showerror("EduBoard","Cannot leave password and email empty. \nPlease try again or contact your administrator.")
        elif self.entryUser.get() == "":
            messagebox.showerror("EduBoard","Cannot leave email empty. \nPlease try again or contact your administrator.")
        elif self.entryPass.get() == "":
            messagebox.showerror("EduBoard","Cannot leave password empty. \nPlease try again or contact your administrator.")
        else:
            cur.execute(f"""INSERT INTO logins VALUES
                            ('{hashUser}', '{hashPassword}')
                            """)
            con.commit()
            self.login_page()
            messagebox.showinfo("EduBoard", "Successfully Created Account.")
    def login_page(self):
        self.loginFrame.destroy()
        self.buttonLoginpage.destroy()
        self.eduboard.destroy()
        Login(self.master)

class Landing:
    def __init__(self, master, user):
        self.master = master
        self.master.minsize(width=1200, height=800)
        self.master.maxsize(width=1200, height=800)
        self.master.rowconfigure(6,weight=1)
        self.master.columnconfigure(5,weight=1)
        self.master.configure(bg='#0079b5')
        self.master.title("EduBoard - Main")

        
        self.labelEduboard = Label(self.master,text="EduBoard", font=("Quicksand Bold", 48),bg='#0079b5')
        self.labelEduboard.grid()

        self.username = Label(self.master,text=f"{user}", font=("Quicksand Bold", 38),bg='#0079b5')
        self.username.grid(column=6,row=0)

        self.functionality = Frame(self.master, bg='#0079b5',bd=0)
        self.functionality.grid(row=3,column=3)

        self.functionality.columnconfigure(0,weight=1)
        self.functionality.rowconfigure(3,weight=1)

        self.buttonAttendance = Button(self.functionality, text="Attendance",width=15,height=1, font=("Quicksand Bold", 18),bg='#0079b5',pady=5)
        self.buttonAttendance.grid(row=0,column=0,pady=10)

        self.buttonLookup = Button(self.functionality, text="Lookup",width=15,height=1, font=("Quicksand Bold", 18),bg='#0079b5',pady=5)
        self.buttonLookup.grid(row=1,column=0,pady=10)

        self.buttonReports = Button(self.functionality, text="Reports",width=15,height=1, font=("Quicksand Bold", 18),bg='#0079b5',pady=5)
        self.buttonReports.grid(row=2,column=0,pady=10)

        self.buttonSettings = Button(self.functionality, text='Settings',width=15,height=1, font=("Quicksand Bold", 18),bg='#0079b5',pady=5)
        self.buttonSettings.grid(row=3,column=0,pady=10)

        self.buttonLogout = Button(self.master,text="Logout",command=self.login_page, font=("Quicksand Bold", 18),bg='#0079b5')
        self.buttonLogout.grid(row=7,column=0)

        self.buttonHelp = Button(self.master,text="Help",command=self.help_menu, font=("Quicksand Bold", 18),bg='#0079b5')
        self.buttonHelp.grid(row=7,column=6)
    
    def login_page(self):
        self.master.destroy()
        main()
        

    def help_menu(self):
        help = Toplevel(self.master)



def main(): 
    root = Tk()
    Login(root)
    root.mainloop()


if __name__ == '__main__':
    main()