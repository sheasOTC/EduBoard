from tkinter import *
import sqlite3

master = Tk()
master.minsize(width=1200, height=800)
master.maxsize(width=1200, height=800)
master.rowconfigure(5,weight=1)
master.columnconfigure(2,weight=1)
master.configure(bg='#0079b5')
master.title("EduBoard - Settings")

def personalise():
    pass

def administrator():
    pass



labelEduboard = Label(master,text="EduBoard", font=("Quicksand Bold", 48),bg='#0079b5')
labelEduboard.grid(row=0,column=2)

#labelUser = Label(master, text=f"user", font=("Quicksand Bold", 48),bg='#0079b5')
#labelUser.grid(row=0,coloumn=3)

frameSettings = Frame(master, bg='#0079b5',bd=0)
frameSettings.grid(row=1,column=2)

buttonPersonalise = Button(frameSettings,text="Personalise", font=("Quicksand Bold", 24),bg='#0079b5',command=personalise, width=12,pady=5)
buttonPersonalise.grid(row=0,column=2,pady=10)

buttonAdministrator  = Button(frameSettings, text="Administrator", font=("Quicksand Bold", 24),bg='#0079b5',command=administrator,width=12,pady=5)
buttonAdministrator.grid(row=1,column=2,pady=10)

buttonBack = Button(master,text="Go Back",command="", font=("Quicksand Bold", 18),bg='#0079b5')
buttonBack.grid(row=6,column=0)

master.mainloop()



