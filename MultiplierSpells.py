from GenericSpells import GenericSpells as Gs


class MultiplierSpells(Gs):
    def __init__(self, name, multiplier):
        from file_handler import add_to_file
        super().__init__(spell_type="Multiplier", name=name)
        self.multiplier = multiplier
        self.dict["Multiplier"] = self.multiplier
        add_to_file(self)

    def __repr__(self):
        return super().__repr__() + f"Multiplier: {self.multiplier}"
