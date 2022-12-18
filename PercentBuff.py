from GenericSpells import GenericSpells as Gs


class PercentBuff(Gs):
    """Percent buff spells. Child class of the generic spells.
    needs a name (str),
    cost of the spell (int),
    whether it applies to all enemies/self (true) or just one enemy (false)
    and the percentage buff applied (int).
    e.g. a buff that makes a 10 damage spell do 15 should have a percentage buff argument of 50."""
    def __init__(self, name: str, cost: int, multi_target: bool, percent: int):
        from file_handler import add_to_file
        super().__init__(spell_type="Percent Buff", name=name)
        self.cost = cost
        self.multi_target = multi_target
        self.percent = percent
        self.dict["Cost"] = self.cost
        self.dict["Multiple Targets"] = self.multi_target
        self.dict["Percent"] = self.percent

        add_to_file(self)

    def __repr__(self):
        return super().__repr__() + f"Cost: {self.cost}\nMultiple Targets: {self.multi_target}\n" \
                                    f"Percent buff: {self.percent}"


if __name__ == '__main__':
    asdf = PercentBuff('asdf', 1, True, 35)
    zxcv = PercentBuff('zxcv', 2, False, 35)
