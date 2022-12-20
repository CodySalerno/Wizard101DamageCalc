from GenericSpells import GenericSpells as Gs


class FlatBuff(Gs):
    """Flat buff spells. Child class of the generic spells.
    needs a name (str),
    cost of the spell (int),
    whether it applies to all enemies/self (true) or just one enemy (false)
    and the flat buff applied (int)."""
    def __init__(self, name: str, cost: int, multi_target: bool, flat: int):
        from file_handler import add_to_file
        super().__init__(spell_type="Flat Buff", name=name, multi_target=multi_target)
        self.cost = cost
        self.flat = flat
        self.dict["Cost"] = self.cost
        self.dict["Flat"] = self.flat
        add_to_file(self)

    def __repr__(self):
        return super().__repr__() + f"Cost: {self.cost}\nFlat buff: {self.flat}\n"


if __name__ == '__main__':
    asdf = FlatBuff('asdf', 1, True, 35)
    zxcv = FlatBuff('zxcv', 2, False, 35)
