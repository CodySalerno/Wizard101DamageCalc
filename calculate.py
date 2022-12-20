import FlatBuff as FlatB
import MultiplierSpells as MultiS
import PercentBuff as PercB
import StandardSpells as StandardS
import ComboBuffs as ComboB
import BuffedSpell as BuffedS
import file_handler as fh
import more_itertools
import tkinter as tk
from tkinter import messagebox
import widgets as w
from Enemy import Enemy


# Order of methods usually
# create_buff_and_spell_list
# calculate_everything
# optimizer
# enemy_stats
# simulator


def create_buff_and_spell_lists():
    """create_buff_and_spell_lists calculates every combination of buffs and gets a list of all attack_type spells
    Returns a tuple

    First is the list of all the buffs after they've been made and turned into ComboBuff objects to be more usable.

    Second is the list of all the attack_type spells."""
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
    calculated_buffs: list[ComboB.ComboBuff] = []
    """calculated_buffs is a list of tuples, each tuple is one combination of buffs.
    In order the tuple represents:
    Damage multiplier,
    Flat damage increase, 
    List of the names of the buffs in the combination,
    Total cost of all buffs in the combination"""
    for buff_set in buff_combos:  # iterates through each combination of buffs
        calculated_buffs.append(ComboB.ComboBuff(buff_set))
        # ^turns the combination of buff spells into a tuple of their combined stats and puts it in a list
    return calculated_buffs, all_attacks


def calculate_everything(calculated_buffs: list[ComboB.ComboBuff],
                         damage_spells: list[StandardS.StandardSpells | MultiS.MultiplierSpells]):
    """calculated_buffs is a list of ComboBuff objects

    damage_spells is a list of all the spells of type StandardSpells or MultiplierSpells.

    Returns two lists

    The first list is all the StandardSpells combined with each set of buffs.

    The second list is all the MultiplierSpells combined with each set of buffs."""
    standard_finished: list[BuffedS.BuffedStandard] = []
    """standard_finished is a list of the standard spells after they've been combined with buffs."""
    multiplier_finished: list[BuffedS.BuffedMultiplier] = []
    for spell in damage_spells:  # iterates through all damage spells
        if type(spell) == StandardS.StandardSpells:
            for buff_set in calculated_buffs:  # iterates through every combination of buffs
                standard_finished.append(BuffedS.BuffedStandard(buff_set, spell))
        elif type(spell) == MultiS.MultiplierSpells:
            for buff_set in calculated_buffs:  # iterates through every combination of buffs
                multiplier_finished.append(BuffedS.BuffedMultiplier(buff_set, spell))
    # Have now looped through every spell with every combination of buffs and put them into two lists.
    return standard_finished, multiplier_finished


def enemy_stats(costs_and_min_dam:  dict[int, list[BuffedS.BuffedStandard]],
                costs_and_max_dam: dict[int, list[BuffedS.BuffedStandard]],
                multiplier_done: list[BuffedS.BuffedMultiplier]):
    def submission():
        try:
            enemy_health = int(enemy_health_widget.get())
            enemy_name = enemy_name_widget.get()
            Enemy(enemy_name, enemy_health)
        except ValueError:
            messagebox.showerror("Error", "Multiplier must be a number")

    def simulator_helper():
        """helper function to close out the enemy window and then call the simulator"""
        enemy_window.destroy()
        simulator(costs_and_min_dam, costs_and_max_dam, multiplier_done)

    enemy_window = tk.Tk()
    enemy_window.title("Enemy")
    enemy_name_widget = w.Entry("Enemy name", master=enemy_window, width=50)
    enemy_name_widget.grid(row=0)
    enemy_health_widget = w.Entry("Enemy maximum health", master=enemy_window, width=50)
    enemy_health_widget.grid(row=1)
    w.Button(master=enemy_window, text="submit", state=tk.DISABLED, command=submission).grid(row=2, column=0)
    # ^submission disabled till entries filled out
    tk.Button(master=enemy_window, text="All enemies submitted",
              state=tk.NORMAL, command=simulator_helper).grid(row=2, column=1)
    enemy_window.mainloop()


