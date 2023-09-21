from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
import hashlib
from tkcalendar import DateEntry
import random
import datetime

# Connects to the logins.db
con = sqlite3.connect("datebases\logins.db")
cur = con.cursor()

# Connects to the classes.db
con_classes = sqlite3.connect("datebases\classes.db")
cur_classes = con_classes.cursor()

con_students = sqlite3.connect("datebases\students.db")
cur_students = con_students.cursor()


try:
    open("datebases\logins.db", "x")
    open("datebases\students.db", "x")
except FileExistsError:
    cur.execute("""CREATE TABLE IF NOT EXISTS
                logins(emails, passwords, administrator)""")
    con.commit()

    cur_students.execute("""CREATE TABLE IF NOT EXISTS
                students(id, year, first_name, last_name, dob, phone_number, 
                parent1_first_name, parent1_last_name, parent1_dob, parent2_phone number,
                parent2_first_name, parent2_last_name, parent2_dob, parent2_phone_number,
                emergency_first_name, emergency_last_name, emergency_dob ,emergency_phone_number)""")
    con_students.commit()
finally:
    pass


class Login:
    '''Has self parameter, and retrives master parameter (Tk()) 
    from when intially called.
    Setups the "Login" Frame using Tkinter widgets.'''

    def __init__(self, master):
        self.master = master
        master.minsize(width=1200, height=800)
        master.maxsize(width=1200, height=800)
        master.resizable(False, True)
        master.rowconfigure(6, weight=1)
        master.columnconfigure(4, weight=1)
        master.configure(bg='#0079b5')
        master.title("EduBoard - Login")

        self.label_eduboard = Label(master,
                                    text="EduBoard",
                                    font=("Quicksand Bold", 48),
                                    bg='#0079b5', )
        self.label_eduboard.grid(column=4, row=0)

        self.login_frame = LabelFrame(master,
                                      text="Login",
                                      font=("Quicksand Bold", 36),
                                      labelanchor='n',
                                      bg='#0079b5',
                                      width=5,
                                      height=5)
        self.login_frame.grid(column=4, row=1, sticky='n')

        self.label_user = Label(self.login_frame,
                                text="Email",
                                justify='center',
                                bg='#0079b5',
                                font=("Quicksand Bold", 12))
        self.label_user.grid(column=3, row=0)

        self.entry_user = Entry(self.login_frame,
                                justify='center',
                                width=24)
        self.entry_user.grid(column=3, row=1)

        self.label_pass = Label(self.login_frame,
                                text="Password",
                                bg='#0079b5',
                                font=("Quicksand Bold", 12))
        self.label_pass.grid(column=3, row=2)

        self.entry_pass = Entry(self.login_frame,
                                show='*',
                                justify='center',
                                width=24)
        self.entry_pass.grid(column=3, row=3)

        self.button_login = Button(self.login_frame,
                                   text="Login",
                                   command=self.validate_login,
                                   bg='#0079b5',
                                   font=("Quicksand Bold", 12),
                                   bd=0)
        self.button_login.grid(column=3, row=4)

    def validate_login(self):
        '''Retrives parameter self from __init__: Is used to validate user inputted and
          then proceeds to login if all information corrolates with logins.db'''

        correct_password = False
        correct_username = False

        hash_password = hashlib.md5(self.entry_pass.get().encode()).hexdigest()

        for user in cur.execute("SELECT emails FROM logins").fetchall():
            if user[0] == self.entry_user.get():
                correct_username = True

        for password in cur.execute("SELECT passwords FROM logins").fetchall():
            if password[0] == hash_password:
                correct_password = True

        if correct_password and correct_username:
            username = self.entry_user.get()
            self.label_eduboard.destroy()
            self.login_frame.destroy()
            Landing(self.master, username)

        else:
            if self.entry_pass.get() == "" and self.entry_user.get() == "":
                messagebox.showerror(
                    "EduBoard", """Cannot leave password and email empty. 
                    \nPlease try again or contact your administrator.""")

            elif self.entry_user.get() == "":
                messagebox.showerror(
                    "EduBoard", """Cannot leave email empty. 
                    \nPlease try again or contact your administrator.""")

            elif self.entry_pass.get() == "":
                messagebox.showerror(
                    "EduBoard", """Cannot leave password empty. 
                    \nPlease try again or contact your administrator.""")

            else:
                messagebox.showerror(
                    "EduBoard", """Wrong email or password. 
                    \nPlease try again or contact your administrator.""")


