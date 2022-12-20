from GenericSpells import GenericSpells as Gs


class MultiplierSpells(Gs):
    """Multiplier damage spells. Child class of the generic spells.
    needs a name (str),
    whether it applies to all enemies(true) or just one enemy (false)
    and the multiplier each pips increases the damage by (float)"""
    def __init__(self, name: str, multi_target: bool, multiplier: float):
        from file_handler import add_to_file
        super().__init__(spell_type="Multiplier", name=name, multi_target=multi_target)
        self.multiplier = multiplier
        self.dict["Multiplier"] = self.multiplier
        add_to_file(self)

    def __repr__(self):
        return super().__repr__() + f"Multiplier: {self.multiplier}"
