import tkinter as tk
from tkinter import ttk
import customtkinter
from src.Pythonfiles.App.Defs import App




# create the root window
root = tk.Tk()
root.title('Server Launcher')
root.configure(bg='#242424')
root.iconbitmap(r'src\images\icon.ico')
root.geometry("1000x400")
root.resizable(False, False)


style = ttk.Style()
style.configure('TFrame', background='#242424',foreground='#242424')
style.configure('TButton',background='#242424',foreground='#242424')
style.configure('TLabel', background='#242424',foreground='#242424')

#global variables


# create the notebook widget
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# create the first frame
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text="Server Management")


# create the "Create server" button in frame1


app = App(root)
app.pack(side="top", fill="both", expand=True)

start_btn = customtkinter.CTkButton(master=frame1, text='Start server', command=app.start)
start_btn.pack(pady=(10), anchor='w')

create_btn = customtkinter.CTkButton(master=frame1, text='Create server', command=app.create)
create_btn.pack(pady=(10), anchor='w')

clear_btn = customtkinter.CTkButton(master=frame1, text="Clear Console", command=app.clear_console)
clear_btn.pack(pady=(10), anchor='w')

stop_btn = customtkinter.CTkButton(master=frame1, text='Stop server', command=app.stop)
stop_btn.pack(pady=(10), anchor='w')

# create the second frame
frame2 = ttk.Frame(notebook)
notebook.add(frame2, text="Ect")


# start the event loop


app.mainloop()