class CreateUser:
    '''Continues the current Tk() instance replacing with a UI 
    that allows admins to create new user for EduBoard'''

    def __init__(self, master, user):
        self.user = user
        self.master = master
        master.title("EduBoard - Signup")

        self.eduboard = Label(self.master,
                              text="EduBoard",
                              font=("Quicksand Bold", 48),
                              bg='#0079b5')
        self.eduboard.grid(column=4, row=0, sticky='n')

        self.login_frame = LabelFrame(self.master,
                                      text="Create User",
                                      font=("Quicksand Bold", 36),
                                      labelanchor='n',
                                      bg='#0079b5')
        self.login_frame.grid(column=4, row=1, sticky='n')
        self.login_frame.columnconfigure(2, weight=1)

        self.label_user = Label(self.login_frame,
                                text="Email",
                                justify='center',
                                bg='#0079b5',
                                font=("Quicksand Bold", 12))
        self.label_user.grid(column=2, row=2)

        self.entry_user = Entry(self.login_frame,
                                justify='center',
                                width=24)
        self.entry_user.grid(column=2, row=3)

        self.label_pass = Label(
            self.login_frame,
            text="Password",
            bg='#0079b5',
            font=("Quicksand Bold", 12))
        self.label_pass.grid(column=2, row=4)

        self.entry_pass = Entry(self.login_frame,
                                show='*',
                                justify='center',
                                width=24)
        self.entry_pass.grid(column=2, row=5)

        self.button_signup = Button(self.login_frame,
                                    text="Create",
                                    command=self.create_account,
                                    bg='#0079b5',
                                    font=("Quicksand Bold", 12),
                                    bd=0)
        self.button_signup.grid(column=2, row=6)

        self.button_admin_page = Button(
            self.master, text="Go Back",
            command=self.admin_page,
            bd=0,
            bg='#0079b5',
            font=("Quicksand Bold", 12))
        self.button_admin_page.grid(row=4, pady=10, column=4)

    def create_account(self):
        '''Retrives self parameter from __init__: Creates new row in logins.db.
        Detects whether or not inputted strings are in logins.db
        Detects whether or not the "entry_pass" is == "entry_user."'''

        dup_email = False
        dup_password = False
        hash_password = hashlib.md5(self.entry_pass.get().encode()).hexdigest()

        for user in cur.execute("""SELECT emails
                                FROM logins""").fetchall():
            if user[0] == self.entry_user.get():
                dup_email = True

        if self.entry_pass.get() == self.entry_user.get():
            dup_password = True

        if dup_email:
            messagebox.showerror(
                'EduBoard',
                """An account with this email already exists. 
                \nPlease try again or contact your administrator.""")

        elif dup_password:
            messagebox.showerror(
                'Eduboard',
                """Password cannot be the same as username, 
                \nPlease try again or contact your administrator.""")

        elif self.entry_pass.get() == "" and self.entry_user.get() == "":
            messagebox.showerror(
                "EduBoard",
                """Cannot leave password and email empty. 
                \nPlease try again or contact your administrator.""")

        elif self.entry_user.get() == "":
            messagebox.showerror(
                "EduBoard",
                """Cannot leave email empty. 
                \nPlease try again or contact your administrator.""")

        elif self.entry_pass.get() == "":
            messagebox.showerror(
                "EduBoard", """Cannot leave password empty. 
                \nPlease try again or contact your administrator.""")

        else:
            cur.execute(f"""INSERT INTO logins VALUES
                            ('{self.entry_user.get()}', '{hash_password}', False)
                            """)
            con.commit()
            self.admin_page()
            messagebox.showinfo("EduBoard", "Successfully Created Account.")

    def admin_page(self):
        '''Retrives self parameter from __init__.
        Destroys all widgets in the __init__ method'''
        self.login_frame.destroy()
        self.button_admin_page.destroy()
        self.eduboard.destroy()
        Admin(self.master, self.user)


class Landing:
    '''Continues current Tk() instance and replaces widgets with a UI
    that allows user to navigate features of EduBoard'''

    def __init__(self, master, user):

        self.user = user
        self.master = master

        self.master.configure(bg='#0079b5')
        self.master.title("EduBoard - Main")

        self.label_eduboard = Label(self.master,
                                    text="EduBoard",
                                    font=("Quicksand Bold", 48),
                                    bg='#0079b5')
        self.label_eduboard.grid(row=0)

        self.label_username = Label(self.master,
                                    text=f"{user}",
                                    font=("Quicksand Bold", 38),
                                    bg='#0079b5')
        self.label_username.grid(column=6, row=0)

        self.frame_functions = Frame(self.master,
                                     bg='#0079b5',
                                     bd=0)
        self.frame_functions.grid(row=1, column=3, padx=180)

        self.frame_functions.columnconfigure(0, weight=1)
        self.frame_functions.rowconfigure(3, weight=1)

        self.button_attendance = Button(self.frame_functions,
                                        text="Attendance",
                                        width=15,
                                        height=1,
                                        font=("Quicksand Bold", 18),
                                        bg='#0079b5',
                                        pady=5,
                                        command=self.attendance)
        self.button_attendance.grid(row=0, column=0, pady=10)

        self.button_lookup = Button(self.frame_functions,
                                    text="Lookup",
                                    width=15,
                                    height=1,
                                    font=("Quicksand Bold", 18),
                                    bg='#0079b5',
                                    pady=5)
        self.button_lookup.grid(row=1, column=0, pady=10)

        self.button_reports = Button(self.frame_functions,
                                     text="Reports", width=15, height=1, font=(
                                         "Quicksand Bold", 18), bg='#0079b5', pady=5)
        self.button_reports.grid(row=2, column=0, pady=10)

        self.button_settings = Button(self.frame_functions,
                                      text='Settings',
                                      width=15,
                                      height=1,
                                      font=("Quicksand Bold", 18),
                                      bg='#0079b5',
                                      pady=5,
                                      command=self.settings_page)
        self.button_settings.grid(row=3, column=0, pady=10)

        self.button_logout = Button(self.master,
                                    text="Logout",
                                    command=self.login_page,
                                    font=("Quicksand Bold", 18),
                                    bg='#0079b5')
        self.button_logout.grid(row=7, column=0)

        self.button_help = Button(self.master,
                                  text="Help",
                                  command=self.help_menu,
                                  font=("Quicksand Bold", 18),
                                  bg='#0079b5')
        self.button_help.grid(row=7, column=6)

    def login_page(self):
        '''Retrives self parameter from __init__. 
        Destroys Tk() master instance and starts a new one'''

        self.master.destroy()
        main()

    def settings_page(self):
        '''Retrives self parameter from __init__.
        Destroys all widgets in the __init__ method'''

        self.label_eduboard.destroy()
        self.frame_functions.destroy()
        self.button_logout.destroy()
        self.button_help.destroy()
        AdminLogin(self.master, self.user)

    def help_menu(self):
        '''Retrives self parameter from __init__.
        Opens "Help" screen via TopLevel'''
        help = Toplevel(self.master)

    def attendance(self):
        '''Retrives self parameter from __init__.
        Destroys all widgets in the __init__ method and runs "Attendance Selection"'''
        self.label_eduboard.destroy()
        self.label_username.destroy()
        self.frame_functions.destroy()
        AttendanceSelection(self.master, self.user)


