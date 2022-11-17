from tkinter import *
import widgets as w
from tkinter import messagebox
import StandardSpells as StS
import file_handler as fh


def creation():  # creates the form for choosing what type of spell
    def submission():
        name = name_entry.get()
        if spell_type.get() == 1:
            spell = fh.search_for_spell(name)
            if spell:
                messagebox.showinfo(name, "Cost: " + str(spell.cost) + "\n"
                                    "Minimum damage: " + str(spell.min_dam) + "\n"
                                    "Maximum damage: " + str(spell.max_dam))
            else:
                messagebox.showwarning("missing spell", "No standard spell was found with this name.")
        elif spell_type.get() == 2:
            spell = fh.search_for_spell(name)
            if spell:
                messagebox.showinfo(name, "Multiplier: " + str(spell.multiplier))
        else:
            messagebox.showerror("Unreachable", "This messagebox shouldn't have been reachable.\n"
                                                "Please contact us with steps on how to reproduce this error box.")
    checker = Tk()
    checker.title("spell checker")
    checker.focus_force()  # set this window to focus
    name_entry = w.Entry(default_text="Name", master=checker)
    name_entry.grid(row=0)  # entry box for name of spell to check
    spell_type = IntVar(master=checker, value=3)  # variable for which spell radio button is checked
    Radiobutton(master=checker, text="Standard spell", variable=spell_type, value=1).grid(row=1)
    # ^standard spell radio button
    Radiobutton(master=checker, text="Per pip spell", variable=spell_type, value=2).grid(row=2)
    # ^per pip spell radio button
    w.Button(radio_var=spell_type, master=checker, text="Submit", state=DISABLED, command=submission).grid(row=4)
    # ^button to click when ready to submit
    checker.mainloop()
