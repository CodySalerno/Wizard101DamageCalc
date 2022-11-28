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
            MpS.MultiplierSpells(name, multiplier)
        except ValueError:
            messagebox.showerror("Error", "Multiplier must be a number")

    c_pip = Tk()
    name_entry = w.Entry("name", master=c_pip, width=30)
    # entry widget for name of spell
    name_entry.grid(row=0)
    name_entry.focus_force()  # gives this entry focus first
    multiplier_entry = w.Entry("Damage per pip", master=c_pip, width=30)
    # entry widget for the multiplier of spell
    multiplier_entry.grid(row=1)
    w.Button(master=c_pip, text="submit", state=DISABLED, command=submission).grid(row=2)
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
            if min_dam >= max_dam:
                raise ValueError  # error value of 3
            StS.StandardSpells(name, cost, min_dam, max_dam)
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
                    messagebox.showerror("Error", "Minimum damage must be less than maximum damage")
                    min_dam_entry.focus_force()

    c_standard = Tk()
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
    submit_button = w.Button(master=c_standard, text="submit", state=DISABLED, command=submission)
    submit_button.grid(row=4)  # ^submission disabled till entries filled out


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
            PerB.PercentBuff(name, cost, percent)
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
    name_entry = w.Entry("name", master=c_percent, width=30)
    name_entry.grid(row=0)
    cost_entry = w.Entry(default_text="cost", master=c_percent, width=30)
    cost_entry.grid(row=1)
    percent_entry = w.Entry("percent buff", master=c_percent, width=30)
    percent_entry.grid(row=2)
    submit_button = w.Button(master=c_percent, text="submit", state=DISABLED, command=submission)
    submit_button.grid(row=3)


def creation_flat_blade():
    def submission():
        state = 0
        try:
            name = name_entry.get()
            cost = int(cost_entry.get())
            state = 1
            flat = int(flat_entry.get())
            FlatB.FlatBuff(name, cost, flat, True)
        except ValueError:
            if state == 0:
                messagebox.showerror("Error", "Cost must be an integer.")
                cost_entry.focus_force()
            else:
                messagebox.showerror("Error", "Flat buff must be an integer.")
                flat_entry.focus_force()

    c_flat = Tk()
    name_entry = w.Entry("name", master=c_flat, width=30)
    name_entry.grid(row=0)
    cost_entry = w.Entry("cost", master=c_flat, width=30)
    cost_entry.grid(row=1)
    flat_entry = w.Entry("flat buff", master=c_flat, width=30)
    flat_entry.grid(row=2)
    submit_button = w.Button(master=c_flat, text="submit", state=DISABLED, command=submission)
    submit_button.grid(row=3)


if __name__ == '__main__':
    creation()
