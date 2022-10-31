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
    def __init__(self, radio_var=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.radio_var = radio_var  # the variable that keeps track of which radio button is clicked
        if self.radio_var is None:  # if no variable is given (i.e. no radio buttons affect this button)
            self.radio_val = -1
        else:
            self.radio_val = radio_var.get()  # finds the value the variable has when this button is created
            # TODO: give the variable an attribute for its default value instead of this method.
            # TODO: Current method may cause an issue if button created after value changed.
        self.bind("<Enter>", lambda event: self.on_enter(self.radio_val))
        # ^adds a bind for whenever you hover the button to check entry widgets
        # ^lambda has to take in argument but isn't needed in on_enter function

    def on_enter(self, default_radio):
        print("def rad " + str(default_radio))
        entry_passed = True  # flag
        if default_radio == -1:
            radio_pass = True
        else:
            radio_pass = False
        for widgets in self.master.winfo_children():  # iterates through sibling widgets
            if widgets.winfo_class() == "Entry":  # checks if class is entry (add text)
                print('entry')
                if widgets.get() == widgets.default_text or widgets.get() == "":  # if default text or blank text
                    print('entry flag bad')
                    entry_passed = False  # trigger flag
                    break  # no need to continue iterations
        if default_radio != -1:  # checks if class is radio button
            print('def radio not -1')
            print(self.radio_var.get())
            if self.radio_var.get() != default_radio:
                print('radio flag good')
                radio_pass = True
        if entry_passed and radio_pass:  # if flag not triggered
            self["state"] = "normal"  # sets button to be clickable
        else:
            self["state"] = "disabled"