class AdminLogin:
    '''Continues Tk() instance replacing widgets that allows users
    to login into the administrator. If the user succesfully logs in,
    the administrator row for the users changes to True in logins.db '''

    def __init__(self, master, user):
        self.user = user
        self.master = master
        self.master.title("EduBoard - Admin")

        self.label_eduboard = Label(self.master,
                                    text="EduBoard",
                                    font=("Quicksand Bold", 48),
                                    bg='#0079b5')
        self.label_eduboard.grid(column=4, row=0, padx=240)

        self.frame_admin = Frame(self.master,
                                 bg='#0079b5',
                                 bd=0)
        self.frame_admin.grid(column=4, row=1, padx=120)

        self.button_back = Button(self.frame_admin,
                                  text="Go Back",
                                  command=self.go_back,
                                  font=("Quicksand Bold", 18),
                                  bg='#0079b5')
        self.button_back.grid(row=3, column=3)

        if cur.execute(f"""SELECT administrator
                       FROM logins 
                       WHERE emails = '{self.user}'""").fetchone()[0] is False:
            self.label_admin_password = Label(self.frame_admin,
                                              text="Enter administrator password.",
                                              font=("Quicksand Bold", 12),
                                              bg='#0079b5')
            self.label_admin_password.grid(column=3, row=0)

            self.entry_admin = Entry(self.frame_admin,
                                     show='*',
                                     justify='center',
                                     width=24,
                                     bg='#0079b5')
            self.entry_admin.grid(column=3, row=1)

            self.button_login = Button(self.frame_admin,
                                       text="Login",
                                       bd=0,
                                       bg='#0079b5',
                                       command=self.validate_password)
            self.button_login.grid(column=3, row=2)

        else:
            self.admin_page()

    def go_back(self):
        '''Retrives self parameter from __init__.
        Deletes all widgets then runs "Landing" Class'''

        self.frame_admin.destroy()
        self.label_eduboard.destroy()
        Landing(self.master, self.user)

    def validate_password(self):
        '''Retrives self parameter from __init__.
        Validates whether or not self.entry_admin.get() is 123'''

        if self.entry_admin.get() == "123":
            self.admin_page()

        else:
            messagebox.showerror(
                "EduBoard", """Wrong password. 
                \nPlease try again or contact your administrator.""")

    def admin_page(self):
        '''Retrives self parameter from __init__.
        Check whether or not the user who inputed the password correctly
        is already an administrator, if they aren't their administrator column 
        is updated to True'''
        if cur.execute(f"""SELECT administrator
                       FROM logins 
                       WHERE emails = '{self.user}'""").fetchone()[0] is False:
            con.execute(f"""UPDATE logins
                            SET administrator = True
                            WHERE emails = '{self.user}'""")
            con.commit()

        self.label_eduboard.destroy()
        self.frame_admin.destroy()
        self.button_back.destroy()
        Admin(self.master, self.user)


class Admin:
    '''Continues previous instance of Tk() replacing widgets that allows users to
    Add more users (rows) to logins.db.
    Remove users from logins.db'''

    def __init__(self, master, user):
        self.user = user
        self.master = master

        self.label_eduboard = Label(self.master,
                                    text="EduBoard",
                                    font=("Quicksand Bold", 48),
                                    bg='#0079b5')
        self.label_eduboard.grid(column=4, row=0, sticky='N')

        self.frame_admin_tools = Frame(self.master,
                                       bg='#0079b5',
                                       bd=0,
                                       padx=180)
        self.frame_admin_tools.grid(column=4, row=1)

        self.button_create_user = Button(self.frame_admin_tools,
                                         text="Create User",
                                         bd=0,
                                         bg='#0079b5',
                                         font=("Quicksand Bold", 20),
                                         command=self.create_user)
        self.button_create_user.grid(column=3, row=0)

        self.button_create_student = Button(self.frame_admin_tools,
                                            text="Create Student",
                                            bd=0,
                                            font=("Quicksand Bold", 20),
                                            bg='#0079b5',
                                            command=self.add_student)
        self.button_create_student.grid(row=1, column=3)

        self.button_remove_user = Button(self.frame_admin_tools,
                                         text="Remove User",
                                         bd=0,
                                         bg='#0079b5',
                                         font=("Quicksand Bold", 20),
                                         command=self.remove_user)
        self.button_remove_user.grid(column=3, row=2)

        self.button_remove_student = Button(self.frame_admin_tools,
                                            text="Remove Student",
                                            bd=0,
                                            bg='#0079b5',
                                            font=("Quicksand Bold", 20),
                                            command=self.remove_student)
        self.button_remove_student.grid(column=3, row=3)

        self.button_back = Button(self.master, text="Return", command=self.go_back, font=(
            "Quicksand Bold", 12), bg='#0079b5')
        self.button_back.grid(column=4, row=2)

    def create_user(self):
        '''Retrives self parameter from __init__.
        Destroys all widgets in the __init__ method.
        Calls the CreateUser class.'''
        self.frame_admin_tools.destroy()
        self.label_eduboard.destroy()
        self.button_back.destroy()
        CreateUser(self.master, self.user)

    def remove_user(self):
        '''Retrives self parameter from __init__.
        Destroys all widgets in the __init__ method.
        Calls the Remove_User class.'''
        self.frame_admin_tools.destroy()
        self.button_back.destroy()
        self.label_eduboard.destroy()
        RemoveUser(self.master, self.user, False)

    def remove_student(self):
        '''Retrives self parameter from __init__.
        Destroys all widgets in the __init__ method.
        Calls the Remove_User class.'''
        self.frame_admin_tools.destroy()
        self.button_back.destroy()
        self.label_eduboard.destroy()
        RemoveUser(self.master, self.user, True)

    def add_student(self):
        '''Retrives self parameter from __init__.
        Destroys all widgets in the __init__ method.
        Calls the Add_Student class.
        The parameters given allow the list to reset and 
        allows for multiple intervals of the same function'''
        self.frame_admin_tools.destroy()
        self.button_back.destroy()
        self.label_eduboard.destroy()
        variable = IntVar(self.master)
        variable.set(1)
        details = []
        AddStudents(self.master, self.user, variable, True, details)

    def go_back(self):
        '''Retrives self parameter from __init__.
        Deletes all widgets then runs "Landing" Class'''
        self.frame_admin_tools.destroy()
        self.button_back.destroy()
        self.label_eduboard.destroy()
        Landing(self.master, self.user)


