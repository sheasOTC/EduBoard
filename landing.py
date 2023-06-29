from tkinter import *


landing = Tk()
landing.rowconfigure(6,weight=1)
landing.columnconfigure(0,weight=1)
landing.minsize(width=600, height=400)
landing.maxsize(width=1200, height=800)
landing.configure(bg='#717171')
landing.title("EduBoard - Main")


eduboard = Label(landing,text="EduBoard", font=("Comic Sans MS", 48),bg='#717171')
eduboard.grid(column=0,row=0,sticky='n')

landing.mainloop()
