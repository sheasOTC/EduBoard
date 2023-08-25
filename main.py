from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
import hashlib
from tkcalendar import Calendar, DateEntry

# Connects to the logins.db
con = sqlite3.connect("datebases\logins.db")
cur = con.cursor()

try:
    open("datebases\logins.db", "x")
except FileExistsError:
    cur.execute("""CREATE TABLE IF NOT EXISTS
                logins(emails, passwords, administrator)""")
    con.commit()
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
                                         text="Remove Teacher or Student",
                                         bd=0,
                                         bg='#0079b5',
                                         font=("Quicksand Bold", 20),
                                         command=self.remove_user)
        self.button_remove_user.grid(column=3, row=2)

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
        RemoveUser(self.master, self.user)

    def add_student(self):
        '''Retrives self parameter from __init__.
        Destroys all widgets in the __init__ method.
        Calls the Remove_User class.'''
        self.frame_admin_tools.destroy()
        self.button_back.destroy()
        self.label_eduboard.destroy()
        AddStudents(self.master, self.user)

    def go_back(self):
        '''Retrives self parameter from __init__.
        Deletes all widgets then runs "Landing" Class'''
        self.frame_admin_tools.destroy()
        self.button_back.destroy()
        self.label_eduboard.destroy()
        Landing(self.master, self.user)


class AddStudents:
    def __init__(self, master, user):
        self.master = master
        self.user = user
        self.label_eduboard = Label(master,
                                    text="EduBoard",
                                    font=("Quicksand Bold", 48),
                                    bg='#0079b5')
        self.label_eduboard.grid(column=4, row=0, sticky='N')

        self.frame_details = LabelFrame(master,
                                        bg='#0079b5',
                                        bd=1,
                                        text="Add Student",
                                        font=("Quicksand Bold", 36))
        self.frame_details.grid(column=4, row=1)

        self.label_student_name = Label(self.frame_details,
                                        bg='#0079b5',
                                        font=("Quicksand Bold", 20),
                                        text="*Student Name")
        self.label_student_name.grid(row=0, column=1)

        self.entry_student_first_name = Entry(self.frame_details,
                                              bg='#0079b5',
                                              width=16)
        self.entry_student_first_name.grid(row=1)
        self.entry_student_first_name.insert(0, string="First Name")

        self.entry_student_last_name = Entry(self.frame_details,
                                             bg='#0079b5',
                                             width=16)
        self.entry_student_last_name.grid(row=1, column=0)
        self.entry_student_last_name.insert(0, string="Last Name")

        self.label_student_dob = Label(self.frame_details,
                                       bg='#0079b5',
                                       font=("Quicksand Bold", 12),
                                       text="Enter Date of Birth*")

        self.label_student_dob.grid(row=2)

        dateentry_student_dob = DateEntry(self.frame_details)
        dateentry_student_dob.grid(row=3)

        self.label_student_phnum = Label(self.frame_details,
                                         text="Student Phone Number",
                                         bg='#0079b5',
                                         font=("Quicksand Bold", 12))
        self.label_student_phnum.grid(row=4)

        self.entry_student_phnum


class RemoveUser:
    '''Continues previous instance of Tk() replacing widgets that allows users to
    Remove users from logins.db, checks whether or not the user is an admistrator
    if so, it wont be allowed to administrators from the logins.db'''

    def __init__(self, master, user):
        self.label_username = user
        self.master = master

        self.frame_table = Frame(master, bd=0, bg='#0079b5')
        self.frame_table.grid(column=4, row=1)
        self.frame_table.columnconfigure(1, weight=1)

        self.label_eduboard = Label(master,
                                    text="EduBoard",
                                    font=("Quicksand Bold", 48),
                                    bg='#0079b5')
        self.label_eduboard.grid(column=4, row=0,)

        self.treeview_emails = ttk.Treeview(self.frame_table,
                                            columns='Emails',
                                            show="headings")

        self.treeview_emails.heading('Emails', text="Email")
        self.treeview_emails.column("Emails", anchor=CENTER, width=180)
        self.refresh_table()
        self.treeview_emails.grid(row=1, column=0)

        self.scrollbar_users = Scrollbar(
            self.frame_table, orient=VERTICAL, command=self.delete_user)
        self.treeview_emails.configure(yscroll=self.scrollbar_users.set)
        self.scrollbar_users.grid(row=1, column=1, ipady=86)

        self.button_delete_user = Button(self.frame_table, text="Delete User",
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
        for i in self.treeview_emails.selection():
            failed = False
            users = self.treeview_emails.item(i)
            user = users["values"][0]
            cur.execute(f"""DELETE FROM logins
                        WHERE emails = '{user}'""")
            con.commit()
        if failed is False:
            messagebox.showinfo("EduBoard", "Successfully Deleted User(s).")
            self.refresh_table()

    def refresh_table(self):
        '''Retrives self parameter from __init__.
        Iterates through logins.db then displays all rows in the email colomn
        into treeview_emails'''
        users_list = cur.execute(
            """SELECT emails FROM logins 
            WHERE administrator = False""").fetchall()
        for i in self.treeview_emails.get_children():
            self.treeview_emails.delete(i)
        for user in users_list:
            self.treeview_emails.insert('', END, values=user)

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
                                        font=("Quicksand Bold", 20))
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

    def go_back(self):
        '''Retrives self parameter from __init__.
        Deletes all widgets then runs "Landing" Class passing the master
        and user parameters.'''
        self.label_eduboard.destroy()
        self.frame_functions.destroy()
        Landing(self.master, self.user)


class Attendance:
    """Allows users to take attendance for a class."""

    def __init__(self, master):
        pass


class ConfigureClass:
    def __init__(self, master):
        pass


class CreateClass:
    def __init__(self, master, user):
        self.master = master
        self.user = user
        conclasses = sqlite3.connect("datebases\classes.db")
        self.curclasses = conclasses.cursor()

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

        self.button_select_students = Button(self.frame_functions,
                                             text="Select Students",
                                             bd=1,
                                             bg='#0079b5',
                                             font=("Quicksand Bold", 20),
                                             command=self.select_students)
        self.button_select_students.grid(row=2, pady=20)

        self.button_back = Button(self.frame_functions,
                                  text="Go Back",
                                  command=self.go_back,
                                  font=("Quicksand Bold", 18),
                                  bg='#0079b5')
        self.button_back.grid(row=3)

    def select_students(self):
        '''Retrives self parameter from __init__.
        Deletes all widgets then runs "AttendanceSelection" Class passing the master
        and user parameters.'''
        self.frame_functions.destroy()
        for c in self.curclasses(""):
            pass
            # if self.entry_class_name.get() ==

    def go_back(self):
        '''Retrives self parameter from __init__.
        Deletes all widgets then runs "AttendanceSelection" Class passing the master
        and user parameters.'''
        self.label_eduboard.destroy()
        self.frame_functions.destroy()
        AttendanceSelection(self.master, self.user)


def main():
    '''Only runs the code in this function.'''
    root = Tk()
    Login(root)
    root.mainloop()


if __name__ == '__main__':
    main()
