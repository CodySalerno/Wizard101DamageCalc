from GenericSpells import GenericSpells as Gs


class MultiplierSpells(Gs):
    def __init__(self, name, multiplier):
        super().__init__(spell_type="Multiplier", name=name)
        self.multiplier = multiplier
        self.dict["Multiplier"] = self.multiplier

    def __repr__(self):
        return super().__repr__() + f"Multiplier: {self.multiplier}"