def simulator(standard_min_dict: dict[int, list[BuffedS.BuffedStandard]],
              standard_max_dict: dict[int, list[BuffedS.BuffedStandard]],
              multiplier_list: list[BuffedS.BuffedMultiplier]):
    enemy_list = Enemy.enemy_list
    one_enemy = True
    if len(enemy_list) > 1:
        focus = messagebox.askyesno("Focus", "Are single target spells okay?\n"
                                             "e.g. one strong enemy with some weak ones that aren't threats.")
        if not focus:
            one_enemy = False
    for cost, list_of_buffed_spells in standard_min_dict.items():
        print(cost)
        for buffed_spell in list_of_buffed_spells:
            pass


def optimizer(standard_calced: list[BuffedS.BuffedStandard],
              costs_and_min_dam: dict[int, list[BuffedS.BuffedStandard]] = None,
              costs_and_max_dam: dict[int, list[BuffedS.BuffedStandard]] = None):
    """Returns a tuple containing 2 dictionaries, the first based on standard spells minimum damage.
    The second based on standard spells maximum damage.

    Each dictionary has keys based on the total cost of a combination of spells with the value being
    a tuple of float, float, list[str], int.

    The first float is the combo's minimum damage.

    The second float is the combo's maximum damage.

    The list[str] is a list of the names of all spells needed to be cast.

    The int is the total cost of the combination (the same as the key)."""
    if costs_and_min_dam is None:
        cost_min = {}
    else:
        cost_min = costs_and_min_dam
    if costs_and_max_dam is None:
        cost_max = {}
    else:
        cost_max = costs_and_max_dam
    change = False  # value stating if any changes were made
    for spell in standard_calced:  # loops through all combinations of spells
        max_dam = spell.max_dam  # maximum damage of the current iteration
        length = len(spell.names)  # number of spells in the combination
        try:
            good = True  # flag for if this combination isn't beaten by another spell
            same = False  # flag for if this combination is already in the dictionary
            sames_indexes = []  # list of indexes the spell is found at
            for index, value in enumerate(cost_max[spell.cost]):
                if spell == value:  # checks if the combination is already in the list
                    same = True
                    sames_indexes.append(index)
                elif max_dam <= value.max_dam and length >= len(value.names):
                    # ^checks if any combination already in the list has better stats.
                    good = False
                    break
            if good and not same:  # if no spell is completely better, and it's not already in the list.
                cost_max[spell.cost].append(spell)  # adds it to the list.
                change = True  # a change to the dictionary was made
            elif same and not good:  # if this spell was already in but is no longer good enough.
                for i in sames_indexes:  # removes spell from any indexes it was found in.
                    cost_max[spell.cost].pop(i)
                    change = True  # change was made
        except KeyError:  # no dictionary key for this cost exists yet.
            cost_max[spell.cost] = [spell]
            change = True
    # TODO: make below for loop part of above for loop.
    for spell in standard_calced:  # repeats above process for minimum damage
        min_dam = spell.min_dam
        length = len(spell.names)
        try:
            good = True
            same = False
            sames_indexes = []
            for index, value in enumerate(cost_min[spell.cost]):
                if spell == value:
                    same = True
                    sames_indexes.append(index)
                elif min_dam <= value.min_dam and length >= len(value.names):
                    good = False
                    break
            if good and not same:
                cost_min[spell.cost].append(spell)
                change = True
            elif same and not good:
                for i in sames_indexes:
                    cost_min[spell.cost].pop(i)
                    change = True
        except KeyError:
            cost_min[spell.cost] = [spell]
            change = True
    if change:  # if any changes were made rerun this method with new dictionaries
        return optimizer(standard_calced, cost_min, cost_max)
    else:
        return cost_min, cost_max


def main():
    buffs, spells = create_buff_and_spell_lists()
    # buffs is a list of tuples containing in order: multiplier, flat buff, names of spells in that combo, total cost.
    # spells is a list of all the spells of the StandardSpells and MultiplierSpells types.
    standard_done_calculating, multiplier_done = calculate_everything(buffs, spells)
    """standard_done_calculating is a list of the standard spells after they've been combined with buffs. 
    The list is [minimum damage, maximum damage, list of names, total cost] 
    There should be duplicates of spells because they will have different stats 
    since they've been combined with different buffs."""
    cost_and_min_dam, cost_and_max_dam = optimizer(standard_done_calculating)
    print(cost_and_min_dam)
    print(cost_and_max_dam)
    enemy_stats(cost_and_min_dam, cost_and_max_dam, multiplier_done)
