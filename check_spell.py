from tkinter import *
import widgets as w


def creation():  # creates the form for choosing what type of spell
    def submission():
        pass
    checker = Tk()
    checker.title("spell checker")
    checker.focus_force()  # set this window to focus
    w.Entry(default_text="Name", master=checker).grid(row=0)  # entry box for name of spell to check
    spell_type = IntVar(master=checker, value=3)  # variable for which spell radio button is checked
    Radiobutton(master=checker, text="Standard spell", variable=spell_type, value=1).grid(row=1)
    # ^standard spell radio button
    Radiobutton(master=checker, text="Per pip spell", variable=spell_type, value=2).grid(row=2)
    # ^per pip spell radio button
    w.Button(radio_var=spell_type, master=checker, text="Submit", state=DISABLED, command=submission).grid(row=4)
    # ^button to click when ready to submit
    checker.mainloop()
