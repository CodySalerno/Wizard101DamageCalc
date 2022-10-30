import json


class StandardSpells:
    def __init__(self, name, cost, min_dam, max_dam):
        self.name = name
        self.cost = cost
        self.min_dam = min_dam
        self.max_dam = max_dam
        self.add_to_file()

    def add_to_file(self):
        json_data = json.dumps(self.__dict__)
        print(json_data)