class AddStudents:
    def __init__(self, master, user, variable, new_instance, details):
        self.master = master
        self.user = user
        self.variable = variable
        self.details = details
        self.new_instance = new_instance

        if new_instance:
            figure = "Student"
        else:
            figure = "Guardian"

        self.label_eduboard = Label(master,
                                    text="EduBoard",
                                    font=("Quicksand Bold", 48),
                                    bg='#0079b5',
                                    justify="center")
        self.label_eduboard.grid(column=4, row=0, sticky='N')

        self.frame_details = LabelFrame(master,
                                        bg='#0079b5',
                                        bd=1,
                                        text=f"Add {figure}",
                                        font=("Quicksand Bold", 36))
        self.frame_details.grid(column=4, row=1)

        self.label_name = Label(self.frame_details,
                                bg='#0079b5',
                                font=("Quicksand Bold", 20),
                                text=f"{figure} Name*")
        self.label_name.grid(row=0, padx=85)

        self.entry_first_name = Entry(self.frame_details,
                                      bg='#0079b5',
                                      width=16)
        self.entry_first_name.grid(row=1)
        self.entry_first_name.insert(0, string="First Name")

        self.entry_last_name = Entry(self.frame_details,
                                     bg='#0079b5',
                                     width=16)
        self.entry_last_name.grid(row=2, padx=85)
        self.entry_last_name.insert(0, string="Last Name")

        if new_instance:
            self.label_year = Label(self.frame_details,
                                    bg='#0079b5',
                                    font=("Quicksand Bold", 12),
                                    text="Enter Year*")

            self.label_year.grid(row=3)

            self.entry_year = Entry(self.frame_details,
                                    bg='#0079b5',
                                    width=16)
            self.entry_year.grid(row=4)
            self.entry_year.insert(0, string="Year")

        self.label_dob = Label(self.frame_details,
                               bg='#0079b5',
                               font=("Quicksand Bold", 12),
                               text="Enter Date of Birth*")

        self.label_dob.grid(row=5)

        self.dateentry_dob = DateEntry(self.frame_details)
        self.dateentry_dob.grid(row=6)

        self.label_phnum = Label(self.frame_details,
                                 text=f"{figure} Phone Number",
                                 bg='#0079b5',
                                 font=("Quicksand Bold", 12))
        self.label_phnum.grid(row=7)

        self.entry_phnum = Entry(self.frame_details,
                                 width=20)
        self.entry_phnum.grid(row=8)
        if new_instance:
            self.label_amount_contact = Label(self.frame_details,
                                              text="Amount of Contacts",
                                              bg='#0079b5',
                                              font=("Quicksand Bold", 12))
            self.label_amount_contact.grid(row=9)

            self.openmenu_amount_contact = OptionMenu(self.frame_details,
                                                      variable,
                                                      *[1, 2, 3])
            self.openmenu_amount_contact.grid(row=10)

        self.button_next = Button(self.frame_details,
                                  bg='#0079b5',
                                  font=("Quicksand Bold", 12),
                                  text="Next",
                                  command=self.save_details)
        self.button_next.grid(row=11)

        self.button_go_back = Button(self.master,
                                     bg='#0079b5',
                                     font=("Quicksand Bold", 12),
                                     text="Back",
                                     command=self.go_back)
        self.button_go_back.grid(row=3, column=4, pady=10)

    def save_details(self):
        if self.entry_first_name.get() == "First Name":
            messagebox.showerror("EduBoard", "Please enter a first name")
            self.frame_details.destroy()
            self.label_eduboard.destroy()
            self.button_go_back.destroy()
            self.__init__(self.master, self.user, self.variable, self.new_instance, self.details)
        if self.entry_last_name.get() == "Last Name":
            messagebox.showerror("EduBoard", "Please enter a last name")
            self.frame_details.destroy()
            self.label_eduboard.destroy()
            self.button_go_back.destroy()
            self.__init__(self.master, self.user, self.variable, self.new_instance, self.details)
        if self.entry_phnum.get() == "":
            messagebox.showerror("EduBoard", "Please enter a phone number")
            self.frame_details.destroy()
            self.label_eduboard.destroy()
            self.button_go_back.destroy()
            self.__init__(self.master, self.user, self.variable, self.new_instance, self.details)
        if not isinstance(int(self.entry_phnum.get()), int) or len(self.entry_phnum.get()) < 9 or len(self.entry_phnum.get()) > 12:
            messagebox.showerror("EduBoard", """Please enter a valid phone number\n
                                 For example (022 1234 123)""")
            self.frame_details.destroy()
            self.label_eduboard.destroy()
            self.button_go_back.destroy()
            self.__init__(self.master, self.user, self.variable, self.new_instance, self.details)
        try:
            if self.entry_year.get() == "Year":
                messagebox.showerror("EduBoard", "Please enter a year")
                self.frame_details.destroy()
                self.label_eduboard.destroy()
                self.button_go_back.destroy()
                self.__init__(self.master, self.user, self.variable, self.new_instance, self.details)
            if not isinstance(int(self.entry_year.get()),int):
                messagebox.showerror("""EduBoard", "Please enter a valid year\n
                                    For example (12)""")
                self.frame_details.destroy()
                self.label_eduboard.destroy()
                self.button_go_back.destroy()
                self.__init__(self.master, self.user, self.variable, self.new_instance, self.details)
            if int(self.entry_year.get()) < 9 or int(self.entry_year.get()) > 13:
                messagebox.showerror("EduBoard", "Please enter a year between 9 - 13")
                self.frame_details.destroy()
                self.label_eduboard.destroy()
                self.button_go_back.destroy()
                self.__init__(self.master, self.user, self.variable, self.new_instance, self.details)
        except TclError:
            pass
        id = random.randint(0, 10000)
        while cur_students.execute(f"SELECT id FROM students WHERE id = {id}").fetchall() is []:
            id = random.randint(0, 10000)
        if len(self.details) == 0:
            self.details.append(str(id))
            self.details.append(str(self.entry_year.get()))
        if len(self.details) > 1: # Adds all details to self.details
            self.details.append(self.entry_first_name.get())
            self.details.append(self.entry_last_name.get())
            self.details.append(self.dateentry_dob.get())
            self.details.append(self.entry_phnum.get())
            if (self.variable.get() * 4 + 6) == len(self.details): # Appened None to details if there arent 3 guardians selected
                while len(self.details) is not 18:
                    self.details.append('None')
                cur_students.executemany(
                    "INSERT into students VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (self.details,))
                con_students.commit()
                messagebox.showinfo(
                    "EduBoard",
                    "Succesfully created Student.")
                self.go_back()
            else:
                self.frame_details.destroy()
                self.label_eduboard.destroy()
                self.button_go_back.destroy()
                self.__init__(self.master,
                              self.user,
                              self.variable,
                              False,
                              self.details)

    def go_back(self):
        '''Retrives self parameter from __init__.
        Deletes all widgets then runs "Landing" Class'''
        self.frame_details.destroy()
        self.button_go_back.destroy()
        self.label_eduboard.destroy()
        Admin(self.master, self.user)


class RemoveUser:
    '''Continues previous instance of Tk() replacing widgets that allows users to
    Remove users from logins.db, checks whether or not the user is an admistrator
    if so, it wont be allowed to administrators from the logins.db'''

    def __init__(self, master, user, student):
        self.label_username = user
        self.master = master
        self.student = student

        self.frame_table = Frame(master, bd=0, bg='#0079b5')
        self.frame_table.grid(column=4, row=1)
        self.frame_table.columnconfigure(1, weight=1)

        self.label_eduboard = Label(master,
                                    text="EduBoard",
                                    font=("Quicksand Bold", 48),
                                    bg='#0079b5')
        self.label_eduboard.grid(column=4, row=0,)

        if student:
            entity = "Student"
            self.treeview_entities = ttk.Treeview(self.frame_table,
                                                  columns=(
                                                      "ID", "Year", "First_Name", "Surname"),
                                                  show="headings")
            self.treeview_entities.heading('ID', text="ID")
            self.treeview_entities.column("ID", anchor=CENTER, width=40)
            self.treeview_entities.heading('Year', text="Year")
            self.treeview_entities.column(
                "Year", anchor=CENTER, width=80)
            self.treeview_entities.heading('First_Name', text="First Name")
            self.treeview_entities.column(
                "First_Name", anchor=CENTER, width=80)
            self.treeview_entities.heading('Surname', text="Surname")
            self.treeview_entities.column("Surname", anchor=CENTER, width=80)

        else:
            self.treeview_entities = ttk.Treeview(self.frame_table,
                                                  columns="Emails",
                                                  show="headings")
            entity = "User"
            self.treeview_entities.heading('Emails', text=f"{entity}")
            self.treeview_entities.column("Emails", anchor=CENTER, width=180)

        self.refresh_table()
        self.treeview_entities.grid(row=1, column=0)

        self.scrollbar_users = Scrollbar(
            self.frame_table, orient=VERTICAL, command=self.delete_user)
        self.treeview_entities.configure(yscroll=self.scrollbar_users.set)
        self.scrollbar_users.grid(row=1, column=1, ipady=86)

        self.button_delete_user = Button(self.frame_table, text=f"Delete {entity}",
                                         command=self.delete_user,
                                         bd=0,
                                         bg='#0079b5',
                                         font=("Quicksand Bold", 20),)
        self.button_delete_user.grid(row=2, column=0)
        self.button_back = Button(self.frame_table,
                                  text="Return",
                                  command=self.go_back,
                                  font=("Quicksand Bold", 12),
                                  bg='#0079b5')
        self.button_back.grid(column=0, row=3)

    def delete_user(self):
        '''Iterates through every selected row and removes them from 
        logins.db'''
        if self.student:
            for i in self.treeview_entities.selection():
                failed = False
                users = self.treeview_entities.item(i)
                id = users["values"][0]
                cur_students.execute(f"""DELETE FROM students
                            WHERE id = '{id}'""")
                con_students.commit()
            if failed is False:
                messagebox.showinfo(
                    "EduBoard", "Successfully Deleted Student(s).")
                self.refresh_table()
        else:
            for i in self.treeview_entities.selection():
                failed = False
                users = self.treeview_entities.item(i)
                user = users["values"][0]
                cur.execute(f"""DELETE FROM logins
                            WHERE emails = '{user}'""")
                con.commit()
            if failed is False:
                messagebox.showinfo(
                    "EduBoard", "Successfully Deleted User(s).")
                self.refresh_table()

    def refresh_table(self):
        '''Retrives self parameter from __init__.
        Iterates through logins.db then displays all rows in the email colomn
        into treeview_entities'''
        if self.student:
            student_data = cur_students.execute(
                "SELECT id, year, first_name, last_name  FROM students ")
            for i in self.treeview_entities.get_children():
                self.treeview_entities.delete(i)
            for student in student_data:
                self.treeview_entities.insert("", END, values=student)
        else:
            users_list = cur.execute(
                """SELECT emails FROM logins 
                WHERE administrator = False""").fetchall()
            for i in self.treeview_entities.get_children():
                self.treeview_entities.delete(i)
            for user in users_list:
                self.treeview_entities.insert('', END, values=user)

    def go_back(self):
        '''Retrives self parameter from __init__.
        Deletes all widgets then runs "Admin" Class'''
        self.frame_table.destroy()
        self.label_eduboard.destroy()
        Admin(self.master, self.label_username)


class AttendanceSelection:
    '''Continues previous instance of Tk() replacing widgets that allows users to
    Configure classes.
    Create Classes
    And take classes attendance'''

    def __init__(self, master, user):
        self.master = master
        self.user = user
        master.title("EduBoard - Attendance")
        self.label_eduboard = Label(master,
                                    text="EduBoard",
                                    font=("Quicksand Bold", 48),
                                    bg='#0079b5')
        self.label_eduboard.grid(column=4, row=0,)

        self.frame_functions = Frame(master,
                                     bg='#0079b5',
                                     bd=0)
        self.frame_functions.grid(column=4, row=1)

        button_take_attendance = Button(self.frame_functions,
                                        text="Take Attendance",
                                        bd=0,
                                        bg='#0079b5',
                                        font=("Quicksand Bold", 20),
                                        command=self.take_attendance)
        button_take_attendance.grid(column=4, row=0)

        if cur.execute(f"""SELECT administrator
                       FROM logins
                       WHERE emails = '{self.user}'""").fetchone()[0] == True:
            button_create_class = Button(self.frame_functions,
                                         text="Create Class",
                                         bd=0,
                                         bg='#0079b5',
                                         font=("Quicksand Bold", 20),
                                         command=self.create_class)
            button_create_class.grid(row=1, column=4)

            button_configure_class = Button(self.frame_functions,
                                            text="Configure Class",
                                            bd=0,
                                            bg='#0079b5',
                                            font=("Quicksand Bold", 20))
            button_configure_class.grid(column=4, row=2)

        self.button_back = Button(self.frame_functions,
                                  text="Go Back",
                                  command=self.go_back,
                                  font=("Quicksand Bold", 18),
                                  bg='#0079b5')
        self.button_back.grid(column=4, row=3)

    def create_class(self):
        self.label_eduboard.destroy()
        self.frame_functions.destroy()
        CreateClass(self.master, self.user)

    def take_attendance(self):
        self.label_eduboard.destroy()
        self.frame_functions.destroy()
        Attendance(self.master, self.user)

    def go_back(self):
        '''Retrives self parameter from __init__.
        Deletes all widgets then runs "Landing" Class passing the master
        and user parameters.'''
        self.label_eduboard.destroy()
        self.frame_functions.destroy()
        Landing(self.master, self.user)


class Attendance:
    """Allows users to take attendance for a class."""
    # peg

    def __init__(self, master, user):
        self.master = master
        self.user = user
        master.title("EduBoard - Attendance")
        self.label_eduboard = Label(master,
                                    text="EduBoard",
                                    font=("Quicksand Bold", 48),
                                    bg='#0079b5')
        self.label_eduboard.grid(column=4, row=0)

        self.frame_functions = Frame(self.master, bd=0, bg='#0079b5')

        print(cur_classes.execute("""SELECT name FROM sqlite_master  
        WHERE type='table';""").fetchall())
        self.treeview_classes = ttk.Treeview(self.frame_functions,
                                             columns=("Classes"),
                                             show="headings")
        self.treeview_classes.heading('Classes', text="Classes")
        self.treeview_classes.column(
            "Classes", anchor=CENTER, width=40)
        for cl in cur_classes.execute("""SELECT name FROM sqlite_master  
        WHERE type='table';""").fetchall():
            self.treeview_classes.insert(
                "", END, values=cl)
        self.treeview_classes.grid(ipadx=86)
        self.button_take_attendance = Button(self.frame_functions,
                                             text="Select Class",
                                             bd=1,
                                             bg='#0079b5',
                                             font=("Quicksand Bold", 20),
                                             command=self.take_attendance)
        self.button_take_attendance.grid(row=1)
        self.button_go_back = Button(self.frame_functions,
                                     text="Go Back",
                                     bd=1, bg='#0079b5',
                                     font=("Quicksand Bold", 18),
                                     command=self.go_back)
        self.button_go_back.grid(row=2)
        self.frame_functions.grid(row=1, column=4)

    def take_attendance(self):
        self.buttons = list()
        student_list = list()
        class_selected = self.treeview_classes.item(
            self.treeview_classes.selection())
        class_select = class_selected['values'][0]
        self.frame_functions.destroy()
        ids = list(map(lambda x: x[0], cur_classes.execute(
            f'select * from {class_select}').description))
        ids.pop(0)
        for id in ids:
            students = cur_students.execute(
                f"SELECT year, first_name, last_name FROM students WHERE id = '{id}'").fetchall()
            student_list.append(students)
        self.frame_functions2 = Frame(self.master, bd=0, bg='#0079b5')
        self.frame_radio_buttons = Frame(self.master, bd=0, bg='#0079b5')
        self.treeview_students = ttk.Treeview(self.frame_functions2, columns=(
            "Year", "First Name", "Last Name"), show="headings")
        self.treeview_students.heading('Year', text="Year")
        self.treeview_students.column(
            "Year", anchor=CENTER, width=40)
        self.treeview_students.heading('First Name', text="First Name")
        self.treeview_students.column(
            "First Name", anchor=CENTER, width=40)
        self.treeview_students.heading('Last Name', text="Last Name")
        self.treeview_students.column(
            "Last Name", anchor=CENTER, width=40)
        for student in student_list:
            self.treeview_students.insert(
                "", END, values=student[0])
            
        attendance_options = {"P": "1",
                              "L": "2",
                              "U": "3",
                              "J": "4",
                              "O": "5"}
        posy = 0
        posx = 0
        self.frame_functions2.rowconfigure(30)

        for students in range(len(student_list)):
            for (text, mode) in attendance_options.items():
                posx += 1
                self.buttons.append(StringVar(value=""))
                self.buttons.append(Radiobutton(self.frame_radio_buttons, padx=10, font=(
                    'arial', 10, ), bd=4, text=text, variable=self.buttons[-1], value=mode, bg="#0079b5"))
                # Adds radiobuttons to a list to be easily accessed
                self.buttons[-1].grid(row=posy,
                                      column=posx)
                if len(self.buttons) % 10 == 0:  # Checks if it is a new row of radio buttons
                    posy += 1
                    posx = 0

        self.treeview_students.grid(ipadx=43,row=0)
        self.frame_functions2.grid(row=1, column=4)
        self.frame_radio_buttons.grid(row=1,column=4,sticky="NE")

    def go_back(self):
        '''Retrives self parameter from __init__.
        Deletes all widgets then runs "AttendanceSelection" Class passing the master
        and user parameters.'''
        self.label_eduboard.destroy()
        self.frame_functions.destroy()
        AttendanceSelection(self.master, self.user)


class ConfigureClass:
    def __init__(self, master):
        pass


class CreateClass:
    def __init__(self, master, user):
        self.master = master
        self.user = user
        student_list = list()
        self.student_list = student_list

        self.label_eduboard = Label(master,
                                    text="EduBoard",
                                    font=("Quicksand Bold", 48),
                                    bg='#0079b5')
        self.label_eduboard.grid(column=4, row=0,)

        self.frame_functions = Frame(self.master,
                                     bg='#0079b5',
                                     bd=0)
        self.frame_functions.grid(column=4, row=1)

        self.label_class_name = Label(self.frame_functions,
                                      font=("Quicksand Bold", 24),
                                      bg='#0079b5',
                                      text="Class Name")
        self.label_class_name.grid(row=0)

        self.entry_class_name = Entry(self.frame_functions,
                                      font=("Quicksand Bold", 12),
                                      width=18)
        self.entry_class_name.grid(row=1)

        self.label_year_level = Label(self.frame_functions,
                                      font=("Quicksand Bold", 24),
                                      bg='#0079b5',
                                      text="Year Level")
        self.label_year_level.grid(row=2)

        self.entry_year_level = Entry(self.frame_functions,
                                      font=("Quicksand Bold", 12),
                                      width=18)
        self.entry_year_level.grid(row=3)

        self.button_select_students = Button(self.frame_functions,
                                             text="Select Students",
                                             bd=1,
                                             bg='#0079b5',
                                             font=("Quicksand Bold", 20),
                                             command=self.select_students)
        self.button_select_students.grid(row=4, pady=20)

        self.button_back = Button(self.frame_functions,
                                  text="Go Back",
                                  command=self.go_back,
                                  font=("Quicksand Bold", 18),
                                  bg='#0079b5')
        self.button_back.grid(row=5)
        self.frame_functions2 = Frame(self.master,
                                      bd=0,
                                      bg='#0079b5')
        self.treeview_students_avaliable = ttk.Treeview(self.frame_functions2,
                                                        columns=(
                                                            "ID", 'Year', "First_Name", "Surname"),
                                                        show="headings")
        self.treeview_students_unavaliable = ttk.Treeview(self.frame_functions2,
                                                          columns=(
                                                              "ID", "Year", "First_Name", "Surname"),
                                                          show="headings")
        self.button_move_students = Button(self.frame_functions2,
                                           text="Move Student",
                                           bd=0,
                                           bg='#0079b5',
                                           font=("Quicksand Bold", 20),
                                           command=self.move_student)

        self.button_move_students2 = Button(self.frame_functions2,
                                            text="Move Student",
                                            bd=0,
                                            bg='#0079b5',
                                            font=("Quicksand Bold", 20),
                                            command=self.move_student2)
        self.button_back = Button(self.frame_functions2,
                                  text="Go Back",
                                  command=self.go_back,
                                  font=("Quicksand Bold", 18),
                                  bg='#0079b5')
        self.button_create_class = Button(self.frame_functions2,
                                          text="Create Class",
                                          command=self.create_class,
                                          font=("Quicksand Bold", 18),
                                          bg='#0079b5')

    def select_students(self):
        '''Retrives self parameter from __init__.
        Deletes all widgets then runs "AttendanceSelection" Class passing the master
        and user parameters.'''
        if self.entry_class_name.get() == "":
            messagebox.showinfo("EduBoard", "Please give the class a name")
            self.frame_functions.destroy()
            self.label_eduboard.destroy()
            self.__init__(self.master, self.user)
        else:
            avaliable = cur_students.execute(
                f"SELECT id, year ,first_name,last_name FROM students where year = '{self.entry_year_level.get()}'").fetchall()
            self.avaliable_list = list()
            for row in avaliable:
                self.avaliable_list.append(row)
            self.class_name = self.entry_class_name.get()
            self.class_year_level = self.entry_year_level.get()
            self.frame_functions.destroy()

            self.treeview_students_avaliable.heading('ID', text="ID")
            self.treeview_students_avaliable.column(
                "ID", anchor=CENTER, width=40)
            self.treeview_students_avaliable.heading('Year', text="Year")
            self.treeview_students_avaliable.column(
                "Year", anchor=CENTER, width=80)
            self.treeview_students_avaliable.heading(
                'First_Name', text="First_Name")
            self.treeview_students_avaliable.column(
                "First_Name", anchor=CENTER, width=80)
            self.treeview_students_avaliable.heading('Surname', text="Surname")
            self.treeview_students_avaliable.column(
                "Surname", anchor=CENTER, width=80)

            self.treeview_students_avaliable.grid(row=0)

            self.insert_values()

            self.treeview_students_unavaliable.heading('ID', text="ID")
            self.treeview_students_unavaliable.column(
                "ID", anchor=CENTER, width=40)
            self.treeview_students_unavaliable.heading('Year', text="Year")
            self.treeview_students_unavaliable.column(
                "Year", anchor=CENTER, width=40)
            self.treeview_students_unavaliable.heading(
                'First_Name', text="First Name")
            self.treeview_students_unavaliable.column(
                "First_Name", anchor=CENTER, width=80)
            self.treeview_students_unavaliable.heading(
                'Surname', text="Surname")
            self.treeview_students_unavaliable.column(
                "Surname", anchor=CENTER, width=80)
            self.treeview_students_unavaliable.grid(row=0, column=1)
            self.button_back.grid(row=2)
            self.button_move_students.grid(row=1)
            self.button_move_students2.grid(row=1, column=1)
            self.button_create_class.grid(row=3)
            self.frame_functions2.grid(column=4, row=1)

    def insert_values(self):
        for i in self.treeview_students_avaliable.get_children():
            self.treeview_students_avaliable.delete(i)
        for student in self.avaliable_list:
            self.treeview_students_avaliable.insert(
                "", END, values=student)
            if student in self.student_list:
                self.student_list.remove(student)
                self.refresh_avaliablity()

    def refresh_avaliablity(self):
        for i in self.treeview_students_unavaliable.get_children():
            self.treeview_students_unavaliable.delete(i)
        for student in self.student_list:
            self.treeview_students_unavaliable.insert(
                "", END, values=student)
            if student in self.avaliable_list:
                self.avaliable_list.remove(student)
                self.insert_values()

    def move_student(self):
        for s in self.treeview_students_avaliable.selection():
            student = self.treeview_students_avaliable.item(s)['values']
            if (f'{student[0]}', student[1], student[2], student[3]) not in self.student_list:
                self.student_list.append(
                    (f'{student[0]}', f'{student[1]}', student[2], student[3]))
                self.refresh_avaliablity()

    def move_student2(self):
        for s in self.treeview_students_unavaliable.selection():
            student = self.treeview_students_unavaliable.item(s)['values']
            if (f'{student[0]}', student[1], student[2], student[3]) not in self.avaliable_list:
                self.avaliable_list.append(
                    (f'{student[0]}', f'{student[1]}', student[2], student[3]))
                self.insert_values()

    def create_class(self):
        if self.student_list == []:
            messagebox.showerror(
                "EduBoard", "Please add students to the class.")
        else:
            class_name = f'{self.class_name}_{self.class_year_level}_{datetime.date.today().year}'
            student_id = []
            for stu in self.student_list:
                student_id.append(stu[0])
            cur_classes.execute(
                f"""CREATE TABLE IF NOT EXISTS 
                '{class_name}'('{self.user}')""")
            for id in student_id:
                cur_classes.execute(f"""ALTER TABLE '{class_name}'
                                    ADD '{id}'""")
            con_classes.commit()
            messagebox.showinfo("EduBoard", "Succesfully created class.")
            self.go_back()

    def go_back(self):
        '''Retrives self parameter from __init__.
        Deletes all widgets then runs "AttendanceSelection" Class passing the master
        and user parameters.'''
        self.label_eduboard.destroy()
        self.frame_functions.destroy()
        self.frame_functions2.destroy()
        AttendanceSelection(self.master, self.user)


def main():
    '''Only runs the code in this function.'''
    root = Tk()
    Login(root)
    root.mainloop()


if __name__ == '__main__':
    main()
