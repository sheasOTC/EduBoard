from tkinter import *
import sqlite3

master = Tk()
master.minsize(width=1200, height=800)
master.maxsize(width=1200, height=800)
master.rowconfigure(5,weight=1)
master.columnconfigure(2,weight=1)
master.configure(bg='#0079b5')
master.title("EduBoard - Attendance")



con = sqlite3.connect("datebases\logins.db")
cur = con.cursor()

def personalise():
    pass

def administrator():
    pass


labelEduBoard = Label(master, text="EduBoard", font=("Quicksand Bold", 48),bg='#0079b5')
labelEduBoard.grid(column=4,row=0,)

frameFunctions = Frame(master, bg='#0079b5',bd=0)
frameFunctions.grid(column=4,row=1)
buttonTake_Attendance = Button(frameFunctions, text="Take Attendance",
                                   bd=0,
                                   bg='#0079b5',
                                   font=("Quicksand Bold", 20))
buttonTake_Attendance.grid(column=4,row=0)

if cur.execute(f"SELECT administrator FROM logins WHERE emails = 'self.hashUser'").fetchone()[0] == True:
    buttonCreate_Class = Button(frameFunctions, text="Create Class")
    buttonCreate_Class.grid(row=1,column=4)
    buttonConfigure_Class = Button(frameFunctions,text="Configure Class")
    buttonConfigure_Class.grid(column=4,row=2)



master.mainloop()



