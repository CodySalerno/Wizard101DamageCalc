import sys

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


def create_buff_and_spell_lists():
    """create_buff_and_spell_lists calculates every combination of buffs and gets a list of all attack_type spells
    Returns a tuple\n
    First is the list of all the buffs after they've been made and turned into ComboBuff objects to be more usable.\n
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
    """buff_combos is the collection of every way to combine each of the buffs.\n
    this collection isn't very usable and so quickly gets turned into a list of ComboBuff objects
    in the list calculated_buffs"""
    calculated_buffs: list[ComboB.ComboBuff] = []
    """calculated_buffs is a list of ComboBuffs, each ComboBuff is one combination of buffs."""
    for buff_set in buff_combos:  # iterates through each combination of buffs
        calculated_buffs.append(ComboB.ComboBuff(buff_set))
        # ^turns the combination of buff spells into a tuple of their combined stats and puts it in a list
    return calculated_buffs, all_attacks


def calculate_everything(calculated_buffs: list[ComboB.ComboBuff],
                         damage_spells: list[StandardS.StandardSpells | MultiS.MultiplierSpells],
                         gear_perc_buff, gear_flat_buff):
    """calculated_buffs is a list of ComboBuff objects\n
    damage_spells is a list of all the spells of type StandardSpells or MultiplierSpells.\n
    Returns two lists\n
    The first list is all the StandardSpells combined with each set of buffs.\n
    The second list is all the MultiplierSpells combined with each set of buffs."""
    standard_finished: list[BuffedS.BuffedStandard] = []
    """standard_finished is a list of the standard spells after they've been combined with buffs."""
    multiplier_finished: list[BuffedS.BuffedMultiplier] = []
    for spell in damage_spells:  # iterates through all damage spells
        if type(spell) == StandardS.StandardSpells:
            for buff_set in calculated_buffs:  # iterates through every combination of buffs
                standard_finished.append(BuffedS.BuffedStandard(buff_set, spell, gear_perc_buff, gear_flat_buff))
        elif type(spell) == MultiS.MultiplierSpells:
            for buff_set in calculated_buffs:  # iterates through every combination of buffs
                multiplier_finished.append(BuffedS.BuffedMultiplier(buff_set, spell, gear_perc_buff, gear_flat_buff))
    # Have now looped through every spell with every combination of buffs and put them into two lists.
    return standard_finished, multiplier_finished


def enemy_stats():
    multi_needed = True
    enemy_list = []

    def submission():
        try:
            enemy_health = int(enemy_health_widget.get())
            enemy_name = enemy_name_widget.get()
            Enemy(enemy_name, enemy_health)
        except ValueError:
            messagebox.showerror("Error", "Multiplier must be a number")

    def simulator_helper():
        """helper function to close out the enemy window and then call the simulator"""
        nonlocal multi_needed, enemy_list
        enemy_list = Enemy.enemy_list
        if len(enemy_list) > 1:
            multi_needed = messagebox.askyesno("Focus", "Are multi target spells necessary?\n"
                                                        "e.g. multiple weak enemies rather than one strong one weak.")
        else:
            multi_needed = False
        enemy_window.destroy()

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
    return multi_needed, enemy_list


def simulator(standard_buffed: list[BuffedS.BuffedStandard],
              multiplier_buffed: list[BuffedS.BuffedMultiplier], multi_needed: bool, enemy_list: list[Enemy],
              min_use: bool, max_use: bool, multi_use: bool):
    """Figures out which combinations of spells will beat the enemy and returns them in order below\n
    multiplier_spells\n
    standard spells using minimum damage\n
    standard spells using maximum damage"""
    if multi_needed:
        multiplier_buffed[:] = [spell for spell in multiplier_buffed if spell.multi_target]
        standard_buffed[:] = [spell for spell in standard_buffed if spell.multi_target]
    enemy_max_health: int = 0
    for curr_enemy in enemy_list:
        if curr_enemy.health > enemy_max_health:
            enemy_max_health = curr_enemy.health
    m_shortest_length = sys.maxsize
    m_smallest_cost = sys.maxsize
    multiplier_candidates: list[tuple[BuffedS.BuffedMultiplier, int]] = []
    if multi_use:
        for multiplier_spell in multiplier_buffed:
            try:
                curr_len, curr_cost, extra_rounds = \
                    multiplier_sim(multiplier_spell, enemy_max_health, m_shortest_length, m_smallest_cost)
            except TypeError:
                # not good enough multiplier
                continue
            if curr_len <= m_shortest_length and curr_cost <= m_smallest_cost:  # at least as good in both
                m_shortest_length, m_smallest_cost = curr_len, curr_cost  # change best found to current
                multiplier_candidates = [multiplier_spell, extra_rounds]  # remove old found good spells for this one
            elif curr_len < m_shortest_length or curr_cost < m_smallest_cost:  # better in one of the ways
                multiplier_candidates.append((multiplier_spell, extra_rounds))  # add it to the list of potentials.
            else:
                print("SIMULATOR FAILED THIS SHOULD BE UNREACHABLE")
    standard_max_candidates, standard_min_candidates = [], []
    for spell in standard_buffed:
        if min_use and spell.min_dam >= enemy_max_health:
            standard_min_candidates.append(spell)
        if max_use and spell.max_dam >= enemy_max_health:
            standard_max_candidates.append(spell)
    filtered_standard_max = filter_spells(standard_max_candidates)
    filter_standard_min = filter_spells(standard_min_candidates)
    return multiplier_candidates, filter_standard_min, filtered_standard_max


