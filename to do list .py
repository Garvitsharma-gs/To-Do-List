import tkinter as tk
from tkinter import messagebox
import json
import os

# File for saving tasks
TASKS_FILE = "tasks.json"


def save_tasks():
    """Save tasks to a file."""
    tasks = task_listbox.get(0, tk.END)
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

def load_tasks():
    """Load tasks from a file."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            tasks = json.load(file)
            for task in tasks:
                task_listbox.insert(tk.END, task)

def add_task():
    task = task_entry.get()
    if task.strip():
        # Add a numbered format to the task
        task_listbox.insert(tk.END, f"{task_listbox.size() + 1}. {task}")
        task_entry.delete(0, tk.END)
        save_tasks()
        messagebox.showinfo("Task Added", f"Task '{task}' added!")
    else:
        messagebox.showwarning("Input Error", "Task cannot be empty!")

def delete_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task = task_listbox.get(selected_task_index)
        task_listbox.delete(selected_task_index)
        update_task_numbering()
        save_tasks()
        messagebox.showinfo("Task Deleted", f"Task '{task.split('. ', 1)[1]}' deleted!")
    else:
        messagebox.showwarning("Selection Error", "Please select a task to delete!")

def clear_tasks():
    if messagebox.askyesno("Confirm", "Do you want to clear all tasks?"):
        task_listbox.delete(0, tk.END)
        save_tasks()

def update_task_numbering():
    """Update task numbering after adding or deleting a task."""
    tasks = [f"{index + 1}. {task.split('. ', 1)[1]}" for index, task in enumerate(task_listbox.get(0, tk.END))]
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, task)

def toggle_complete():
    """Toggle task completion status."""
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task = task_listbox.get(selected_task_index)
        task_listbox.delete(selected_task_index)
        if task.startswith("[X]"):
            task = task[3:]  # Remove completed mark
        else:
            task = "[X] " + task  # Mark as completed
        task_listbox.insert(tk.END, task)
        save_tasks()
        messagebox.showinfo("Task Status Updated", f"Task '{task.split('. ', 1)[1]}' marked as {'completed' if task.startswith('[X]') else 'incomplete'}!")
    else:
        messagebox.showwarning("Selection Error", "Please select a task to toggle its completion status!")

# Main application window
root = tk.Tk()
root.title("To-Do List")
root.geometry("550x600")  # Adjusted for better spacing and appearance
root.resizable(False, False)

# Set a new dark, elegant background color
root.config(bg="#1F1F2E")

# Motivational message with a sleek font and improved contrast
motivation_label = tk.Label(
    root,
    text="“Success is the sum of small efforts, repeated day in and day out.”",
    font=("Helvetica", 13, "italic"),
    fg="#D9E4F5",
    bg="#1F1F2E",
    wraplength=500,
    justify=tk.CENTER,
)
motivation_label.pack(pady=20)

# Entry widget for task input with modern styling
task_entry = tk.Entry(
    root,
    width=40,
    font=("Helvetica", 14),
    borderwidth=2,
    relief="flat",
    bg="#3A3A4B",  # Darker background for input
    fg="#F3F4F7",  # Light text
    highlightbackground="#3A3A4B",  # Subtle focus border
    highlightthickness=2,
    insertbackground="#F3F4F7",  # Light cursor
)
task_entry.pack(pady=10)

# Add Task Button with a bold, energetic color
add_button = tk.Button(
    root,
    text="Add Task",
    command=add_task,
    width=20,
    font=("Helvetica", 12, "bold"),
    bg="#4C97FF",  # Lively blue for action
    fg="white",
    relief="flat",
    activebackground="#357BFF",  # Slightly darker when pressed
    activeforeground="white",
    height=2,
)
add_button.pack(pady=10)

# Task Listbox with a clean, modern look and dark background
task_listbox = tk.Listbox(
    root,
    width=40,
    height=12,
    selectmode=tk.SINGLE,
    font=("Helvetica", 12),
    bd=0,
    relief="flat",
    bg="#2A2A39",  # Darker list background
    fg="#D9E4F5",  # Light text
    selectbackground="#4C97FF",  # Highlighted task selection
    selectforeground="white",
    highlightthickness=0,
)
task_listbox.pack(pady=10)

# Frame for the buttons
button_frame = tk.Frame(root, bg="#1F1F2E")
button_frame.pack(pady=20)

# Delete Task Button
delete_button = tk.Button(
    button_frame,
    text="Delete Task",
    command=delete_task,
    width=15,
    font=("Helvetica", 12, "bold"),
    bg="#F44336",  # Red for danger/alert
    fg="white",
    relief="flat",
    activebackground="#D32F2F",  # Darker red when pressed
    activeforeground="white",
    height=2,
)
delete_button.pack(side=tk.LEFT, padx=20)

# Clear All Tasks Button
clear_button = tk.Button(
    button_frame,
    text="Clear All",
    command=clear_tasks,
    width=15,
    font=("Helvetica", 12, "bold"),
    bg="#FFEB3B",  # Yellow for caution
    fg="white",
    relief="flat",
    activebackground="#FBC02D",  # Darker yellow when pressed
    activeforeground="white",
    height=2,
)
clear_button.pack(side=tk.LEFT, padx=20)

# Mark Task as Completed Button
complete_button = tk.Button(
    button_frame,
    text="Mark Complete",
    command=toggle_complete,
    width=15,
    font=("Helvetica", 12, "bold"),
    bg="#8BC34A",  # Green for success
    fg="white",
    relief="flat",
    activebackground="#689F38",  # Darker green when pressed
    activeforeground="white",
    height=2,
)
complete_button.pack(side=tk.LEFT, padx=20)

# Keyboard Shortcuts
def on_enter(event):
    add_task()

def on_delete(event):
    delete_task()

def mark(event):
    toggle_complete()

root.bind('<Return>', on_enter)  # Enter key to add task
root.bind('<Delete>', on_delete)  # Delete key to delete task
root.bind('<Control-t>', mark)  # Ctrl+T to toggle completion

# Load tasks at startup
load_tasks()

# Run the application
root.mainloop()
