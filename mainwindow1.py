from tkinter import PhotoImage
import ctypes
import tkinter.ttk as ttk
from tkinter import *
import tkinter as tk
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime
from PIL import Image, ImageTk, ImageFilter  # Import ImageFilter module
from tkinter import messagebox

###################################### SQL Database COnnection ##############################

def save_task():
    # Retrieve values from the input fields
    task_name_value = task_name.get()
    description_value = discription.get()
    date_value = cal.get_date()

    # Check if the task name is still the default value
    if task_name_value == "Task Name":
        # Display an error popup
        messagebox.showerror("Error", "Please enter a valid task name.")
        return  # Stop further execution if there's an error

    # Connect to the SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT,
            description TEXT,
            date TEXT
        )
    ''')

    # Insert the task details into the database
    cursor.execute("INSERT INTO tasks (task_name, description, date) VALUES (?, ?, ?)",
                   (task_name_value, description_value, date_value))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

    # Reset the input fields
    reset_fields()
################################ Reset Function ##############################

    reset_fields()

def reset_fields():
    # Reset task name
    task_name.set("Task Name")

    # Reset description
    discription.set("Task Discription .....")

    # Reset date
    cal.set_date(datetime.now())

#################################################################################

################################# Side Calendar #################################
def show_tasks_for_date():
    # Connect to the SQLite database
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    # Retrieve selected date from the DateEntry widget
    selected_date = cal_selected_date.get_date()

    # Retrieve tasks for the selected date
    selected_date_tasks = cursor.execute("SELECT * FROM tasks WHERE date = ?", (selected_date,)).fetchall()

    # Close the connection
    connection.close()

    # Clear existing items in the listbox
    tasks_for_date_listbox.delete(0, tk.END)

    # Insert data into the listbox
    for task in selected_date_tasks:
        tasks_for_date_listbox.insert(tk.END, f"{task[1]} - {task[2]} ({task[3]})")

########################################################################################

# Get the screen size
user32 = ctypes.windll.user32
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# Create the tkinter window
root = tk.Tk()
root.title("Background Image Example")

# Load the background image
background_image_path = "Tsheduler_bg.png"
background_image = Image.open(background_image_path)

# Scale the image to fit within the window size using the "BILINEAR" filter

image_width, image_height = background_image.size
scaling_factor = min(screen_width / image_width, screen_height / image_height)
image_width, image_height = int(image_width * scaling_factor), int(image_height * scaling_factor)
background_image = background_image.resize((image_width, image_height), Image.BILINEAR)
# Set the window size to match the screen size
root.geometry(f"{image_width}x{image_height}")

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
task_entry.place(x=932,y=168,height=44,width=515 )
task_entry.bind("<FocusIn>", temp_text)

########################################## Add Discription ##########################################################

def temp_text(e):
   discription_entry.delete(0,"end")

#Creating string variable for storing task discription
discription=tk.StringVar()
ttk.Style().configure('pad.TEntry', padding='5 1 1 1',foreground='#808080')
# task discription using widget Entry
discription_entry = ttk.Entry(root,textvariable = discription , font=('Helvetica',16,'normal'),style='pad.TEntry')
discription_entry.insert(0, "Task Discription .....")

#placing the input box
discription_entry.place(x=932,y=391,height=96,width=514 )
discription_entry.bind("<FocusIn>", temp_text)

################################# Add date ###########################################################################

cal = DateEntry(root, width=12, background='white', foreground='#808080', borderwidth=2, font=("Helvetica", 16),justify='center', date_pattern="dd/MM/yyyy")
cal.place(x=1030, y=235, height=54, width=418)

# Function to retrieve the selected date
def get_selected_date():
    selected_date = cal.get_date()

################################### Create a label Date ############################################################

label = ttk.Label(root, text='Date', font=('Helvetica', 16), foreground='grey', background='white', relief='solid', borderwidth=2)
label.place(x=932, y=236, height=52, width=97)

# Create a frame to act as the background for the label
frame = tk.Frame(root, background='white')
frame.place(x=932, y=236, height=52, width=97)

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
        cursor.execute("UPDATE tasks SET task_name=?, description=?, date=? WHERE id=?",
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


# Load the image for the button
image_path = r"shedule_button.png"
image = Image.open(image_path)

image = image.resize((150, 44))  # Use ImageFilter.ANTIALIAS
photo = ImageTk.PhotoImage(image)

# Create the "Save Task" button with an image
save_button = Button(root, image=photo, command=save_task,borderwidth=0, activebackground="#ed1c24")
save_button.image = photo  # Keep a reference to prevent garbage collection
save_button.place(x=930, y=500, height=35, width=145)


########################################################################################################

# Create an "Edit Task" button
edit_button = ttk.Button(root, text="Edit Task", command=edit_task)
edit_button.place(x=1120, y=500, height=35, width=145)

# Create a "Remove Task" button
remove_button = ttk.Button(root, text="Remove Task", command=remove_task)
remove_button.place(x=1300, y=500, height=35, width=145)

#######################################################################################################
# Create a DateEntry widget for selecting a specific date to view tasks
cal_selected_date = DateEntry(root, width=12, background='white', foreground='#8F8F8F', borderwidth=2,
                               font=("Helvetica", 12), justify='center', date_pattern="dd/MM/yyyy")
cal_selected_date.place(x=85, y=515, height=44, width=150)

################### Show Tasks for Date Button #########################################################

show_tasks_for_date_button = ttk.Button(root, text="Show Tasks for Date", command=show_tasks_for_date)
show_tasks_for_date_button.place(x=335


, y=515, height=46, width=150)

################ Create a Listbox to display tasks for a particular date ###############################

tasks_for_date_listbox = tk.Listbox(root, font=('Helvetica', 12), selectbackground='#a6a6a6', selectforeground='black', height=10, width=50)
tasks_for_date_listbox.place(x=50, y=300)

#########################################################################################################

# Run the tkinter main loop
root.mainloop()
