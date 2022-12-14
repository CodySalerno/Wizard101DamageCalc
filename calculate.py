import FlatBuff as FlatB
import MultiplierSpells as MultiS
import PercentBuff as PercB
import StandardSpells as StandardS
import file_handler as fh
import more_itertools


def create_buff_and_spell_lists():
    all_spells = fh.get_all_spells()  # gets all spells into 4 lists of dictionaries
    standard_spells: list[StandardS.StandardSpells] = []
    multiplier_spells: list[MultiS.MultiplierSpells] = []
    percent_buffs: list[PercB.PercentBuff] = []
    flat_buffs: list[FlatB.FlatBuff] = []
    for key, value in all_spells[0].items():  # makes a list of objects of type StandardSpells
        standard_spells.append(value)
    for key, value in all_spells[1].items():  # makes a list of objects of type MultiplierSpells
        multiplier_spells.append(value)
    for key, value in all_spells[2].items():  # makes a list of objects of type PercentBuffs
        percent_buffs.append(value)
    for key, value in all_spells[3].items():  # makes a list of objects of type FlatBuffs
        flat_buffs.append(value)
    all_buffs = percent_buffs + flat_buffs  # combines the two buff type lists
    all_attacks: tuple[list[StandardS.StandardSpells], list[MultiS.MultiplierSpells]] = \
        standard_spells, multiplier_spells  # creates a tuple of two lists
    buff_combos = more_itertools.powerset(all_buffs)  # creates every combination of buffs possible
    calculated_buffs = []
    for buff_set in buff_combos:  # iterates through each combination of buffs
        calculated_buffs.append(calculate_buff(buff_set))
        # ^turns the combination of buff spells into a tuple of their combined stats and puts it in a list
    return calculated_buffs, all_attacks


def calculate_buff(buff_combo):
    multiplier: float = 1
    flat_buff: int = 0
    cost: int = 0
    names: list[str] = []
    # ^default values
    if len(buff_combo) == 0:  # if empty buff list
        return 1, 0, [], 0
    for buff in buff_combo:  # iterates through each buff in the combination
        names.append(buff.name)  # adds the name of each buff into the list
        cost += buff.cost  # adds the cost of all buffs together
        if type(buff) == PercB.PercentBuff:  # if the buff is a percentage multiplier
            percent = (100 + buff.percent) / 100  # buff.percent is an int from 1 to 100.
            # ^turns it into a float between 1 and 2 to multiply together
            multiplier *= percent  # increases the multiplier
        elif type(buff) == FlatB.FlatBuff:  # if the buff is a flat addition
            flat_buff += buff.flat  # increases the flat buff
    return multiplier, flat_buff, names, cost  # returns the tuple with all important info


def calculate_everything(calculated_buffs: list[tuple[float, int, list[str], int]],
                         damage_spells: tuple[list[StandardS.StandardSpells], list[MultiS.MultiplierSpells]]):
    """Calculated buffs is a list of tuples with the values in order multiplier, flatt buff, names, cost"""
    for spell in damage_spells[0]:  # iterates through all standard spells
        for buff_set in calculated_buffs:  # iterates through every combination of buffs
            min_dam = spell.min_dam * buff_set[0] + buff_set[1]
            max_dam = spell.max_dam * buff_set[0] + buff_set[1]
            cost = spell.cost + buff_set[3]
    for spell in damage_spells[1]:  # iterates through all multiplier spells
        for buff_set in calculated_buffs:  # iterates through every combination of buffs
            pass


print(create_buff_and_spell_lists())
