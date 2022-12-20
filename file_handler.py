import os
import pickle
from StandardSpells import StandardSpells
from MultiplierSpells import MultiplierSpells
from PercentBuff import PercentBuff
from FlatBuff import FlatBuff
from tkinter import messagebox

std_dir = "%APPDATA%/Wiz101Calc"
std_dir = os.path.expandvars(std_dir)
std_file = "%APPDATA%/Wiz101Calc/AllSpells.pickle"
std_file = os.path.expandvars(std_file)
std_enemy_file = "%APPDATA%/Wiz101Calc/Enemy.pickle"
std_enemy_file = os.path.expandvars(std_enemy_file)


def create_files(direc=std_dir, file=std_file, enemy_file=std_enemy_file):
    """Creates a file at the specified directory and file if it doesn't already exist."""
    direc = os.path.expandvars(direc)
    file = os.path.expandvars(file)
    enemy_file = os.path.expandvars(enemy_file)
    if not os.path.exists(direc):  # if directory doesn't exist
        os.mkdir(direc)  # create directory
    if not os.path.exists(file):
        open(file, 'w').close()
    if not os.path.exists(enemy_file):
        open(file, 'w').close()


def add_to_file(spell, direc=std_dir, file=std_file):
    """Adds spell to file, if file doesn't exist calls the create_files method and then recalls itself
       If spell name already exists calls update confirm instead. """
    found = search_for_spell(spell.name)
    if found is not None:
        update_confirm(spell, found)
    else:
        try:
            with open(file, 'a+b') as pickle_file:
                pickle.dump(spell, pickle_file)
        except FileNotFoundError:
            create_files(direc, file)
            add_to_file(spell, direc, file)


def get_all_spells(direc=std_dir, file=std_file):
    """Returns all spells found in file as a list with 2 indexes.
    The 0th index is standard damage spells the 1st is per pip damage spells.
    The 2nd index id percent buff spells and the 3rd index is flat buff spells. """
    all_spells = [{}, {}, {}, {}]
    try:
        with open(file, 'rb') as pickle_file:
            pickle_file.seek(0)
            while True:
                try:
                    curr_spell = pickle.load(pickle_file)
                    if curr_spell.type == "Standard":
                        all_spells[0][curr_spell.name] = curr_spell
                    elif curr_spell.type == "Multiplier":
                        all_spells[1][curr_spell.name] = curr_spell
                    elif curr_spell.type == "Percent Buff":
                        all_spells[2][curr_spell.name] = curr_spell
                    elif curr_spell.type == "Flat Buff":
                        all_spells[3][curr_spell.name] = curr_spell
                    else:
                        raise ValueError
                except ValueError:
                    print("unknown type")
                    exit(2)
                except EOFError:
                    return all_spells
    except FileNotFoundError:
        create_files(direc, file)
        return all_spells


def search_for_spell(name: str, direc=std_dir, file=std_file)\
                     -> StandardSpells | MultiplierSpells | PercentBuff | FlatBuff | None:
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
        create_files(direc, file)
        return None


def update_confirm(new_spell: StandardSpells | MultiplierSpells | PercentBuff | FlatBuff,
                   old_spell: StandardSpells | MultiplierSpells | PercentBuff | FlatBuff, file=std_file):
    if new_spell.dict == old_spell.dict:
        messagebox.showinfo("Same spell", "This spell is already in your file with these stats.")
        return False
    if type(new_spell) != type(old_spell):
        type_question = "The types of the previously entered spell and the new one do not match.\n" \
                        "The old spell had type" + old_spell.type + ".\n" \
                        "The new spell has type" + new_spell.type + ".\n" \
                        "Would you like to change to the new type?"
        change_type = messagebox.askyesno("Spell type", type_question)
        if change_type == 0:  # if they select No
            return False
    stats_question = "This spell's name is already known:\n" \
                     "The old stats are \n" + str(old_spell.dict) + ".\n" \
                     "The new stats are \n" + str(new_spell.dict) + ".\n" \
                     "Would you like to keep the new stats?"
    change_stats = messagebox.askyesno("Stats change", stats_question)
    if change_stats == 0:
        return False
    else:
        update(new_spell, file)


def update(spell, file=std_file):
    all_spells = []
    try:
        with open(file, 'rb') as pickle_file:
            pickle_file.seek(0)
            while True:
                try:
                    curr_spell = pickle.load(pickle_file)
                    if curr_spell.name == spell.name:
                        curr_spell = spell
                    all_spells.append(curr_spell)
                except EOFError:
                    break
        for spell in all_spells:
            try:
                with open(file, 'wb') as pickle_file:
                    pickle_file.seek(0)
                    pickle.dump(spell, pickle_file)
            except FileNotFoundError:
                print("This shouldn't happen")
    except FileNotFoundError:
        print("This shouldn't happen")


def create_enemy_file(direc=std_dir, file=std_enemy_file):
    """Creates a file at the specified directory and file if it doesn't already exist."""
    direc = os.path.expandvars(direc)
    file = os.path.expandvars(file)
    if not os.path.exists(direc):  # if directory doesn't exist
        os.mkdir(direc)  # create directory
    if not os.path.exists(file):
        open(file, 'w').close()


if __name__ == '__main__':
    pass
