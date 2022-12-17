from tkinter import *
import new_spell
import check_spell
import calculate as calc


def calculate():
    calc.main()


def create_new():
    new_spell.creation()


def check_spells():
    check_spell.creation()


if __name__ == "__main__":
    root = Tk()
    root.title("Wizard101 Spell Damage Calculator")
    calcButton = Button(master=root, text="Calculator", command=calculate)
    calcButton.grid(row=0)
    spellButton = Button(master=root, text="Add new spell", command=create_new)
    spellButton.grid(row=1)
    checkButton = Button(master=root, text="See created spells", command=check_spells)
    checkButton.grid(row=2)

    root.mainloop()
