from tkinter import *
from tkinter import messagebox
import StandardSpells as StS
import MultiplierSpells as MpS
import PercentBuff as PerB
import FlatBuff as FlatB
import widgets as w


def creation():  # creates the form for choosing what type of spell
    creator = Tk()
    creator.title("Select a spell type")
    creator.focus_force()  # set this window to focus
    w.Button(master=creator, text="Standard", command=creation_standard).grid(row=0)
    w.Button(master=creator, text="Per Pip", command=creation_per_pip).grid(row=1)
    w.Button(master=creator, text="Percent Buff", command=creation_percent_blade).grid(row=2)
    creator.mainloop()


def creation_per_pip():
    def submission():
        try:
            name = name_entry.get()
            multiplier = float(multiplier_entry.get())
            if targets.get() == 1:
                multi_target = False
            else:
                multi_target = True
            MpS.MultiplierSpells(name, multi_target, multiplier)
        except ValueError:
            messagebox.showerror("Error", "Multiplier must be a number")

    c_pip = Tk()
    c_pip.title("Creating a per pip damage spell")
    name_entry = w.Entry("name", master=c_pip, width=30)
    # entry widget for name of spell
    name_entry.grid(row=0)
    name_entry.focus_force()  # gives this entry focus first
    multiplier_entry = w.Entry("Damage per pip", master=c_pip, width=30)
    # entry widget for the multiplier of spell
    multiplier_entry.grid(row=1)
    targets = IntVar(master=c_pip, value=3)  # variable for how many targets radio button is checked
    Radiobutton(master=c_pip, text="Single Target", variable=targets, value=1).grid(row=2)
    # ^single target radio button
    Radiobutton(master=c_pip, text="Multiple Targets", variable=targets, value=2).grid(row=3)
    # ^multi target radio button
    w.Button(radio_var=targets, master=c_pip, text="Submit", state=DISABLED, command=submission).grid(row=4)
    # button widget for submitting the spell


def creation_standard():  # creates the form for a standard spell addition
    def submission():
        state = 0
        try:
            name = name_entry.get()
            cost = int(cost_entry.get())  # error state of 0
            state += 1
            min_dam = int(min_dam_entry.get())  # error state of 1
            state += 1
            max_dam = int(max_dam_entry.get())  # error state of 2
            state += 1
            if min_dam > max_dam:
                raise ValueError  # error value of 3
            if targets.get() == 1:
                multi_target = False
            else:
                multi_target = True

            StS.StandardSpells(name, cost, multi_target, min_dam, max_dam)
        except ValueError:
            match state:
                case 0:
                    messagebox.showerror("Error", "Cost must be an integer.")
                    cost_entry.focus_force()
                case 1:
                    messagebox.showerror("Error", "Minimum damage must be an integer.")
                    min_dam_entry.focus_force()
                case 2:
                    messagebox.showerror("Error", "Maximum damage must be an integer.")
                    max_dam_entry.focus_force()
                case 3:
                    messagebox.showerror("Error", "Minimum damage must be less than or equal to maximum damage")
                    min_dam_entry.focus_force()

    c_standard = Tk()
    c_standard.title("Creating a standard damage spell")
    name_entry = w.Entry("name", master=c_standard, width=30)
    # entry widget for name of spell
    name_entry.grid(row=0)
    name_entry.focus_force()  # give this entry focus first
    cost_entry = w.Entry(default_text="cost", master=c_standard, width=30)
    # entry widget for cost of spell
    cost_entry.grid(row=1)
    min_dam_entry = w.Entry(default_text="Minimum damage", master=c_standard, width=30)
    # entry widget for minimum damage of spell
    min_dam_entry.grid(row=2)
    max_dam_entry = w.Entry(default_text="Maximum damage", master=c_standard, width=30)
    # entry widget for maximum damage of spell
    max_dam_entry.grid(row=3)
    targets = IntVar(master=c_standard, value=3)  # variable for how many targets radio button is checked
    Radiobutton(master=c_standard, text="Single Target", variable=targets, value=1).grid(row=4)
    # ^single target radio button
    Radiobutton(master=c_standard, text="Multiple Targets", variable=targets, value=2).grid(row=5)
    # ^multi target radio button
    submit_button = w.Button(master=c_standard, text="submit", state=DISABLED, command=submission)
    # ^submission disabled till entries filled out
    submit_button.grid(row=6)


def creation_percent_blade():
    def submission():
        state = 0
        try:
            name = name_entry.get()
            cost = int(cost_entry.get())
            state = 1
            percent = int(percent_entry.get())
            state = 2
            if percent < 1 or percent > 100:
                raise ValueError
            if targets.get() == 1:
                multi_target = False
            else:
                multi_target = True
            PerB.PercentBuff(name, cost, multi_target, percent)
        except ValueError:
            if state == 0:
                messagebox.showerror("Error", "Cost must be an integer.")
                cost_entry.focus_force()
            elif state == 1:
                messagebox.showerror("Error", "Percent buff must be an integer.")
                percent_entry.focus_force()
            else:
                messagebox.showerror("Error", "percent buff must be between 1% and 100%")
                percent_entry.focus_force()
    c_percent = Tk()
    c_percent.title("Creating a percent damage buff spell")
    name_entry = w.Entry("name", master=c_percent, width=30)
    name_entry.grid(row=0)
    cost_entry = w.Entry(default_text="cost", master=c_percent, width=30)
    cost_entry.grid(row=1)
    percent_entry = w.Entry("percent buff", master=c_percent, width=30)
    percent_entry.grid(row=2)
    targets = IntVar(master=c_percent, value=3)  # variable for how many targets radio button is checked
    Radiobutton(master=c_percent, text="Single Target", variable=targets, value=1).grid(row=3)
    # ^single target radio button
    Radiobutton(master=c_percent, text="Multiple Targets", variable=targets, value=2).grid(row=4)
    # ^multi target radio button
    submit_button = w.Button(master=c_percent, text="submit", state=DISABLED, command=submission)
    submit_button.grid(row=5)


def creation_flat_blade():
    def submission():
        state = 0
        try:
            name = name_entry.get()
            cost = int(cost_entry.get())
            state = 1
            flat = int(flat_entry.get())
            if targets.get() == 1:
                multi_target = False
            else:
                multi_target = True
            FlatB.FlatBuff(name, cost, multi_target, flat)
        except ValueError:
            if state == 0:
                messagebox.showerror("Error", "Cost must be an integer.")
                cost_entry.focus_force()
            else:
                messagebox.showerror("Error", "Flat buff must be an integer.")
                flat_entry.focus_force()

    c_flat = Tk()
    c_flat.title("Creating a flat damage buff spell")
    name_entry = w.Entry("name", master=c_flat, width=30)
    name_entry.grid(row=0)
    cost_entry = w.Entry("cost", master=c_flat, width=30)
    cost_entry.grid(row=1)
    targets = IntVar(master=c_flat, value=3)  # variable for how many targets radio button is checked
    Radiobutton(master=c_flat, text="Single Target", variable=targets, value=1).grid(row=2)
    # ^single target radio button
    Radiobutton(master=c_flat, text="Multiple Targets", variable=targets, value=2).grid(row=3)
    # ^multi target radio button
    flat_entry = w.Entry("flat buff", master=c_flat, width=30)
    flat_entry.grid(row=4)
    submit_button = w.Button(master=c_flat, text="submit", state=DISABLED, command=submission)
    submit_button.grid(row=5)


if __name__ == '__main__':
    creation()
