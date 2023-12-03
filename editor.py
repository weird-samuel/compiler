# Import necessary modules
import subprocess
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter.filedialog import asksaveasfilename, askopenfilename

# Global variables
path = ''
process = None

# Function to set the global file path variable


def set_path(file_path):
    global path
    path = file_path

# Function to run Python code using subprocess and capture standard output and error


def run_subprocess(code):
    try:
        global process

        # Using subprocess to run the Python code
        process = subprocess.Popen(
            ["python", "compiler.py", code],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Getting the standard output and error from the process
        stdout, stderr = process.communicate(input=None)

        return stdout, stderr

    except Exception as e:
        return f"Error: {str(e)}", None

# Function to update the output display widget with captured output and error


def update_output_display(stdout, stderr):
    # Configuring and updating the output display widget
    output_display.config(state=tk.NORMAL)
    output_display.delete("1.0", tk.END)
    output_display.insert(tk.END, stdout)
    if stderr:
        output_display.insert(tk.END, stderr, "error")
    output_display.config(state=tk.DISABLED)

# Function to execute code, capture output, and update the output display


def execute_code():
    code = our_editor.get("1.0", tk.END)

    stdout, stderr = run_subprocess(code)

    update_output_display(stdout, stderr)

# Function to handle and display errors


def handle_error(exception):
    # Handling and displaying errors if any
    output_display.config(state=tk.NORMAL)
    output_display.delete("1.0", tk.END)
    output_display.insert(tk.END, exception)
    output_display.config(state=tk.DISABLED)

# Function to open a Python file, read its content, and load it into the editor


def open_file():
    file_path = askopenfilename(filetypes=[('python files', '*.py')])
    with open(file_path, 'r') as file:
        code = file.read()
        our_editor.delete('1.0', tk.END)
        our_editor.insert('1.0', code)
        set_path(file_path)

# Function to save the code to a file, asking for a file path if none is set


def save_as():
    if path == '':
        file_path = asksaveasfilename(filetypes=[('python files', '*.py')])
    else:
        file_path = path
    with open(file_path, 'w') as file:
        code = our_editor.get("1.0", tk.END)
        file.write(code)
        set_path(file_path)


# GUI setup
root = tk.Tk()
root.title("My Improved Compiler IDE")

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Save", command=save_as)
file_menu.add_command(label="Save AS", command=save_as)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Exit", command=exit)

# Run menu
run_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Run", menu=run_menu)
run_menu.add_command(label="Execute", command=execute_code)

# Code editor
our_editor = scrolledtext.ScrolledText(root, wrap=tk.WORD)
our_editor.pack(expand=True, fill='both')
our_editor.configure(font=("TkDefaultFont", 10))  # Use default font

# Output display
output_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
output_display.pack(expand=True, fill='both')
# Red color for error messages
output_display.tag_configure("error", foreground="red")
output_display.config(state=tk.DISABLED)

# Start the Tkinter main event loop
root.mainloop()
