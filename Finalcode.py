# Project Link - https://github.com/Saransh-Jainbu/T-Sheduler
# I will try my best to add notes explaining every peice of code used
# Feel free to customize code based on your liking.

############################################################ Importing all Necessary Libraries #######################################################################################

# Make sure you pip install all the libraries before running the code 
# To pip install go to cmd and Enter pip install package_name
# No this is not chatgpt I am trying my best to write the code in such a way that anyone can understand this code
# I will explain all libraries while using them , so don't worry :)

import tkinter.ttk as ttk
from tkinter import *
import tkinter as tk
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime
from datetime import time
from PIL import Image, ImageTk  
from tkinter import messagebox

######################################################################################################################################################################################

# So first before Gui , I am creating Sql table to store all the tasks and data required for the program 
# The following code will create the table on its own if you are running the code for the first time :)

def create_tasks_table():
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT,
            description TEXT,
            datetime TEXT
        )
    ''')

    connection.commit()
    connection.close()

'''
Explaination of Code: 

=> So basically connection =.... creates sqlite3 database if one already doesn't exists.
=> A cursor is a pointer that allows Python code to execute SQL commands in a database.
=> The block of code Below it is an SQL command executed using the cursor's execute method. It creates a table named 'tasks' in the database. 
=> The table has the following columns:id,task_name,description,datetime
=> Commit and close just save the changes to the Sql Database and closes the connection

(Reminder - Its just me Saransh writting the code and No chatgpt is used in writing the code)

'''
###################################################################################################################################################################################

# Create the tkinter window
root = tk.Tk()
root.resizable(FALSE,FALSE)
root.title("Background Image Example")
root.geometry('1300x729+70+12')

# Load the background image
background_image_path = "Tsheduler (2).png"
background_image = Image.open(background_image_path)

# Create a label to display the background image
background_image = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

######################################################################################################################################################################################
#Just creating a function right now which will be used to reset the input boxes to default values , after user interactiob

def reset_fields():
    # Reset task name
    task_name.set("Task Name")

    # Reset description
    discription.set("Task Description .....")

    # Reset date to the current date
    cal.set_date(datetime.now())

    time_entry.delete(0, "end")
    time_entry.insert(0, "Task Time (HH:MM)")


#######################################################################################################################################################################################

    '''
    Explaination of the code until line seperation:
    
    => So basically here I am trying to keep my code logic clean and trying to avoid wrong inputs by user
    => The above code will try to split hour and minute first and then will try to convert it into HH:MM format
    => If the code is not in the format it will just send a pop up error stating wrong format 
    => Rest Sql connection part is same , we will open connection ,update time and date input to database and then commit and close the databse

    *Special Note- Yeah I am writing all this comments manually , Not at all Ai generated comments*
    
    '''

    # Okay Now creating a function to save the task with date and time 

def save_task():

    create_tasks_table()  # Create the table if it doesn't exist (Code Above Just Explained)

    # I will use the below variables to retrive values from input box soon :)
    task_name_value = task_name.get()
    description_value = discription.get()
    date_value = cal.get_date()
    time_value = time_entry.get()  

   
    if task_name_value == "Task Name":
        messagebox.showerror("Error", "Please enter a valid task name.")
        return  
    
    # So here we simply used message box which we imported from tkinter to deafault Error

    try:
        time_parts = time_value.split(':')
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        time_object = time(hour, minute)
    except ValueError:
        messagebox.showerror("Error", "Invalid time format. Please use HH:MM.")
        return

    datetime_value = datetime.combine(date_value, time_object)
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tasks (task_name, description, datetime) VALUES (?, ?, ?)",
                   (task_name_value, description_value, str(datetime_value)))
    connection.commit()
    connection.close()
    reset_fields()

    
##################################################################################################################################################################################
'''
Its The part of Code where I spent my most time , I will simply breakdown what happens here:

