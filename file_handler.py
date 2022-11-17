import os
import pickle
from StandardSpells import StandardSpells
from MultiplierSpells import MultiplierSpells

std_dir = "%APPDATA%/Wiz101Calc"
std_dir = os.path.expandvars(std_dir)
std_file = "%APPDATA%/Wiz101Calc/StandardSpells.pickle"
std_file = os.path.expandvars(std_file)


def create_file(direc="%APPDATA%/Wiz101Calc", file="%APPDATA%/Wiz101Calc/StandardSpells.pickle"):
    """Creates a file at the specified directory and file if it doesn't already exist."""
    direc = os.path.expandvars(direc)
    file = os.path.expandvars(file)
    if not os.path.exists(file):  # if directory doesn't exist
        os.mkdir(direc)  # create directory
    if not os.path.exists(file):
        open(file, 'w').close()


def add_to_file(spell, direc=std_dir, file=std_file):
    """Adds spell to file, if file doesn't exist calls the create_file method and then recalls itself"""
    try:
        with open(file, 'a+b') as pickle_file:
            pickle.dump(spell, pickle_file)
    except FileNotFoundError:
        create_file(direc, file)
        add_to_file(spell, direc, file)


def get_all_spells(direc=std_dir, file=std_file):
    """Returns all spells found in file as a list with 2 indexes.
    The first index is standard spells the second is per pip spells."""
    all_spells = [{}, {}]
    try:
        with open(file, 'rb') as pickle_file:
            pickle_file.seek(0)
            while True:
                try:
                    curr_spell = pickle.load(pickle_file)
                    if curr_spell.dict["Type"] == "Standard":
                        all_spells[0][curr_spell.name] = curr_spell.dict
                    elif curr_spell.dict["Type"] == "Multiplier":
                        all_spells[1][curr_spell.name] = curr_spell.dict
                except EOFError:
                    print('reached end of file')
                    return all_spells
    except FileNotFoundError:
        print('file not found')
        create_file(direc, file)
        return all_spells


def search_for_spell(name, direc=std_dir, file=std_file) -> StandardSpells | MultiplierSpells:
    """Searches file for spell with name provided. If found returns the spell, otherwise returns None."""
    try:
        with open(file, 'rb') as pickle_file:
            pickle_file.seek(0)
            while True:
                try:
                    curr_spell = pickle.load(pickle_file)
                    if curr_spell.dict["Name"] == name:
                        return curr_spell
                except EOFError:
                    return None
    except FileNotFoundError:
        print("File not found")
        create_file(direc, file)
        return None
