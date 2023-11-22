import tkinter.ttk as ttk
from tkinter import *
import tkinter as tk
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime
from datetime import time
from PIL import Image, ImageTk  
from tkinter import messagebox

###################################### SQL Database COnnection ##############################


# Function to create the 'tasks' table if it doesn't exist
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

# Function to save the task with date and time
def save_task():
    create_tasks_table()  # Create the table if it doesn't exist

    # Retrieve values from the input fields
    task_name_value = task_name.get()
    description_value = discription.get()
    date_value = cal.get_date()
    time_value = time_entry.get()  # Get the time input

    # Check if the task name is still the default value
    if task_name_value == "Task Name":
        # Display an error popup
        messagebox.showerror("Error", "Please enter a valid task name.")
        return  # Stop further execution if there's an error

    # Convert time_value to datetime.time
    try:
        time_parts = time_value.split(':')
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        time_object = time(hour, minute)
    except ValueError:
        messagebox.showerror("Error", "Invalid time format. Please use HH:MM.")
        return

    # Combine date and time into a single datetime object
    datetime_value = datetime.combine(date_value, time_object)

    # Connect to the SQLite database
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    # Insert the task details into the database
    cursor.execute("INSERT INTO tasks (task_name, description, datetime) VALUES (?, ?, ?)",
                   (task_name_value, description_value, str(datetime_value)))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

    # Reset the input fields
    reset_fields()

################################ Reset Function ##############################

def reset_fields():
    # Reset task name
    task_name.set("Task Name")

    # Reset description
    discription.set("Task Description .....")

    # Reset date to the current date
    cal.set_date(datetime.now())

    # Reset time to the default text
    time_entry.delete(0, "end")
    time_entry.insert(0, "Task Time (HH:MM)")



#################################################################################

################################# Side Calendar #################################
def show_tasks_for_date():
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()

        # Retrieve selected date from the DateEntry widget
        selected_date = cal_selected_date.get_date()

        # Retrieve tasks for the selected date
        selected_date_tasks = cursor.execute("SELECT * FROM tasks WHERE datetime LIKE ?", (f"{selected_date}%",)).fetchall()

        # Close the connection
        connection.close()

        # Clear existing items in the listbox
        tasks_for_date_listbox.delete(0, tk.END)

        # Insert data into the listbox
        for task in selected_date_tasks:
            try:
                # Try to parse as date-time
                formatted_datetime = datetime.strptime(task[3], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                # If parsing as date-time fails, assume it's date-only
                formatted_datetime = datetime.strptime(task[3], "%Y-%m-%d").strftime("%Y-%m-%d")

            tasks_for_date_listbox.insert(tk.END, f"{task[1]} - {task[2]} ({formatted_datetime})")

    except sqlite3.Error as e:
        # Display an error message if there's an issue with the SQL query or database connection
        messagebox.showerror("Error", f"Error accessing the database: {str(e)}")





########################################################################################

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

################################# Add date ###########################################################################

cal = DateEntry(root, width=12, background='white', foreground='#808080', borderwidth=2, font=("Helvetica", 16),justify='center', date_pattern="dd/MM/yyyy")
cal.place(x=790, y=185, height=41, width=312)

# Function to retrieve the selected date
def get_selected_date():
    selected_date = cal.get_date()

################################### Create a label Date ############################################################

label = ttk.Label(root, text='Date', font=('Helvetica', 16), foreground='grey', background='white', relief='solid', borderwidth=2)
label.place(x=710, y=186, height=37, width=80)

# Create a frame to act as the background for the label
frame = tk.Frame(root, background='white')
frame.place(x=710, y=186, height=37, width=80)

# Center the text within the frame
label_text = tk.Label(frame, text='Date', font=('Helvetica', 16), foreground='grey', background='white')
label_text.pack(expand=True, fill='both', padx=10, pady=10)

##########################################################################################################################

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

#################################################################################################################################

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

########################################### Save Button ##################################################################

# Create the "Save Task" button with an image
save_button = Button(root,text="Schedule", command=save_task,borderwidth=0, activebackground="#ed1c24",bg="#ed1c24",fg="white",font=("Helvetica",13,'bold'))
#save_button.image = photo  # Keep a reference to prevent garbage collection
save_button.place(x=700, y=425, height=35, width=120)

# Create an "Edit Task" button
edit_button = ttk.Button(root, text="Edit Task", command=edit_task)
edit_button.place(x=850, y=425, height=35, width=120)

# Create a "Remove Task" button
remove_button = ttk.Button(root, text="Remove Task", command=remove_task)
remove_button.place(x=1000, y=425, height=35, width=120)

# Create a DateEntry widget for selecting a specific date to view tasks
cal_selected_date = DateEntry(root, width=12, background='white', foreground='#8F8F8F', borderwidth=2,
                               font=("Helvetica", 12), justify='center', date_pattern="dd/MM/yyyy")
cal_selected_date.place(x=85, y=355, height=35, width=150)

#Creating a "Show task for date button"
show_tasks_for_date_button = ttk.Button(root, text="Show Tasks for Date", command=show_tasks_for_date)
show_tasks_for_date_button.place(x=335, y=355, height=35, width=150)

#Creating a listboc
tasks_for_date_listbox = tk.Listbox(root, font=('Helvetica', 12), selectbackground='#a6a6a6', selectforeground='black', height=10, width=50)
tasks_for_date_listbox.place(x=50, y=134)

#########################################################################################################
# Add a time entry widget
time_entry = ttk.Entry(root, font=('Helvetica', 16, 'normal'), style='pad.TEntry')
time_entry.insert(0, "Task Time (HH:MM)")  # Default value
time_entry.place(x=710, y=245, height=40, width=391)
##################################### SHow all upcoming tasks #########################################
def show_upcoming_tasks():
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()

        # Retrieve upcoming tasks from the database (tasks with datetime greater than or equal to now)
        current_datetime = datetime.now().strftime("%Y-%m-%d 00:00")  # Start of the current day

        upcoming_tasks = cursor.execute("SELECT * FROM tasks WHERE datetime >= ?", (current_datetime,)).fetchall()

        # Close the connection
        connection.close()

        # Clear existing items in the listbox
        tasks_for_date_listbox.delete(0, tk.END)

        # Insert data into the listbox
        for task in upcoming_tasks:
            # Convert the datetime string to a more readable format
            formatted_datetime = datetime.strptime(task[3], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            tasks_for_date_listbox.insert(tk.END, f"{task[1]} - {task[2]} ({formatted_datetime})")

    except sqlite3.Error as e:
        # Display an error message if there's an issue with the SQL query or database connection
        messagebox.showerror("Error", f"Error accessing the database: {str(e)}")

# Create a "Show Upcoming Tasks" button
show_upcoming_button = ttk.Button(root, text="Show Upcoming Tasks", command=show_upcoming_tasks)
show_upcoming_button.place(x=355, y=85, height=35, width=150)

### Run the tkinter main loop
root.mainloop()
