from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
import hashlib
import time

con = sqlite3.connect("datebases\logins.db")
cur = con.cursor()

try:
    open("datebases\logins.db","x")
except FileExistsError:
    cur.execute("""CREATE TABLE IF NOT EXISTS
                logins(emails, passwords, administrator)""")
    con.commit()
finally:
    pass


class Login:
    def __init__(self, master):
        self.master = master
        self.master.minsize(width=1200, height=800)
        self.master.maxsize(width=1200, height=800)
        self.master.resizable(False, True)
        master.rowconfigure(6,weight=1)
        master.columnconfigure(4,weight=1)
        master.configure(bg='#0079b5')
        master.title("EduBoard - Login")

        self.eduboard = Label(self.master,text="EduBoard", font=("Quicksand Bold", 48),bg='#0079b5', )
        self.eduboard.grid(column=4,row=0)

        self.loginFrame = LabelFrame(self.master,text="Login", font=("Quicksand Bold", 36),labelanchor='n',bg='#0079b5',width=5,height=5)
        self.loginFrame.grid(column=4,row=1,sticky='n')
        self.labelUser = Label(self.loginFrame,text="Email",justify='center',bg='#0079b5', font=("Quicksand Bold", 12))
        self.labelUser.grid(column=3,row=0)
        self.entryUser = Entry(self.loginFrame,justify='center',width=24)
        self.entryUser.grid(column=3,row=1)
        self.labelPass = Label(self.loginFrame,text="Password",bg='#0079b5', font=("Quicksand Bold",12))
        self.labelPass.grid(column=3,row=2)
        self.entryPass = Entry(self.loginFrame,show='*',justify='center',width=24)
        self.entryPass.grid(column=3,row=3)
        self.buttonLogin = Button(self.loginFrame,text="Login",command=self.validate_login,bg='#0079b5', font=("Quicksand Bold", 12), bd=0)
        self.buttonLogin.grid(column=3,row=4)
        

    def validate_login(self):
        correctPassword = False
        correctUsername = False
        
        encPassword = self.entryPass.get()
        hashPassword = hashlib.md5(encPassword.encode()).hexdigest()
        for user in cur.execute("SELECT emails FROM logins").fetchall():
            if user[0] == self.entryUser.get():
                correctUsername = True
        for password in cur.execute("SELECT passwords FROM logins").fetchall():
            if password[0] == hashPassword:
                correctPassword = True
        if correctPassword and correctUsername == True:
            username = self.entryUser.get()
            self.eduboard.destroy()
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

