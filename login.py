from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3
import os



# Connects to the sqlite3 database file; this file is automatically encrypted.

con = sqlite3.connect("logins.db")
cur = con.cursor()


cur.execute("CREATE TABLE IF NOT EXISTS logins(emails,passwords)")

# Login Function -- Validates information retrived from entries in the root 

def login():
    correctP = False
    correctU = False
    for user in cur.execute("SELECT emails FROM logins").fetchall():
        if user[0] == entryUser.get():
            correctU = True
    for password in cur.execute("SELECT passwords FROM logins").fetchall():
        if password[0] == entryPass.get():
            correctP = True
    if correctP and correctU == True:
        run_landing
    else:
        messagebox.showerror("EduBoard","Wrong email or password. \nPlease try again or contact your administrator.")
    
# Creates accounts for EduBoard - To be configured into administrator settings.

def create_account():
    dupEmail = False
    dupPass = False
    for user in cur.execute("SELECT emails FROM logins").fetchall():
        if user[0] == entryUser.get():
            dupEmail = True
    for password in cur.execute("SELECT passwords FROM logins").fetchall():
        if password[0] == entryPass.get() :
            dupPass = True
    if dupEmail or dupPass:
        messagebox.showerror('EduBoard', 'An account with this email already exists. \nPlease try again or contact your administrator.')
    
    if entryUser.get() == "" or entryPass.get() == "":
        print(entryUser.get())
    else:
        cur.execute(f"""INSERT INTO logins VALUES
                        ('{entryUser.get()}', '{entryPass.get()}')
                        """)
        con.commit()

def run_landing():
    os.system('landing.py')

# Defines the root window -- Configures root window

root = Tk()
root.rowconfigure(6,weight=1)
root.columnconfigure(0,weight=1)
root.minsize(width=600, height=400)
root.maxsize(width=1200, height=800)
root.configure(bg='#717171')
root.title("EduBoard - Login")


reveal = Image.open('eyegraphic.png')
reveal = reveal.convert("RGBA")
transparent = Image.new("RGBA", reveal.size, (0, 0, 0, 0))
composed_image = Image.alpha_composite(transparent, reveal)
temp_filename = "temp.gif"
composed_image.save(temp_filename, format="GIF")
tk_image = PhotoImage(file=temp_filename).subsample(8)

eduboard = Label(root,text="EduBoard", font=("Comic Sans MS", 48),bg='#717171')
eduboard.grid(column=0,row=0,sticky='n')



# Creates loginframe -- Used to display widgets that are used for loging in to EduBoard

loginFrame = LabelFrame(root,text="Login", font=("Coolvetica", 24),labelanchor='n',bg='#717171')
loginFrame.grid(column=0,row=1,sticky='n')
labelUser = Label(loginFrame,text="Email",justify='center',bg='#717171')
labelUser.grid(column=0,row=2)
entryUser = Entry(loginFrame,justify='center')
entryUser.grid(column=0,row=3)
labelPass = Label(loginFrame,text="Password",bg='#717171')
labelPass.grid(column=0,row=4)
entryPass = Entry(loginFrame,show='*',justify='center')
entryPass.grid(column=0,row=5)
buttonLogin = Button(loginFrame,text="Login",command=login,bg='#717171')
buttonLogin.grid(column=0,row=7)



buttonSignup = Button(root, text='Sign up', command=create_account, bg='#717171')
buttonSignup.grid(column=0,row=2,pady=10)



root.mainloop()