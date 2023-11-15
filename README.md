# Python-project-
# Task Scheduler Application

This is a simple task scheduler application implemented using Tkinter in Python. The application allows users to input task details, including task name, description, and date. Tasks are stored in an SQLite database, and users can view tasks for a specific date.

## Getting Started

### Prerequisites

Make sure you have Python installed on your machine. You can install the required packages by running:

```bash
pip install tk tkcalendar pillow
```

### Running the Application

1. Clone the repository:

   ```bash
   git clone https://github.com/Saransh-Jainbu/Python-project-.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Python-project-
   ```

3. Run the application:

   ```bash
   python mainwindow1.py
   ```

## Application Features

### Task Input

- **Task Name:** Enter the name of the task in the provided input box.
- **Task Description:** Provide a description of the task in the designated input box.
- **Date Selection:** Use the date picker to select the date for the task.

### Save Task

- Click the "Save Task" button to save the entered task details to the SQLite database.

### Show Tasks for Date

- Select a date using the date picker.
- Click the "Show Tasks for Date" button to view tasks scheduled for the selected date.

### Reset Functionality

- The application provides a reset function that clears the input fields after saving a task.

## Background Image

The application features a background image loaded from the specified path. Adjustments are made to scale the image to fit the window size.

## Credits

Special thanks to @Anousha-Singh for helping me out with the project, without her I wouldn't be able to complete it up :)

## Additional Notes

- The application uses the `tkcalendar` library for the date picker and the `PIL` library for image processing.
- SQLite is used for database storage, and tasks are organized by task name, description, and date.

Feel free to explore and enhance the application based on your requirements. Enjoy task scheduling with this Tkinter-based application!
