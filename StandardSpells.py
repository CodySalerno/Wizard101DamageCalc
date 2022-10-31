import pickle
import os
from tkinter import messagebox


class StandardSpells:
    def __init__(self, spell_type, name, cost, min_dam, max_dam):
        self.type = spell_type
        self.name = name
        self.cost = cost
        self.min_dam = min_dam
        self.max_dam = max_dam
        self.check_file()

    def check_file(self, direc="%APPDATA%/Wiz101Calc", file="%APPDATA%/Wiz101Calc/StandardSpells.pickle"):
        direc = os.path.expandvars(direc)
        file = os.path.expandvars(file)
        new_data = {self.type: {
            "name": self.name,
            "cost": self.cost,
            "min_dam": self.min_dam,
            "max_dam": self.max_dam}}
        if not os.path.exists(direc):  # if directory doesn't exist
            os.mkdir(direc)  # create directory
            self.add_to_file(file, new_data)  # creates and adds data to file
            return True
        # directory must exist below this point
        existing_spells = []
        try:  # assumes the file exist
            with open(file, 'rb') as pickle_file:
                pickle_file.seek(0)
                while True:
                    try:
                        existing_spells.append(pickle.load(pickle_file))
                    except EOFError:
                        break
            for spell in existing_spells:
                for type_of_spell in spell.keys():
                    if type_of_spell == self.type:
                        if spell[type_of_spell]['name'] == self.name:
                            self.update_to_file(file, new_data, spell)
                            return True
            self.add_to_file(file, new_data)  # if it makes it this far no spell has the same type and name
        except FileNotFoundError:  # if file doesn't exist
            self.add_to_file(file, new_data)

    @staticmethod
    def del_from_file(file, old_data):
        unpickled_objs = []
        with open(file, 'rb') as pickle_file:

            while True:
                obj_count = 0
                try:
                    unpickled_objs.append(pickle.load(pickle_file))
                    obj_count += 1
                    if unpickled_objs[-1] == old_data:
                        found_index = len(unpickled_objs) - 1
                except EOFError:
                    break
            if found_index == 0:
                unpickled_objs = unpickled_objs[1:]
            else:
                unpickled_objs = unpickled_objs[0:found_index] + unpickled_objs[found_index + 1:]
        with open(file, 'w+b') as pickle_file:
            pickle_file.seek(0)
            for obj in unpickled_objs:
                pickle.dump(obj, pickle_file)

    @staticmethod
    def read_pickle_file(file="%APPDATA%/Wiz101Calc/StandardSpells.pickle",  name=None, spell_type='standard'):
        all_obj = []
        file = os.path.expandvars(file)
        with open(file, 'rb') as pickle_file:
            pickle_file.seek(0)
            while True:
                try:
                    all_obj.append(pickle.load(pickle_file))
                    if name is not None:
                        if all_obj[-1][spell_type]['name'] == name:
                            return all_obj[-1]
                except EOFError:
                    break
        print(all_obj)
        return False

    def update_to_file(self, file, new_data, old_data):
        question = "This spell's name is already known:\n" \
                   "Old Cost: " + str(old_data[self.type]['cost']) + "\n" \
                   "Old Minimum damage: " + str(old_data[self.type]['min_dam']) + "\n" \
                   "Old Maximum damage: " + str(old_data[self.type]['max_dam']) + "\n" \
                   "Would you like to change its stats to your input?\n" \
                   "New Cost: " + str(self.cost) + "\n" \
                   "New Minimum damage: " + str(self.min_dam) + "\n" \
                   "New Maximum damage: " + str(self.max_dam) + "\n"
        response = messagebox.askquestion(self.name, question)
        if response == "yes":
            self.del_from_file(file, old_data)
            self.add_to_file(file, new_data)
            return True

    @staticmethod
    def add_to_file(file, data):
        with open(file, 'a+b') as pickle_file:
            pickle.dump(data, pickle_file)


if __name__ == '__main__':
    file = "%APPDATA%/Wiz101Calc/StandardSpells.pickle"
    file = os.path.expandvars(file)
    StandardSpells('standard', 'asdf', 1, 2, 3)
    StandardSpells.read_pickle_file(file)
    print('FIRST SUBMISSION DONE')
    StandardSpells('standard', 'asdf', 2, 4, 8)
    StandardSpells.read_pickle_file(file)
    print('SECOND SUBMISSION DONE')
    StandardSpells('standard', 'qwer', 3, 6, 9)
    StandardSpells.read_pickle_file(file)
    print('THIRD SUBMISSION DONE')
    StandardSpells('standard', 'asdf', 100, 700, 230000)
    StandardSpells.read_pickle_file(file)
    print('FORTH SUBMISSION DONE')
    StandardSpells('standard', 'qwer', 6, 8, 10)
    StandardSpells.read_pickle_file(file)
    print('Fifth SUBMISSION DONE')
    StandardSpells('standard', 'asdfasdf', 1, 2, 6)
    StandardSpells.read_pickle_file(file)
    print('sixth')
    StandardSpells('standard', 'zxcv', 1, 4, 7)
    StandardSpells.read_pickle_file(file)
    print('seventh')
