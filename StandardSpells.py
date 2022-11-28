from GenericSpells import GenericSpells as Gs


class StandardSpells(Gs):
    def __init__(self, name: str, cost: int, multi_target: bool, min_dam: int, max_dam: int):
        from file_handler import add_to_file
        super().__init__(spell_type="Standard", name=name)
        self.cost = cost
        self.multi_target = multi_target
        self.min_dam = min_dam
        self.max_dam = max_dam
        self.dict["Cost"] = self.cost
        self.dict["Multiple Targets"] = self.multi_target
        self.dict["Minimum Damage"] = self.min_dam
        self.dict["Maximum Damage"] = self.max_dam
        add_to_file(self)

    def __repr__(self):
        return super().__repr__() + f"Cost: {self.cost}\nMultiple Targets: {self.multi_target}\n" \
                                    f"Minimum Damage: {self.min_dam}\nMaximum Damage: {self.max_dam}"


if __name__ == '__main__':
    asdf = StandardSpells('asdf', 1, True, 2, 3)
    zxcv = StandardSpells('zxcv', 2, True, 4, 6)
