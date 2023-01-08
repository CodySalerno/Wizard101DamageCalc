class GenericSpells:
    def __init__(self, name: str, spell_type: str, multi_target: bool, school: str):
        self.dict = {}
        self.name = name
        self.type = spell_type
        self.multi_target = multi_target
        self.school = school
        self.dict["Name"] = self.name
        self.dict["Type"] = self.type
        self.dict["Multi-target"] = self.multi_target
        self.dict["School"] = self.school

    def __repr__(self):
        return f"Name: {self.name}\nType: {self.type}\nMulti-target: {self.multi_target}\nSchool: {self.school}\n"
