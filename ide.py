import tkinter as tk
from tkinter.filedialog import asksaveasfilename,askopenfilename
import tkinter.scrolledtext as scrolledtext
import subprocess
path=''

def set_path(file_path):
    global path
    path=file_path

process = None


def execute_code():
    code = our_editor.get("1.0", tk.END)

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

        # Configuring and updating the output display widget
        output_display.config(state=tk.NORMAL)
        output_display.delete("1.0", tk.END)
        output_display.insert(tk.END, stdout)
        if stderr:
            output_display.insert(tk.END, stderr, "error")
        output_display.config(state=tk.DISABLED)

    except Exception as e:
        # Handling and displaying errors if any
        output_display.config(state=tk.NORMAL)
        output_display.delete("1.0", tk.END)
        output_display.insert(tk.END, f"Error: {str(e)}")
        output_display.config(state=tk.DISABLED)


def open_file():
    file_path=askopenfilename(filetypes=[('python files','*.py')])
    with open(file_path,'r') as file:
        code = file.read()
        our_editor.delete('1.0', tk.END)
        our_editor.insert('1.0', code)
        set_path(file_path)

def save_as():
    if path=='':
        file_path=asksaveasfilename(filetypes=[('python files','*.py')])
    else:
        file_path=path
    with open(file_path,'w') as file:
        code = our_editor.get("1.0", tk.END)
        file.write(code)
        set_path(file_path)



root = tk.Tk()
root.title("Group B1's compiler")

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
output_display = scrolledtext.ScrolledText(root, wrap=tk.WORD,height=10)
output_display.pack(expand=True, fill='both')
output_display.tag_configure("error", foreground="red")  # Red color for error messages
output_display.config(state=tk.DISABLED)

root.mainloop()
