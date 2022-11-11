from tkinter import *
from tkinter import messagebox
import StandardSpells as StS
import MultiplierSpells as MpS
import widgets as w


def creation():  # creates the form for choosing what type of spell
    creator = Tk()
    creator.title("Select a spell type")
    creator.focus_force()  # set this window to focus
    w.Button(master=creator, text="Standard", command=creation_standard).grid(row=0)
    print('why does this work')
    w.Button(master=creator, text="Per Pip", command=creation_per_pip).grid(row=1)
    creator.mainloop()


def creation_per_pip():
    def submission():
        try:
            name = name_entry.get()
            multiplier = int(damage_per_pip_entry.get())
            MpS.MultiplierSpells("Multiplier", name, multiplier)
        except ValueError:
            messagebox.showerror("Error", "Multiplier must be an integer")

    c_pip = Tk()
    name_entry = w.Entry("name", master=c_pip, width=30)
    name_entry.grid(row=0)
    damage_per_pip_entry = w.Entry("Damage per pip", master=c_pip, width=30)
    damage_per_pip_entry.grid(row=1)
    w.Button(master=c_pip, text="submit", state=DISABLED, command=submission).grid(row=2)


def creation_standard():  # creates the form for a standard spell addition
    def submission():
        state = 0
        try:
            name = name_entry.get()
            cost = int(cost_entry.get())  # error value of 0
            state += 1
            min_dam = int(min_dam_entry.get())  # error value of 1
            state += 1
            max_dam = int(max_dam_entry.get())  # error value of 2
            state += 1
            if min_dam >= max_dam:
                raise ValueError  # error value of 3
            StS.StandardSpells("standard", name, cost, min_dam, max_dam)
        except ValueError:
            match state:
                case 0:
                    messagebox.showerror("Error", "Cost must be an integer")
                    cost_entry.focus_force()
                case 1:
                    messagebox.showerror("Error", "minimum damage must be an integer")
                    min_dam_entry.focus_force()
                case 2:
                    messagebox.showerror("Error", "Maximum damage must be an integer")
                    max_dam_entry.focus_force()
                case 3:
                    messagebox.showerror("Error", "Minimum damage must be less than maximum damage")
                    min_dam_entry.focus_force()

    c_standard = Tk()
    name_entry = w.Entry("name", master=c_standard, width=30)
    name_entry.grid(row=0)
    name_entry.focus_force()  # give this entry focus first
    cost_entry = w.Entry(default_text="cost", master=c_standard, width=30)
    cost_entry.grid(row=1)
    min_dam_entry = w.Entry(default_text="Minimum damage", master=c_standard, width=30)
    min_dam_entry.grid(row=2)
    max_dam_entry = w.Entry(default_text="Maximum damage", master=c_standard, width=30)
    max_dam_entry.grid(row=3)
    w.Button(master=c_standard, text="submit", state=DISABLED, command=submission).grid(row=4)
    # ^submission, disabled till entries filled out


if __name__ == '__main__':
    creation()
