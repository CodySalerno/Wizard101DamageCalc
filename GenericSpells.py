class GenericSpells:
    def __init__(self, name, spell_type):
        self.dict = {}
        self.name = name
        self.type = spell_type
        self.dict["Type"] = self.type

    def __repr__(self):
        return f"Name: {self.name}\nType: {self.type}\n"
