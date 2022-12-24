from ComboBuffs import ComboBuff
from StandardSpells import StandardSpells
from MultiplierSpells import MultiplierSpells
import abc


class BaseBuffedSpell(abc.ABC):
    @abc.abstractmethod
    def __repr__(self):
        return "This is a base class, do not instantiate it; instead overload this method."


class BuffedStandard(BaseBuffedSpell):
    def __init__(self, combo_buff: ComboBuff, attack_spell: StandardSpells):
        self.buff = combo_buff
        self.attack_spell = attack_spell
        self.min_dam: float = self.attack_spell.min_dam * self.buff.multiplier + self.buff.flat_buff
        self.max_dam: float = self.attack_spell.max_dam * self.buff.multiplier + self.buff.flat_buff
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
    def __init__(self, combo_buff: ComboBuff, attack_spell: MultiplierSpells):
        self.buff = combo_buff
        self.attack_spell = attack_spell
        self.boosted_damage: float = self.attack_spell.multiplier * self.buff.multiplier
        self.flat_buff: int = self.buff.flat_buff
        self.names: list[str] = []
        for name in self.buff.names:
            self.names.append(name)
        self.names.append(self.attack_spell.name)
        self.cost: int = self.buff.cost + 1
        self.multi_target = combo_buff.multi_target and attack_spell.multi_target

    def __repr__(self):
        return f"Multiplier Damage: {self.boosted_damage}\nFlat Buff: {self.flat_buff}\n" \
               f"All Spell Names: {self.names}\nCost: {self.cost}\nMulti-target: {self.multi_target}"
