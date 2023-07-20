from tkinter import *


self.master.rowconfigure(6,weight=1)
self.master.columnconfigure(2,weight=1)
self.master.minsize(width=600, height=400)
self.master.maxsize(width=1200, height=800)
self.master.configure(bg='#717171')
self.master.title("EduBoard - Main")


labelEduboard = Label(self.master,text="EduBoard", font=("Comic Sans MS", 48),bg='#717171')
labelEduboard.grid(column=0,row=0,sticky='n')

eduboard = Label(self.master,text=f"{user}", font=("Comic Sans MS", 48),bg='#717171')
eduboard.grid(column=2,row=0,sticky='n')



landing.mainloop()