def filter_spells(list_of_spells: list[BuffedS.BuffedStandard]):
    filtered_list = []
    for spell in list_of_spells:  # loop through all spells
        keep = True  # flag for if spell meets criteria
        for other in list_of_spells:  # loops through rest of spell
            if spell is not other and spell.cost >= other.cost and len(spell.names) >= len(other.names):
                # ^if both are worse or equal
                if spell.cost == other.cost and len(spell.names) == len(other.names) and other not in filtered_list:
                    # ^if both are equal and not in list yet don't throw it out.
                    continue  # keep checking
                keep = False  # both are worse or equal so don't add
                break
        if keep:  # once checked against all spells add to list
            filtered_list.append(spell)
    return filtered_list


def multiplier_sim(spell: BuffedS.BuffedMultiplier, enemy_health: int, max_length: int, max_cost: int):
    """Simulates how many pips are needed for this spell combo to One Hit KO.\n
    returns the length (number of turns) and cost """
    spell_length = len(spell.names)  # length of spell being simulated
    spell_cost = spell.cost  # minimum cost of spell being simulated
    base = spell.boosted_damage  # damage the spell does if the multiplier spell has 1 pip cost
    max_iteration = max(max_length - spell_length, max_cost - spell_cost)
    # ^optimization so it doesn't do more checks than necessary.
    for pips in range(1, max_iteration):
        # ^loops through giving extra pips to spell up to the max for it to be better than current best found.
        if base * pips + spell.flat_buff > enemy_health:
            return spell_length + pips - 1, spell_cost + pips - 1, pips - 1
            # ^ needs a -1 because the BuffedMultiplier already includes a base cost and length of the spell of 1
    return -1


def spell_type_usage():
    """Asks users which types of spells they want to use. Returns True or false for\n
    Standard spell minimum damage\n
    Standard spell maximum damage\n
    multiplier spells"""
    min_use = False
    max_use = False
    multi_use = False

    def submission():
        nonlocal min_use, max_use, multi_use
        min_use = standard_min.get()
        max_use = standard_max.get()
        multi_use = multiplier.get()
        window.destroy()
    window = tk.Tk()
    window.title("Spells")
    standard_min = tk.IntVar()
    standard_max = tk.IntVar()
    multiplier = tk.IntVar()
    tk.Label(master=window, text="Select the spells you want to use").grid(row=0)
    tk.Checkbutton(master=window, text="Standard spells minimum damage", variable=standard_min).grid(row=1)
    tk.Checkbutton(master=window, text="Standard spells maximum damage", variable=standard_max).grid(row=2)
    tk.Checkbutton(master=window, text="Per pip (multiplier) spells", variable=multiplier).grid(row=3)
    w.Button(master=window, text="submit", state=tk.DISABLED, command=submission).grid(row=4)
    # ^submission disabled till entries filled out
    window.mainloop()
    return min_use, max_use, multi_use


def gear():
    """Finds out the percent damage increase and the flat damage increase of the user's gear\n
     Returns percent damage increase and flat damage increase."""
    perc_damage = 0
    flat_damage = 0

    def submission():
        nonlocal perc_damage, flat_damage
        state = 0
        try:
            perc_damage = int(percent_damage_entry.get())
            state = 1
            flat_damage = int(flat_damage_entry.get())
            window.destroy()
        except ValueError:
            if state == 0:
                messagebox.showerror("Error", "Percent damage must be an integer.")
            if state == 1:
                messagebox.showerror("Error", "Flat damage increase must be an integer.")

    window = tk.Tk()
    tk.Label(master=window, text="If your gear increases damage by 50% percent damage should be 50").grid(row=0)
    tk.Label(master=window, text="If no gear increase enter 0").grid(row=1)
    percent_damage_entry = w.Entry("Percent damage increase from gear", master=window, width=30)
    percent_damage_entry.grid(row=2)
    flat_damage_entry = w.Entry("Flat damage increase from gear", master=window, width=30)
    flat_damage_entry.grid(row=3)
    w.Button(master=window, text="submit", state=tk.DISABLED, command=submission).grid(row=4)
    window.mainloop()
    return perc_damage, flat_damage


def display(multi: list[tuple[BuffedS.BuffedMultiplier, int]],
            standard_min: list[BuffedS.BuffedStandard], standard_max: list[BuffedS.BuffedStandard]):
    current_spell_names = []
    for spell, extra in multi:
        for name in spell.names:
            current_spell_names.append(name)
        pass  # display list of names and extra
        current_spell_names = []
    for spell in standard_min:
        for name in spell.names:
            current_spell_names.append(name)
        pass  # display list of names
        current_spell_names = []
    for spell in standard_max:
        for name in spell.names:
            current_spell_names.append(name)
        pass  # display list of names
        current_spell_names = []


def main():
    perc_gear, flat_gear = gear()
    buffs, spells = create_buff_and_spell_lists()
    standard_calculated, multiplier_calculated = calculate_everything(buffs, spells, perc_gear, flat_gear)
    multi_needed, enemy_list = enemy_stats()
    min_use, max_use, multi_use = spell_type_usage()
    multi, s_min, s_max = \
        simulator(standard_calculated, multiplier_calculated, multi_needed, enemy_list, min_use, max_use, multi_use)
    # TODO: make output of above 3 variables pretty.
    display(multi, s_min, s_max)
