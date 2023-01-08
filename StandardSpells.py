from GenericSpells import GenericSpells as Gs


class StandardSpells(Gs):
    """Standard damage spells. Child class of the generic spells.
    needs a name (str),
    cost (int)
    whether it applies to all enemies(true) or just one enemy (false)
    minimum damage dealt (int),
    and maximum damage dealt (int)"""
    def __init__(self, name: str, cost: int, multi_target: bool, school: str, min_dam: int, max_dam: int):
        from file_handler import add_to_file
        super().__init__(spell_type="Standard", name=name, multi_target=multi_target, school=school)
        self.cost = cost
        self.min_dam = min_dam
        self.max_dam = max_dam
        self.dict["Cost"] = self.cost
        self.dict["Minimum Damage"] = self.min_dam
        self.dict["Maximum Damage"] = self.max_dam
        add_to_file(self)

    def __repr__(self):
        return super().__repr__() + f"Cost: {self.cost}\nMinimum Damage: {self.min_dam}\nMaximum Damage: {self.max_dam}"
