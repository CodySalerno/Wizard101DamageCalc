from GenericSpells import GenericSpells as Gs


class FlatBuff(Gs):
    """Flat buff spells. Child class of the generic spells.
    needs a name (str),
    cost of the spell (int),
    whether it applies to all enemies/self (true) or just one enemy (false)
    and the flat buff applied (int)."""
    def __init__(self, name: str, cost: int, multi_target: bool, flat: int):
        from file_handler import add_to_file
        super().__init__(spell_type="Flat Buff", name=name)
        self.cost = cost
        self.multi = multi_target
        self.flat = flat
        self.dict["Cost"] = self.cost
        self.dict["Multiple Targets"] = multi_target
        self.dict["Flat"] = self.flat
        add_to_file(self)

    def __repr__(self):
        return super().__repr__() + f"Cost: {self.cost}\nMultiple Targets: {self.multi}\nFlat buff: {self.flat}\n"


if __name__ == '__main__':
    asdf = FlatBuff('asdf', 1, True, 35)
    zxcv = FlatBuff('zxcv', 2, False, 35)
