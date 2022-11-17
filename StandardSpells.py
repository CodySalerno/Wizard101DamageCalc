from GenericSpells import GenericSpells as Gs


class StandardSpells(Gs):
    def __init__(self, name, cost, min_dam, max_dam):
        from file_handler import add_to_file
        super().__init__(spell_type="Standard", name=name)
        self.cost = cost
        self.min_dam = min_dam
        self.max_dam = max_dam
        self.dict["Cost"] = self.cost
        self.dict["Minimum Damage"] = self.min_dam
        self.dict["Maximum Damage"] = self.max_dam
        add_to_file(self)

    def __repr__(self):
        return super().__repr__() + f"Cost: {self.cost}\nMinimum Damage: {self.min_dam}\nMaximum Damage: {self.max_dam}"


if __name__ == '__main__':
    asdf = StandardSpells('asdf', 1, 2, 3)
    zxcv = StandardSpells('zxcv', 2, 4, 6)
