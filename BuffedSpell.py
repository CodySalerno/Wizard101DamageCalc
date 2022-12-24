from ComboBuffs import ComboBuff
from StandardSpells import StandardSpells
from MultiplierSpells import MultiplierSpells
import abc


class BaseBuffedSpell(abc.ABC):
    @abc.abstractmethod
    def __repr__(self):
        return "This is a base class, do not instantiate it; instead overload this method."


class BuffedStandard(BaseBuffedSpell):
    def __init__(self, combo_buff: ComboBuff, attack_spell: StandardSpells, gear_perc, gear_flat):
        self.buff = combo_buff
        self.attack_spell = attack_spell
        gear_perc = (100 + gear_perc) / 100
        multiplier = self.buff.multiplier * gear_perc
        flat = self.buff.flat_buff + gear_flat
        self.min_dam: float = self.attack_spell.min_dam * multiplier + flat
        self.max_dam: float = self.attack_spell.max_dam * multiplier + flat
        self.names: list[str] = []
        for name in self.buff.names:
            self.names.append(name)
        self.names.append(self.attack_spell.name)
        self.cost: int = self.attack_spell.cost + self.buff.cost
        self.multi_target = combo_buff.multi_target and attack_spell.multi_target

    def __repr__(self):
        return f"Minimum Damage: {self.min_dam}\nMaximum Damage: {self.max_dam}\n" \
               f"All Spell Names: {self.names}\nCost: {self.cost}\nMulti-target: {self.multi_target}"


class BuffedMultiplier(BaseBuffedSpell):
    def __init__(self, combo_buff: ComboBuff, attack_spell: MultiplierSpells, gear_perc, gear_flat):
        self.buff = combo_buff
        self.attack_spell = attack_spell
        gear_perc = (100 + gear_perc) / 100
        multiplier = self.buff.multiplier * gear_perc
        flat = self.buff.flat_buff + gear_flat
        self.boosted_damage: float = self.attack_spell.multiplier * multiplier
        self.flat_buff: int = flat
        self.names: list[str] = []
        for name in self.buff.names:
            self.names.append(name)
        self.names.append(self.attack_spell.name)
        self.cost: int = self.buff.cost + 1
        self.multi_target = combo_buff.multi_target and attack_spell.multi_target

    def __repr__(self):
        return f"Multiplier Damage: {self.boosted_damage}\nFlat Buff: {self.flat_buff}\n" \
               f"All Spell Names: {self.names}\nCost: {self.cost}\nMulti-target: {self.multi_target}"