=>Database Connection: It connects to the SQLite database named "tasks.db" where task information is stored.
=>Date Retrieval: It gets the date selected by the user from the DateEntry widget. This is the date for which tasks will be displayed.
=>Task Retrieval: It fetches tasks from the database that have a datetime matching the selected date.
=>Display Update: Clears the existing tasks in the display area and inserts the tasks for the selected date.
=>Error Handling: It checks for any errors that might occur during this process, such as issues with the database, and shows an error message if needed.

In simpler terms, imagine opening your to-do list, checking tasks for a specific day, and updating the list accordingly. If something goes wrong, it lets you know.

'''


def show_tasks_for_date():
    try:
        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()
        selected_date = cal_selected_date.get_date() # Retrieve selected date from the DateEntry widget
        selected_date_tasks = cursor.execute("SELECT * FROM tasks WHERE datetime LIKE ?", (f"{selected_date}%",)).fetchall()         # Retrieve tasks for the selected date
        connection.close()
        tasks_for_date_listbox.delete(0, tk.END)
        
        for task in selected_date_tasks:
            try:
                formatted_datetime = datetime.strptime(task[3], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_datetime = datetime.strptime(task[3], "%Y-%m-%d").strftime("%Y-%m-%d")

            tasks_for_date_listbox.insert(tk.END, f"{task[1]} - {task[2]} ({formatted_datetime})")

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error accessing the database: {str(e)}")

# Similarly creating Show upcoming task button

def show_upcoming_tasks():
    try:
        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()
        current_datetime = datetime.now().strftime("%Y-%m-%d 00:00")  # Start of the current day         # Retrieve upcoming tasks from the database (tasks with datetime greater than or equal to now)
        upcoming_tasks = cursor.execute("SELECT * FROM tasks WHERE datetime >= ?", (current_datetime,)).fetchall()
        connection.close()
        tasks_for_date_listbox.delete(0, tk.END)

        for task in upcoming_tasks:
            # Convert the datetime string to a more readable format
            formatted_datetime = datetime.strptime(task[3], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            tasks_for_date_listbox.insert(tk.END, f"{task[1]} - {task[2]} ({formatted_datetime})")

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error accessing the database: {str(e)}")

# Create a "Show Upcoming Tasks" button
show_upcoming_button = ttk.Button(root, text="Show Upcoming Tasks", command=show_upcoming_tasks)
show_upcoming_button.place(x=355, y=85, height=35, width=150)




####################################################################################################################################################################################

########################################## Add Task  #########################################################

def temp_text(e):
   task_entry.delete(0,"end")

#Creating string variable for storing task names
task_name=tk.StringVar()
ttk.Style().configure('pad.TEntry', padding='5 1 1 1',foreground='#808080')
# task entry using widget Entry
task_entry = ttk.Entry(root,textvariable = task_name , font=('Helvetica',16,'normal'),style='pad.TEntry')
task_entry.insert(0, "Task Name")

#placing the input box
task_entry.place(x=710,y=134,height=34,width=391 )
task_entry.bind("<FocusIn>", temp_text)

########################################## Add Discription #######################################################

def temp_text(e):
   discription_entry.delete(0,"end")

#Creating string variable for storing task discription
discription=tk.StringVar()
ttk.Style().configure('pad.TEntry', padding='5 1 1 1',foreground='#808080')
# task discription using widget Entry
discription_entry = ttk.Entry(root,textvariable = discription , font=('Helvetica',16,'normal'),style='pad.TEntry')
discription_entry.insert(0, "Task Discription .....")

#placing the input box
discription_entry.place(x=710,y=303,height=75,width=391 )
discription_entry.bind("<FocusIn>", temp_text)

################################### Create a label Date ############################################################

label = ttk.Label(root, text='Date', font=('Helvetica', 16), foreground='grey', background='white', relief='solid', borderwidth=2)
label.place(x=710, y=186, height=37, width=80)

# Create a frame to act as the background for the label
frame = tk.Frame(root, background='white')
frame.place(x=710, y=186, height=37, width=80)

# Center the text within the frame
label_text = tk.Label(frame, text='Date', font=('Helvetica', 16), foreground='grey', background='white')
label_text.pack(expand=True, fill='both', padx=10, pady=10)

################################# Add date ###########################################################################

cal = DateEntry(root, width=12, background='white', foreground='#808080', borderwidth=2, font=("Helvetica", 16),justify='center', date_pattern="dd/MM/yyyy")
cal.place(x=790, y=185, height=41, width=312)

# Function to retrieve the selected date
def get_selected_date():
    selected_date = cal.get_date()

############################################### Edit the selected task ###################################################

def edit_task():
    selected_task = tasks_for_date_listbox.curselection()

    if selected_task:
        selected_task_index = selected_task[0]
        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()
        
        # Retrieve the original task details
        original_task = cursor.execute("SELECT * FROM tasks").fetchall()[selected_task_index]
        original_task_id = original_task[0]

        edited_task_name = task_name.get()
        edited_description = discription.get()
        edited_date = cal.get_date()

        # Update the task in the database
        cursor.execute("UPDATE tasks SET task_name=?, description=?, datetime=? WHERE id=?",
                       (edited_task_name, edited_description, edited_date, original_task_id))

        connection.commit()
        connection.close()

        # Refresh the tasks list for the selected date
        show_tasks_for_date()
        reset_fields()

################################# Function to remove the selected task ##########################################################

def remove_task():
    selected_task = tasks_for_date_listbox.curselection()

    if selected_task:
        selected_task_index = selected_task[0]
        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()

        # Retrieve the original task details
        original_task = cursor.execute("SELECT * FROM tasks").fetchall()[selected_task_index]
        original_task_id = original_task[0]

        # Remove the task from the database
        cursor.execute("DELETE FROM tasks WHERE id=?", (original_task_id,))

        connection.commit()
        connection.close()

        # Refresh the tasks list for the selected date
        show_tasks_for_date()

########################################### Buttons ##################################################################

# Creating the "Save Task" button with an image
save_button = Button(root,text="Schedule", command=save_task,borderwidth=0, activebackground="#ed1c24",bg="#ed1c24",fg="white",font=("Helvetica",13,'bold'))
save_button.place(x=700, y=425, height=35, width=120)

# Creating an "Edit Task" button
edit_button = ttk.Button(root, text="Edit Task", command=edit_task)
edit_button.place(x=850, y=425, height=35, width=120)

# Creating a "Remove Task" button
remove_button = ttk.Button(root, text="Remove Task", command=remove_task)
remove_button.place(x=1000, y=425, height=35, width=120)

# Creating a DateEntry widget for selecting a specific date to view tasks
cal_selected_date = DateEntry(root, width=12, background='white', foreground='#8F8F8F', borderwidth=2,
                               font=("Helvetica", 12), justify='center', date_pattern="dd/MM/yyyy")
cal_selected_date.place(x=85, y=355, height=35, width=150)

#Creating a "Show task for date button"
show_tasks_for_date_button = ttk.Button(root, text="Show Tasks for Date", command=show_tasks_for_date)
show_tasks_for_date_button.place(x=335, y=355, height=35, width=150)

#Creating a listboc
tasks_for_date_listbox = tk.Listbox(root, font=('Helvetica', 12), selectbackground='#a6a6a6', selectforeground='black', height=10, width=50)
tasks_for_date_listbox.place(x=50, y=134)

# Create a "Show Upcoming Tasks" button
show_upcoming_button = ttk.Button(root, text="Show Upcoming Tasks", command=show_upcoming_tasks)
show_upcoming_button.place(x=355, y=85, height=35, width=150)

# Creating a time entry widget
time_entry_default = "Task Time (HH:MM)"
time_entry_var = tk.StringVar()
time_entry_var.set(time_entry_default)
time_entry = ttk.Entry(root, textvariable=time_entry_var, font=('Helvetica', 16, 'normal'), style='pad.TEntry')
time_entry.place(x=710, y=245, height=40, width=391)

# Handling the time entry click event
def handle_time_entry_click(event):
    if time_entry_var.get() == time_entry_default:
        time_entry_var.set("")  # Clear the default value when clicked

# Binding the click event to the time entry
time_entry.bind("<FocusIn>", handle_time_entry_click)


root.mainloop()
