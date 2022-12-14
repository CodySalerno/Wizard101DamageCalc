import tkinter as tk
import new_spell
import check_spell
import calculate as calc


def calculate():
    root.destroy()
    calc.main()


def create_new():
    new_spell.creation()


def check_spells():
    check_spell.creation()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Wizard101 Spell Damage Calculator")
    calcButton = tk.Button(master=root, text="Calculator", command=calculate)
    calcButton.grid(row=0)
    spellButton = tk.Button(master=root, text="Add new spell", command=create_new)
    spellButton.grid(row=1)
    checkButton = tk.Button(master=root, text="See created spells", command=check_spells)
    checkButton.grid(row=2)
    root.mainloop()
