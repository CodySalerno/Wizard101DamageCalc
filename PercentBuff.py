from GenericSpells import GenericSpells as Gs


class PercentBuff(Gs):
    def __init__(self, name, cost, percent):
        from file_handler import add_to_file
        super().__init__(spell_type="Percent Buff", name=name)
        self.cost = cost
        self.percent = percent
        self.dict["Cost"] = self.cost
        self.dict["Percent"] = self.percent
        add_to_file(self)

    def __repr__(self):
        return super().__repr__() + f"Cost: {self.cost}\nPercent buff: {self.percent}"


if __name__ == '__main__':
    asdf = PercentBuff('asdf', 1, 35)
    zxcv = PercentBuff('zxcv', 2, 35)