class Create_User:
    def __init__(self, master,user):
        self.user = user
        self.master = master
        master.title("EduBoard - Signup")

        self.eduboard = Label(self.master,text="EduBoard", font=("Quicksand Bold", 48),bg='#0079b5')
        self.eduboard.grid(column=4,row=0,sticky='n')
    
        self.loginFrame = LabelFrame(self.master,text="Create User", font=("Quicksand Bold", 36),labelanchor='n',bg='#0079b5')
        self.loginFrame.grid(column=4,row=1,sticky='n')
        self.loginFrame.columnconfigure(2, weight=1)
        self.labelUser = Label(self.loginFrame,text="Email",justify='center',bg='#0079b5', font=("Quicksand Bold", 12))
        self.labelUser.grid(column=2,row=2)
        self.entryUser = Entry(self.loginFrame,justify='center',width=24)
        self.entryUser.grid(column=2,row=3)
        self.labelPass = Label(self.loginFrame,text="Password",bg='#0079b5', font=("Quicksand Bold", 12))
        self.labelPass.grid(column=2,row=4)
        self.entryPass = Entry(self.loginFrame,show='*',justify='center',width=24)
        self.entryPass.grid(column=2,row=5)
        self.buttonSignup = Button(self.loginFrame,text="Create",command=self.create_account,bg='#0079b5', font=("Quicksand Bold", 12),bd=0)
        self.buttonSignup.grid(column=2,row=6)

        self.buttonAdmin_Page = Button(self.master, text="Go Back", command=self.admin_page,bd=0,bg='#0079b5', font=("Quicksand Bold", 12))
        self.buttonAdmin_Page.grid(row=4,pady=10,column=4)

    def create_account(self):
        dupEmail = False
        dupPassword = False
        hashPassword = hashlib.md5(self.entryPass.get().encode()).hexdigest()
        for user in cur.execute("SELECT emails FROM logins").fetchall():
            if user[0] == self.entryUser.get():
                dupEmail = True
        if self.entryPass.get() == self.entryUser.get():
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
                            ('{self.entryUser.get()}', '{hashPassword}', False)
                            """)
            con.commit()
            print(self.entryUser.get())
            self.admin_page()
            messagebox.showinfo("EduBoard", "Successfully Created Account.")
    def admin_page(self):
        self.loginFrame.destroy()
        self.buttonAdmin_Page.destroy()
        self.eduboard.destroy()
        Admin(self.master,self.user)
class Landing:
    def __init__(self, master, user):
        self.user = user
        self.master = master
        self.master.configure(bg='#0079b5')
        self.master.title("EduBoard - Main")

        
        self.labelEduboard = Label(self.master,text="EduBoard", font=("Quicksand Bold", 48),bg='#0079b5')
        self.labelEduboard.grid(row=0)

        self.username = Label(self.master,text=f"{user}", font=("Quicksand Bold", 38),bg='#0079b5')
        self.username.grid(column=6,row=0)

        self.functionality = Frame(self.master, bg='#0079b5',bd=0)
        self.functionality.grid(row=1,column=3,padx=180)

        self.functionality.columnconfigure(0,weight=1)
        self.functionality.rowconfigure(3,weight=1)

        self.buttonAttendance = Button(self.functionality, text="Attendance",width=15,height=1, font=("Quicksand Bold", 18),bg='#0079b5',pady=5,command=self.attendance)
        self.buttonAttendance.grid(row=0,column=0,pady=10)

        self.buttonLookup = Button(self.functionality, text="Lookup",width=15,height=1, font=("Quicksand Bold", 18),bg='#0079b5',pady=5)
        self.buttonLookup.grid(row=1,column=0,pady=10)

        self.buttonReports = Button(self.functionality, text="Reports",width=15,height=1, font=("Quicksand Bold", 18),bg='#0079b5',pady=5)
        self.buttonReports.grid(row=2,column=0,pady=10)

        self.buttonSettings = Button(self.functionality, text='Settings',width=15,height=1, font=("Quicksand Bold", 18),bg='#0079b5',pady=5,command=self.settings_page)
        self.buttonSettings.grid(row=3,column=0,pady=10)

        self.buttonLogout = Button(self.master,text="Logout",command=self.login_page, font=("Quicksand Bold", 18),bg='#0079b5')
        self.buttonLogout.grid(row=7,column=0)

        self.buttonHelp = Button(self.master,text="Help",command=self.help_menu, font=("Quicksand Bold", 18),bg='#0079b5')
        self.buttonHelp.grid(row=7,column=6)
    
    def login_page(self):
        self.master.destroy()
        main()
    
    def settings_page(self):
        self.labelEduboard.destroy()
        self.functionality.destroy()
        self.buttonLogout.destroy()
        self.buttonHelp.destroy()
        Admin_Login(self.master, self.user)

    def help_menu(self):
        help = Toplevel(self.master)
    def attendance(self):
        self.labelEduboard.destroy()
        self.username.destroy()
        self.functionality.destroy()
        Attendance_Selection(self.master,self.user)
class Lookup:
    def __init__(self):
        pass

class Reports:
    def __init__(self):
        pass

class Admin_Login:
    def __init__(self, master,user):
        self.user = user
        self.master = master
        self.master.title("EduBoard - Admin")
        self.labelEduboard = Label(self.master,text="EduBoard", font=("Quicksand Bold", 48),bg='#0079b5') 
        self.labelEduboard.grid(column=4,row=0,padx=240)
        self.frameAdmin = Frame(self.master, bg='#0079b5',bd=0)
        self.frameAdmin.grid(column=4,row=1,padx=120)
        self.buttonBack = Button(self.frameAdmin,text="Go Back",command=self.go_back, font=("Quicksand Bold", 18),bg='#0079b5')
        self.buttonBack.grid(row=3,column=3)        
        if cur.execute(f"SELECT administrator FROM logins WHERE emails = '{self.user}'").fetchone()[0] == False:
            self.labelAdmin_password = Label(self.frameAdmin, text="Enter administrator password.",font=("Quicksand Bold", 12),bg='#0079b5')
            self.labelAdmin_password.grid(column=3,row=0)
            self.entryAdmin = Entry(self.frameAdmin,show='*',justify='center',width=24,bg='#0079b5')
            self.entryAdmin.grid(column=3,row=1)
            self.buttonLogin = Button(self.frameAdmin, text="Login",bd=0,bg='#0079b5',command=self.validate_password)
            self.buttonLogin.grid(column=3,row=2)
        else:
            self.admin_page()

    def go_back(self):
        self.frameAdmin.destroy()
        self.labelEduboard.destroy()
        Landing(self.master, self.user) 
    def validate_password(self):
        if self.entryAdmin.get() == "123":
            self.admin_page()
        else:
            messagebox.showerror("EduBoard","Wrong password. \nPlease try again or contact your administrator.")
    def admin_page(self):
        if cur.execute(f"SELECT administrator FROM logins WHERE emails = '{self.user}'").fetchone()[0] == False:
            con.execute(f"""UPDATE logins
                            SET administrator = True
                            WHERE emails = '{self.user}'""")
            con.commit()
        self.labelEduboard.destroy()
        self.frameAdmin.destroy()
        self.buttonBack.destroy()
        Admin(self.master,self.user)         
class Admin:
    def __init__(self,master,user):
        self.user = user
        self.master = master
        self.labelEduboard = Label(self.master,text="EduBoard", font=("Quicksand Bold", 48),bg='#0079b5') 
        self.labelEduboard.grid(column=4,row=0,sticky='N')
        self.frameAdmin_Tools = Frame(self.master, bg='#0079b5',bd=0,padx=180)
        self.frameAdmin_Tools.grid(column=4,row=1)
        self.buttonCreate_User = Button(self.frameAdmin_Tools, 
                                        text="Create User",
                                        bd=0,
                                        bg='#0079b5',
                                        font=("Quicksand Bold", 20),
                                        command=self.create_user)
        self.buttonRemove_User = Button(self.frameAdmin_Tools,
                                        text="Remove Teacher or Student",
                                        bd=0,
                                        bg='#0079b5',
                                        font=("Quicksand Bold", 20),
                                        command=self.remove_user)
        self.buttonCreate_User.grid(column=3,row=0)
        self.buttonRemove_User.grid(column=3,row=1)
        self.buttonBack = Button(self.master,text="Return", command=self.go_back, font=("Quicksand Bold", 12),bg='#0079b5')
        self.buttonBack.grid(column=4,row=2)
    def create_user(self):
        self.frameAdmin_Tools.destroy()
        self.labelEduboard.destroy()
        self.buttonBack.destroy()
        Create_User(self.master,self.user)
    def remove_user(self):
        self.frameAdmin_Tools.destroy()
        self.buttonBack.destroy()
        self.labelEduboard.destroy()
        Remove_User(self.master, self.user)

    def go_back(self):
        self.frameAdmin_Tools.destroy()
        self.buttonBack.destroy()
        self.labelEduboard.destroy()
        Landing(self.master, self.user) 


class Remove_User:
    def __init__(self,master,user):
        self.username = user
        self.master = master
        self.labelEduboard = Label(master,text="EduBoard", font=("Quicksand Bold", 48),bg='#0079b5') 
        self.labelEduboard.grid(column=4,row=0,)

        users_list = cur.execute("SELECT emails FROM logins WHERE administrator = False").fetchall()
        self.users = ttk.Treeview(master,columns='Emails', show="headings")
        style = ttk.Style()
        style.configure("Treeview",background='0079b5')
        self.users.heading('Emails', text="Email")
        self.users.column("Emails",anchor=CENTER , width=150)
        for user in users_list:
            print(user)
            self.users.insert('',END, values=user)
        self.users.grid(row=1,column=4)
        self.scrollbar = Scrollbar(master, orient=VERTICAL, command=self.users.yview)
        self.users.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=1,column=4,padx=160)
        self.buttonDelete_User = Button(master, text="Delete User",
                                    command=self.delete_user,
                                    bd=0,
                                    bg='#0079b5',
                                    font=("Quicksand Bold", 20),)   
        self.buttonDelete_User.grid(row=2,column=4)
        self.buttonBack = Button(self.master,text="Return", command=self.go_back, font=("Quicksand Bold", 12),bg='#0079b5')
        self.buttonBack.grid(column=4,row=3)
    def delete_user(self):
        for i in self.users.selection():
            Failed = False
            users = self.users.item(i)
            user = users["values"][0]
            cur.execute(f'DELETE FROM logins WHERE emails = "{user}"')
            con.commit()
        if Failed == False:
            messagebox.showinfo("EduBoard", "Successfully Deleted User(s).")


    def go_back(self):
        self.users.destroy()
        self.buttonBack.destroy()
        self.labelEduboard.destroy()
        self.scrollbar.destroy()
        self.buttonDelete_User.destroy()
        Admin(self.master,self.username)


class Attendance_Selection:
    def __init__(self,master,user):
        self.master = master
        self.user = user
        master.title("EduBoard - Attendance")
        self.labelEduBoard = Label(master, text="EduBoard", font=("Quicksand Bold", 48),bg='#0079b5')
        self.labelEduBoard.grid(column=4,row=0,)

        self.frameFunctions = Frame(master, bg='#0079b5',bd=0)
        self.frameFunctions.grid(column=4,row=1)
        buttonTake_Attendance = Button(self.frameFunctions, text="Take Attendance",
                                        bd=0,
                                        bg='#0079b5',
                                        font=("Quicksand Bold", 20))
        buttonTake_Attendance.grid(column=4,row=0)

        if cur.execute(f"SELECT administrator FROM logins WHERE emails = '{self.user}'").fetchone()[0] == True:
            buttonCreate_Class = Button(self.frameFunctions, text="Create Class",bd=0,
                                        bg='#0079b5',
                                        font=("Quicksand Bold", 20))
            buttonCreate_Class.grid(row=1,column=4)
            buttonConfigure_Class = Button(self.frameFunctions,text="Configure Class",bd=0,
                                        bg='#0079b5',
                                        font=("Quicksand Bold", 20))
            buttonConfigure_Class.grid(column=4,row=2)
        self.buttonBack = Button(self.frameFunctions,text="Go Back",command=self.go_back, font=("Quicksand Bold", 18),bg='#0079b5')
        self.buttonBack.grid(column=4,row=3)

    def go_back(self):
        self.labelEduBoard.destroy()
        self.frameFunctions.destroy()
        Landing(self.master, self.user)




def main(): 
    root = Tk()  
    Login(root)
    root.mainloop()


if __name__ == '__main__':
    main()