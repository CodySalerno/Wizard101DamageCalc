class GenericSpells:
    def __init__(self, name: str, spell_type: str, multi_target: bool):
        self.dict = {}
        self.name = name
        self.type = spell_type
        self.multi_target = multi_target
        self.dict["Name"] = self.name
        self.dict["Type"] = self.type
        self.dict["Multi-target"] = self.multi_target

    def __repr__(self):
        return f"Name: {self.name}\nType: {self.type}\nMulti-target; {self.multi_target}\n"
