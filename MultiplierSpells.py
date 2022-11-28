from GenericSpells import GenericSpells as Gs


class MultiplierSpells(Gs):
    def __init__(self, name: str, multi_target: bool, multiplier: float):
        from file_handler import add_to_file
        super().__init__(spell_type="Multiplier", name=name)
        self.multi_target = multi_target
        self.multiplier = multiplier
        self.dict["Multiple Targets"] = multi_target
        self.dict["Multiplier"] = self.multiplier
        add_to_file(self)

    def __repr__(self):
        return super().__repr__() + f"Multiple Targets: {self.multi_target}\nMultiplier: {self.multiplier}"
