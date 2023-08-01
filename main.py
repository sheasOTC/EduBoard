from tkinter import *
from tkinter import messagebox
import sqlite3
import hashlib


con = sqlite3.connect("logins.db")
cur = con.cursor()


class Login:
    def __init__(self, master):
        self.master = master
        master.rowconfigure(6,weight=1)
        master.columnconfigure(0,weight=1)
        self.master.minsize(width=1200, height=800)
        self.master.maxsize(width=1200, height=800)
        master.configure(bg='#717171')
        master.title("EduBoard - Login")

        self.eduboard = Label(self.master,text="EduBoard", font=("Quicksand Bold", 48),bg='#717171', )
        self.eduboard.grid(column=0,row=0,sticky='n')

        self.loginFrame = LabelFrame(self.master,text="Login", font=("Quicksand Bold", 36),labelanchor='n',bg='#717171')
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
        
        self.buttonSignuppage = Button(self.master, text='Sign up', command=self.open_signup, bg='#717171')
        self.buttonSignuppage.grid(column=0,row=2,pady=10)

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
        self.app = Signup(self.master)
        

class Signup:
    def __init__(self, master):
        self.master = master
        master.rowconfigure(6,weight=1)
        master.columnconfigure(0,weight=1)
        self.master.minsize(width=1200, height=800)
        self.master.maxsize(width=1200, height=800)
        master.configure(bg='#717171')
        master.title("EduBoard - Signup")

        eduboard = Label(self.master,text="EduBoard", font=("Quicksand Bold", 48),bg='#717171')
        eduboard.grid(column=0,row=0,sticky='n')
    
        self.loginFrame = LabelFrame(self.master,text="Sign Up", font=("Quicksand Bold", 24),labelanchor='n',bg='#717171')
        self.loginFrame.grid(column=0,row=1,sticky='n')
        self.labelUser = Label(self.loginFrame,text="Email",justify='center',bg='#717171')
        self.labelUser.grid(column=0,row=2)
        self.entryUser = Entry(self.loginFrame,justify='center')
        self.entryUser.grid(column=0,row=3)
        self.labelPass = Label(self.loginFrame,text="Password",bg='#717171')
        self.labelPass.grid(column=0,row=4)
        self.entryPass = Entry(self.loginFrame,show='*',justify='center')
        self.entryPass.grid(column=0,row=5)
        self.buttonSignup = Button(self.loginFrame,text="Sign Up",command=self.create_account,bg='#717171')
        self.buttonSignup.grid(column=0,row=6)

        self.buttonLoginpage = Button(self.master, text="Go Back", command=self.login_page)
        self.buttonLoginpage.grid(row=2,pady=10,column=0)

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
        elif self.entryPass.get() == "" and self.entryUser.get() == "":
                messagebox.showerror("EduBoard","Cannot leave password and email empty. \nPlease try again or contact your administrator.")
        elif self.entryUser.get() == "":
            messagebox.showerror("EduBoard","Cannot leave email empty. \nPlease try again or contact your administrator.")
        elif self.entryPass.get() == "":
            messagebox.showerror("EduBoard","Cannot leave password empty. \nPlease try again or contact your administrator.")
        else:
            encPassword = self.entryPass.get()
            encUser = self.entryUser.get()
            hashPassword = hashlib.md5(encPassword.encode()).hexdigest()
            hashUser = hashlib.md5(encUser.encode()).hexdigest()
            cur.execute(f"""INSERT INTO logins VALUES
                            ('{hashUser}', '{hashPassword}')
                            """)
            con.commit()
            self.login_page()
            messagebox.showinfo("EduBoard", "Successfully Created Account.")
    
    def login_page(self):
        self.loginFrame.destroy()
        self.buttonLoginpage.destroy()
        Login(self.master)

class Landing:
    def __init__(self, master, user):
        self.master = master

        self.master.rowconfigure(6,weight=1)
        self.master.columnconfigure(4,weight=1)
        self.master.minsize(width=1200, height=800)
        self.master.maxsize(width=1200, height=800)
        self.master.configure(bg='#717171')
        self.master.title("EduBoard - Main")

        
        self.labelEduboard = Label(self.master,text="EduBoard", font=("Quicksand Bold", 48),bg='#717171')
        self.labelEduboard.grid(column=0,row=0,sticky='n')

        self.username = Label(self.master,text=f"{user}", font=("Quicksand Bold", 38),bg='#717171')
        self.username.grid(column=4,row=0,sticky='n',pady=10,padx=20)

        self.functionality = LabelFrame(self.master, bg='#717171')
        self.functionality.grid(row=3,column=2)

        self.functionality.columnconfigure(0,weight=1)
        self.functionality.rowconfigure(4,weight=1)

        self.buttonAttendance = Button(self.functionality, text="Attendance",width=17,height=1, font=("Quicksand Bold", 18),bg='#717171')
        self.buttonAttendance.grid(row=0,column=0)

        self.buttonLookup = Button(self.functionality, text="Lookup",width=15,height=1, font=("Quicksand Bold", 18),bg='#717171')
        self.buttonLookup.grid(row=2,column=0)

        self.buttonReports = Button(self.functionality, text="Reports",width=15,height=1, font=("Quicksand Bold", 18),bg='#717171')
        self.buttonReports.grid(row=4,column=0)

        self.buttonLogout = Button(self.master,text="Logout",command=self.login_page, font=("Quicksand Bold", 18),bg='#717171')
        self.buttonLogout.grid(row=7,column=0,pady=50)

        self.buttonHelp = Button(self.master,text="Help",command=self.help_menu, font=("Quicksand Bold", 18),bg='#717171')
        self.buttonHelp.grid(row=7,column=4)
    def login_page(self):
        self.buttonLogout.destroy()
        self.username.destroy()
        self.labelEduboard.destroy()
        self.functionality.destroy()    
        self.buttonHelp.destroy()
        Login(self.master)

    def help_menu(self):
        help = Toplevel(self.master)



def main(): 
    root = Tk()
    Login(root)
    root.mainloop()
    


if __name__ == '__main__':
    main()