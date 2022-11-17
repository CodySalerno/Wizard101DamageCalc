from tkinter import *
import widgets as w
from tkinter import messagebox
import file_handler as fh


def creation():  # creates the form for choosing what type of spell
    def submission():
        name = name_entry.get()
        spell = fh.search_for_spell(name)
        if spell is None:
            messagebox.showwarning("missing spell", "No spell was found with this name.")
        else:
            messagebox.showinfo(name, spell.dict)

    checker = Tk()
    checker.title("spell checker")
    checker.focus_force()  # set this window to focus
    name_entry = w.Entry(default_text="Name", master=checker)
    name_entry.grid(row=0)  # entry box for name of spell to check
    w.Button(master=checker, text="Submit", state=DISABLED, command=submission).grid(row=4)
    # ^button to click when ready to submit
    checker.mainloop()
