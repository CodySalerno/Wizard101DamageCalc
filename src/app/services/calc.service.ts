import { Injectable } from "@angular/core";
import type {
  AnySpell, PercentBuff, StandardSpell, MultiplierSpell, ComboBuff, School
} from "../models/spells";
import type { Enemy } from "../models/enemy";

// ---------- utilities ----------
function powerset<T>(arr: T[]): T[][] {
  // more_itertools.powerset equivalent
  const res: T[][] = [[]];
  for (const x of arr) {
    const len = res.length;
    for (let i = 0; i < len; i++) res.push(res[i].concat(x));
  }
  return res;
}

export interface Gear {
  gearPerc: number; // e.g. 50 for +50%
  gearFlat: number; // e.g. +35 flat
}

export interface BuffedStandard {
  minDam: number;
  maxDam: number;
  names: string[];
  cost: number;
  multiTarget: boolean;
  base: StandardSpell;
  combo: ComboBuff;
}

export interface BuffedMultiplier {
  boostedDamage: number;    // per pip base damage after buffs & gear %
  flatBuff: number;         // gear flat
  names: string[];
  cost: number;             // combo cost + 1 (base pip for multiplier spell)
  multiTarget: boolean;
  base: MultiplierSpell;
  combo: ComboBuff;
}

@Injectable({ providedIn: "root" })
export class CalcService {

  makeComboBuffs(buffSpells: PercentBuff[]): ComboBuff[] {
    const combos = powerset(buffSpells);
    return combos.map(set => {
      let mult = 1;
      let cost = 0;
      let multiTarget = true;
      const names: string[] = [];
      for (const b of set) {
        names.push(b.name);
        cost += b.cost;
        if (multiTarget && !b.multiTarget) multiTarget = false;
        mult *= (100 + b.percent) / 100;
      }
      return { multiplier: mult, cost, names, multiTarget };
    });
  }

  // Combine buffs with Standard spells
  buffStandard(combo: ComboBuff, spell: StandardSpell, gear: Gear): BuffedStandard {
    const gearPerc = (100 + gear.gearPerc) / 100;
    const multiplier = combo.multiplier * gearPerc;
    return {
      minDam: spell.minDam * multiplier + gear.gearFlat,
      maxDam: spell.maxDam * multiplier + gear.gearFlat,
      names: [...combo.names, spell.name],
      cost: combo.cost + spell.cost,
      multiTarget: combo.multiTarget && spell.multiTarget,
      base: spell,
      combo
    };
    // NOTE: match Python’s float rounding behavior later if needed
  }

  // Combine buffs with Multiplier spells
  buffMultiplier(combo: ComboBuff, spell: MultiplierSpell, gear: Gear): BuffedMultiplier {
    const gearPerc = (100 + gear.gearPerc) / 100;
    return {
      boostedDamage: spell.multiplier * combo.multiplier * gearPerc, // per pip
      flatBuff: gear.gearFlat,
      names: [...combo.names, spell.name],
      cost: combo.cost + 1, // base pip cost accounted as 1
      multiTarget: combo.multiTarget && spell.multiTarget,
      base: spell,
      combo
    };
  }

  // Filter out dominated Standard results (same as Python’s filter_spells)
  filterStandard(list: BuffedStandard[]): BuffedStandard[] {
    const out: BuffedStandard[] = [];
    for (const spell of list) {
      let keep = true;
      for (const other of list) {
        if (spell !== other &&
            spell.cost >= other.cost &&
            spell.names.length >= other.names.length) {
          if (spell.cost === other.cost &&
              spell.names.length === other.names.length &&
              !out.includes(other)) {
            continue;
          }
          keep = false;
          break;
        }
      }
      if (keep) out.push(spell);
    }
    return out;
  }

  // multiplier_sim (returns [length, cost, extraPips] or null if not good enough)
  multiplierSim(
    spell: BuffedMultiplier,
    enemyHealth: number,
    maxLength: number,
    maxCost: number
  ): [number, number, number] | null {
    const base = spell.boostedDamage;
    const startLen = spell.names.length;
    const startCost = spell.cost;
    const maxIteration = Math.max(maxLength - startLen, maxCost - startCost);
    for (let pips = 1; pips < maxIteration; pips++) {
      if (base * pips + spell.flatBuff >= enemyHealth) {
        return [startLen + pips - 1, startCost + pips - 1, pips];
      }
    }
    return null;
  }

  // The main simulator
  simulate(
    standardBuffed: BuffedStandard[],
    multiplierBuffed: BuffedMultiplier[],
    enemies: Enemy[],
    useStandardMin: boolean,
    useStandardMax: boolean,
    useMultiplier: boolean,
    multiNeeded: boolean
  ) {
    const filteredStd = multiNeeded
      ? standardBuffed.filter(s => s.multiTarget)
      : standardBuffed;
    const filteredMult = multiNeeded
      ? multiplierBuffed.filter(m => m.multiTarget)
      : multiplierBuffed;

    const enemyMax = enemies.reduce((mx, e) => Math.max(mx, e.health), 0);

    // Multiplier candidates (best length + cost)
    let mShortest = Number.MAX_SAFE_INTEGER;
    let mSmallestCost = Number.MAX_SAFE_INTEGER;
    let multCandidates: Array<{ spell: BuffedMultiplier; extraPips: number }> = [];
    if (useMultiplier) {
      for (const m of filteredMult) {
        const res = this.multiplierSim(m, enemyMax, mShortest, mSmallestCost);
        if (!res) continue;
        const [len, cost, extra] = res;
        if (len <= mShortest && cost <= mSmallestCost) {
          mShortest = len; mSmallestCost = cost;
          multCandidates = [{ spell: m, extraPips: extra }];
        } else if (len < mShortest || cost < mSmallestCost) {
          multCandidates.push({ spell: m, extraPips: extra });
        }
      }
    }

    // Standard candidates
    const stdMin = useStandardMin
      ? filteredStd.filter(s => s.minDam >= enemyMax)
      : [];
    const stdMax = useStandardMax
      ? filteredStd.filter(s => s.maxDam >= enemyMax)
      : [];

    return {
      multiplier: multCandidates,
      standardMin: this.filterStandard(stdMin),
      standardMax: this.filterStandard(stdMax),
    };
  }
}
