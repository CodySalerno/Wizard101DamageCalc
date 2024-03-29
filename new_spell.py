import tkinter as tk
from tkinter import messagebox
import Spells.Attack_Spells.StandardSpells as StS
import Spells.Attack_Spells.MultiplierSpells as MpS
import Spells.Buff_Spells.PercentBuff as PerB
import widgets as w


def creation():  # creates the form for choosing what type of spell
    creator = tk.Tk()
    creator.title("Select a spell type")
    creator.focus_force()  # set this window to focus
    w.Button(master=creator, text="Standard", command=creation_standard).grid(row=0)
    w.Button(master=creator, text="Per Pip", command=creation_per_pip).grid(row=1)
    w.Button(master=creator, text="Percent Buff", command=creation_percent_blade).grid(row=2)
    creator.mainloop()


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
            school = school_value.get()

            StS.StandardSpells(name, cost, multi_target, school, min_dam, max_dam)
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

    schools = ["Balance", "Storm", "Fire", "Life", "Death", "Ice", "Myth"]
    c_standard = tk.Tk()
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
    school_value = tk.StringVar(c_standard, "Select a school")
    school_menu = tk.OptionMenu(c_standard, school_value, *schools)
    school_menu.grid(row=4)
    targets = tk.IntVar(master=c_standard, value=3)  # variable for how many targets radio button is checked
    tk.Radiobutton(master=c_standard, text="Single Target", variable=targets, value=1).grid(row=5)
    # ^single target radio button
    tk.Radiobutton(master=c_standard, text="Multiple Targets", variable=targets, value=2).grid(row=6)
    # ^multi target radio button
    w.Button(master=c_standard, text="submit", menu_var=school_value, state=tk.DISABLED, command=submission).grid(row=7)
    # ^submission disabled till entries filled out


def creation_per_pip():
    def submission():
        try:
            name = name_entry.get()
            multiplier = float(multiplier_entry.get())
            if targets.get() == 1:
                multi_target = False
            else:
                multi_target = True
            school = school_value.get()
            MpS.MultiplierSpells(name, multi_target, school, multiplier)
        except ValueError:
            messagebox.showerror("Error", "Multiplier must be a number")

    schools = ["Balance", "Storm", "Fire", "Life", "Death", "Ice", "Myth"]
    c_pip = tk.Tk()
    c_pip.title("Creating a per pip damage spell")
    name_entry = w.Entry("name", master=c_pip, width=30)
    # entry widget for name of spell
    name_entry.grid(row=0)
    name_entry.focus_force()  # gives this entry focus first
    multiplier_entry = w.Entry("Damage per pip", master=c_pip, width=30)
    # entry widget for the multiplier of spell
    multiplier_entry.grid(row=1)
    school_value = tk.StringVar(c_pip, "Select a school")
    school_menu = tk.OptionMenu(c_pip, school_value, *schools)
    school_menu.grid(row=2)
    targets = tk.IntVar(master=c_pip, value=3)  # variable for how many targets radio button is checked
    tk.Radiobutton(master=c_pip, text="Single Target", variable=targets, value=1).grid(row=3)
    # ^single target radio button
    tk.Radiobutton(master=c_pip, text="Multiple Targets", variable=targets, value=2).grid(row=4)
    # ^multi target radio button
    w.Button(radio_var=targets, menu_var=school_value, master=c_pip, text="Submit", state=tk.DISABLED, command=submission).grid(row=5)
    # button widget for submitting the spell


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
            school = school_value.get()
            PerB.PercentBuff(name, cost, multi_target, school, percent)
        except ValueError:
            if state == 0:
                messagebox.showerror("Error", "Cost must be an integer.")
                cost_entry.focus_force()
            elif state == 1:
                messagebox.showerror("Error", "Percent buff must be an integer.")
                percent_entry.focus_force()
            elif state == 2:
                messagebox.showerror("Error", "percent buff must be between 1% and 100%")
                percent_entry.focus_force()

    schools = ["Balance", "Storm", "Fire", "Life", "Death", "Ice", "Myth"]
    c_percent = tk.Tk()
    c_percent.title("Creating a percent damage buff spell")
    name_entry = w.Entry("name", master=c_percent, width=30)
    name_entry.grid(row=0)
    cost_entry = w.Entry(default_text="cost", master=c_percent, width=30)
    cost_entry.grid(row=1)
    tk.Label(master=c_percent, text="If the spell increases damage by 50% percent buff should be 50").grid(row=2)
    percent_entry = w.Entry("percent buff", master=c_percent, width=30)
    percent_entry.grid(row=3)
    school_value = tk.StringVar(c_percent, "Select a school")
    school_menu = tk.OptionMenu(c_percent, school_value, *schools)
    school_menu.grid(row=4)
    targets = tk.IntVar(master=c_percent, value=3)  # variable for how many targets radio button is checked
    tk.Radiobutton(master=c_percent, text="Single Target", variable=targets, value=1).grid(row=5)
    # ^single target radio button
    tk.Radiobutton(master=c_percent, text="Multiple Targets", variable=targets, value=2).grid(row=6)
    # ^multi target radio button
    w.Button(master=c_percent, text="submit", state=tk.DISABLED, menu_var=school_value, command=submission).grid(row=7)
