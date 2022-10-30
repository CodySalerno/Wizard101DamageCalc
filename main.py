from tkinter import *
import new_spell
root = Tk()
root.title("Wizard101 Spell Damage Calculator")


def calculate():
    pass


def create_new():
    new_spell.creation()


def check_spells():
    pass


calcButton = Button(root, text="Calculator", command=calculate)
calcButton.grid(row=0, column=0)
spellButton = Button(root, text="Add new spell", command=create_new)
spellButton.grid(row=1, column=0)
checkButton = Button(root, text="See created spells", command=check_spells)
checkButton.grid(row=2, column=0)

root.mainloop()
