import os
import pickle


class GenericSpells:
    def __init__(self, spell_type, name):
        self.type = spell_type
        self.name = name

    @staticmethod
    def get_all_spells(direc="%APPDATA%/Wiz101Calc", file="%APPDATA%/Wiz101Calc/StandardSpells.pickle"):
        direc = os.path.expandvars(direc)
        file_full = os.path.expandvars(file)
        if not os.path.exists(direc):  # if directory doesn't exist
            os.mkdir(direc)  # create directory
        # directory must exist below this point
        existing_spells = []
        try:  # assumes the file exist
            with open(file_full, 'rb') as pickle_file:
                pickle_file.seek(0)
                while True:
                    try:
                        existing_spells.append(pickle.load(pickle_file))
                    except EOFError:
                        if len(existing_spells) > 0:
                            return existing_spells
                        else:
                            return False
        except FileNotFoundError:  # if file doesn't exist
            open(file)
            return False


def get_all_spells():
    return None