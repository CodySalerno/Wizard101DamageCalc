import FlatBuff as FlatB
import MultiplierSpells as MultiS
import PercentBuff as PercB
import StandardSpells as StandardS
import file_handler as fh
import more_itertools
import tkinter as tk
from tkinter import messagebox
import widgets as w
import Enemy


def create_buff_and_spell_lists():
    """create_buff_and_spell_lists calculates every combination of buffs and gets a list of all attack spells."""
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
    all_buffs: list[FlatB.FlatBuff | PercB.PercentBuff] = []
    for i in percent_buffs:
        all_buffs.append(i)
    for i in flat_buffs:
        all_buffs.append(i)
    # adds all flat and percent buffs to one list
    # instead could do below but leads to type hinting warning
    # all_buffs = percent_buffs + flat_buffs
    all_attacks: list[StandardS.StandardSpells | MultiS.MultiplierSpells] = []
    for i in standard_spells:
        all_attacks.append(i)
    for i in multiplier_spells:
        all_attacks.append(i)
    # adds all Standard spells and Multiplier Spells to one list
    # instead could do below but leads to type hinting warning
    # all_attacks = standard_spells + multiplier_spells
    buff_combos = more_itertools.powerset(all_buffs)  # creates every combination of buffs possible
    """buff_combos is the a collection of every way to combine each of the buffs.
    this collection isn't usable and so quickly gets turned into a list of each combination with some formatting done
    through the calculate_buff() method that makes the list more usable."""
    calculated_buffs: list[tuple[float, int, list[str], int]] = []
    """calculated_buffs is a list of tuples, each tuple is one combination of buffs.
    In order the tuple represents:
    Damage multiplier,
    Flat damage increase, 
    List of the names of the buffs in the combination,
    Total cost of all buffs in the combination"""
    for buff_set in buff_combos:  # iterates through each combination of buffs
        calculated_buffs.append(calculate_buff(buff_set))
        # ^turns the combination of buff spells into a tuple of their combined stats and puts it in a list
    return calculated_buffs, all_attacks


def calculate_buff(buff_combo):
    """calculate_buff is ran during create_buff_and_spell_lists to turn the collection of combos into a list of tuples.
    Each tuple is one combination of buffs. This method is just to make the data more usable. """
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
                         damage_spells: list[StandardS.StandardSpells | MultiS.MultiplierSpells]):
    """Calculated buffs is a list of tuples with the values in order multiplier, flatt buff, names, cost
    damage spells is a list of all the spells of type StandardSpells or MultiplierSpells."""
    standard_finished: list[tuple[float, float, list[str], int]] = []
    """standard_finished is a list of the standard spells after they've been combined with buffs.
    the list is [minimum damage, maximum damage, list of names, total cost]
    There should be duplicates of spells because they will have different stats since they've been combined
    with different buffs."""
    multiplier_finished = []
    for spell in damage_spells:  # iterates through all damage spells
        if type(spell) == StandardS.StandardSpells:
            for buff_set in calculated_buffs:  # iterates through every combination of buffs
                min_dam: float = spell.min_dam * buff_set[0] + buff_set[1]
                max_dam: float = spell.max_dam * buff_set[1] + buff_set[1]
                names: list[str] = []
                for name in buff_set[2]:
                    names.append(name)
                names.append(spell.name)
                cost: int = spell.cost + buff_set[3]
                stats = (min_dam, max_dam, names, cost)
                standard_finished.append(stats)

        elif type(spell) == MultiS.MultiplierSpells:
            for buff_set in calculated_buffs:  # iterates through every combination of buffs
                boosted_damage: float = spell.multiplier * buff_set[0]
                flat_buff: int = buff_set[1]
                names: list[str] = []
                for name in buff_set[2]:
                    names.append(name)
                names.append(spell.name)
                cost: int = buff_set[3]
                combined_spell = (boosted_damage, flat_buff, names, cost)
                multiplier_finished.append(combined_spell)
    # Have now looped through every spell with every combination of buffs and put them into two lists.
    return standard_finished, multiplier_finished


def enemy_stats():
    def submission():
        try:
            enemy_health = int(enemy_health_widget.get())
            Enemy.Enemy(enemy_health)
            root.destroy()
        except ValueError:
            messagebox.showerror("Error", "Multiplier must be a number")
    root = tk.Tk()
    root.title("Enemy")
    enemy_health_widget = w.Entry("Enemy maximum health", master=root, width=50)
    enemy_health_widget.grid(row=0)
    submit_button = w.Button(master=root, text="submit", state=tk.DISABLED, command=submission)
    # ^submission disabled till entries filled out
    submit_button.grid(row=6)


def main():
    buffs, spells = create_buff_and_spell_lists()
    # buffs is a list of tuples containing in order: multiplier, flat buff, names of spells in that combo, total cost.
    # spells is a list of all the spells of the StandardSpells and MultiplierSpells types.
    standard_done, multiplier_done = calculate_everything(buffs, spells)
    costs_and_max_dam: dict[int, tuple[float, float, list[str], int]] = {}
    """costs_and_max_dam is a dict of a key for the cost and a value of the spell obj"""
    costs_and_min_dam: dict[int, tuple[float, float, list[str], int]] = {}
    """costs_and_min_dam is a dict of a key for the cost and a value of the spell obj"""
    for spell in standard_done:
        try:
            if costs_and_max_dam[spell[3]][1] < spell[1]:
                # ^if dict[spell[cost]] (this sets the spell's cost to the key) < spell[max_dam]
                costs_and_max_dam[spell[3]] = spell
        except KeyError:  # if this value isn't in the dictionary as a key yet
            costs_and_max_dam[spell[3]] = spell
        try:
            if costs_and_min_dam[spell[3]][0] < spell[0]:
                # ^if dict[spell[cost]] (this sets the spell's cost to the key) < spell[min_dam]
                costs_and_min_dam[spell[3]] = spell
        except KeyError:  # if this value isn't in the dictionary as a key yet
            costs_and_min_dam[spell[3]] = spell
    enemy_stats()
