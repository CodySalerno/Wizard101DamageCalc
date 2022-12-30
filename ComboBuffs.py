import PercentBuff as PercB


class ComboBuff:
    def __init__(self, buff_tuple: tuple[PercB.PercentBuff, ...]):
        self.multiplier: float = 1
        self.cost: int = 0
        self.names: list[str] = []
        self.multi_target = True
        for buff in buff_tuple:  # iterates through each buff in the combination
            self.names.append(buff.name)  # adds the name of each buff into the list
            self.cost += buff.cost  # adds the cost of all buffs together
            if self.multi_target is True and buff.multi_target is False:
                self.multi_target = False
            percent = (100 + buff.percent) / 100  # buff.percent is an int from 1 to 100.
            # ^turns it into a float between 1 and 2 to multiply together
            self.multiplier *= percent  # increases the multiplier
