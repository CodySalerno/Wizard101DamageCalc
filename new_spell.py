from tkinter import *
import tkinter


class Entry(tkinter.Entry):  # Child class of Entry, adds default text support and 2 default binds.
    def __init__(self, default_text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_text = default_text  # default text to enter into entry form
        self.insert(0, default_text)  # does the insert of the default text
        self.bind("<FocusIn>", lambda event, default=default_text: self.text_deleter(event, default))
        # ^bind to remove the default text when the focus is on this widget
        self.bind("<FocusOut>", lambda event, default=default_text, blank="": self.text_adder(event, default, blank))
        # ^bind to add the default text when the focus comes off and nothing was provided
        self.not_default = False  # variable to keep track of if the entry has a value provided

    @staticmethod
    def text_deleter(e, default):
        caller = e.widget  # the widget that called this method
        if caller.get() == default:  # if the value hasn't been changed then delete it
            caller.delete(0, "end")
            return True  # indicates successful deletion
        return False  # indicates deletion didn't need to be done

    def text_adder(self, e, insertion, check_against):  # adds text if the current value is set to the check_against
        caller = e.widget  # the widget that called this method
        if caller.get() == check_against:  # checks current value against parameter
            caller.insert(0, insertion)  # adds the insertion if so
            return True  # indicates successful insertion
        self.not_default = True  # if it didn't have to add text then it's not the default value anymore
        return False  # indicates text wasn't added


class Button(tkinter.Button):  # Child class of Button
    # adds support for easily enabling button if all entry widgets filled out
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<Enter>", lambda event: self.on_enter(event))
        # ^ adds a bind for whenever you hover the button to check entry widgets

    def on_enter(self, e):  # checks whenever you hover the button if all entries have added information
        passed = True  # flag
        for widget in self.master.winfo_children():  # iterates through sibling widgets
            if widget.winfo_class() == "Entry":  # checks if class is entry (add text)
                if widget.get() == widget.default_text or widget.get() == "":  # if default text or blank text
                    passed = False  # trigger flag
                    break  # no need to continue iterations
        if passed:  # if flag not triggered
            self["state"] = "normal"  # sets button to be clickable


def creation():  # creates the form for choosing what type of spell
    creator = Tk()
    creator.title("Select a spell type")
    creator.focus_force()  # set this window to focus
    Button(creator, text="Standard", command=creation_standard).grid(row=0, column=0)
    Button(creator, text="Per Pip", command=creation_per_pip).grid(row=1, column=0)
    creator.mainloop()


def creation_per_pip():
    pass


def creation_standard():  # creates the form for a standard spell addition
    c_standard = Tk()
    name_entry = Entry("enter name here", c_standard, width=30)
    name_entry.grid(row=0, column=0)
    name_entry.focus_force()  # give this entry focus first
    cost_entry = Entry("cost", c_standard, width=30)
    cost_entry.grid(row=1, column=0)
    submit_button = Button(c_standard, text="submit", state=DISABLED)  # submission, disabled till entries filled out
    submit_button.grid(row=2, column=0)


if __name__ == '__main__':
    creation()
