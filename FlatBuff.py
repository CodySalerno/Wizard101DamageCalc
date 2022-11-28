from GenericSpells import GenericSpells as Gs


class FlatBuff(Gs):
    def __init__(self, name, cost, flat):
        from file_handler import add_to_file
        super().__init__(spell_type="Flat Buff", name=name)
        self.cost = cost
        self.flat = flat
        self.dict["Cost"] = self.cost
        self.dict["flat"] = self.flat
        add_to_file(self)

    def __repr__(self):
        return super().__repr__() + f"Cost: {self.cost}\nPercent buff: {self.flat}"


if __name__ == '__main__':
    asdf = FlatBuff('asdf', 1, 35)
    zxcv = FlatBuff('zxcv', 2, 35)
