class GenericSpells:
    def __init__(self, name: str, spell_type: str):
        self.dict = {}
        self.name = name
        self.type = spell_type
        self.dict["Name"] = self.name
        self.dict["Type"] = self.type

    def __repr__(self):
        return f"Name: {self.name}\nType: {self.type}\n"
