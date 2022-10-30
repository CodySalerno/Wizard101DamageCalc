import pickle
import os
from tkinter import messagebox


class StandardSpells:
    def __init__(self, name, cost, min_dam, max_dam):
        self.name = name
        self.cost = cost
        self.min_dam = min_dam
        self.max_dam = max_dam
        self.check_file()

    def check_file(self):
        direc = "%APPDATA%/Wiz101Calc"
        file = "%APPDATA%/Wiz101Calc/StandardSpells.pickle"
        direc = os.path.expandvars(direc)
        file = os.path.expandvars(file)
        new_data = {
            "name": self.name,
            "cost": self.cost,
            "min_dam": self.min_dam,
            "max_dam": self.max_dam}
        if not os.path.exists(direc):  # if directory doesn't exist
            print('make directory')
            os.mkdir(direc)  # create directory
            self.add_to_file(file, new_data)  # creates and adds data to file
            return True
        # directory must exist below this point
        existing_spells = []
        try:  # assumes the file exist
            with open(file, 'rb') as pickle_file:
                while True:
                    try:
                        print('tried')
                        existing_spells.append(pickle.load(pickle_file))
                    except EOFError:
                        print('excepted')
                        break
            for spell in existing_spells:
                print('in for loop')
                if spell['name'] == self.name:
                    if spell == self.__dict__:
                        messagebox.showinfo("updating file", "This spell is already known.")
                        return True
                    self.update_to_file(file, new_data)
                    return True
            print(existing_spells)
            print('after for loop')
            self.add_to_file(file, new_data)
        except FileNotFoundError:  # if file doesn't exist
            self.add_to_file(file, new_data)

    def update_to_file(self, file, data):
        print("entered update")
        question = "This spell's name is already known with stats:\n" \
                   "Cost: " + str(self.cost) + "\n" \
                   "Minimum damage: " + str(self.min_dam) + "\n" \
                   "Maximum damage: " + str(self.max_dam) + "\n" \
                   "Would you like to change its stats to your input?"
        response = messagebox.askquestion("updating file", question)
        if response == "yes":
            self.add_to_file(file, data)
            return True

    @staticmethod
    def add_to_file(file, data):
        print('entered add')
        print(data)
        with open(file, 'a+b') as pickle_file:
            pickle.dump(data, pickle_file)


if __name__ == '__main__':
    StandardSpells('asdf', 1, 2, 3)
    StandardSpells('qwer', 3, 6, 9)
