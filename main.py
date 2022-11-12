from tkinter import *
import new_spell
import check_spell
import GenericSpells
import os
import pickle
import StandardSpells

root = Tk()
root.title("Wizard101 Spell Damage Calculator")


def calculate():
    pass


def create_new():
    new_spell.creation()


def check_spells():
    check_spell.creation()


def get_all_spells(direc="%APPDATA%/Wiz101Calc", file="%APPDATA%/Wiz101Calc/StandardSpells.pickle"):
    direc = os.path.expandvars(direc)
    file_full = os.path.expandvars(file)
    if not os.path.exists(direc):  # if directory doesn't exist
        os.mkdir(direc)  # create directory
    # directory must exist below this point
    existing_spells = []
    standard_spells = {}
    multiplier_spells = {}
    try:  # assumes the file exist
        with open(file_full, 'rb') as pickle_file:
            pickle_file.seek(0)
            while True:
                try:
                    spell = pickle.load(pickle_file)  # returns a dictionary object
                    print(spell)
                    # if spell.key() == "Standard":
                    #    standard_spells[spell.key()] = spell[spell.key()]
                    # elif spell.key() == "Multiplier":
                    #    pass

                    existing_spells.append(pickle.load(pickle_file))
                except EOFError:
                    print('end')
                    if len(existing_spells) > 0:
                        return existing_spells
                    else:
                        return False
    except FileNotFoundError:  # if file doesn't exist
        open(file)
        return False


if __name__ == "__main__":
    all_spells = get_all_spells()
    calcButton = Button(master=root, text="Calculator", command=calculate)
    calcButton.grid(row=0)
    spellButton = Button(master=root, text="Add new spell", command=create_new)
    spellButton.grid(row=1)
    checkButton = Button(master=root, text="See created spells", command=check_spells)
    checkButton.grid(row=2)

    root.mainloop()
