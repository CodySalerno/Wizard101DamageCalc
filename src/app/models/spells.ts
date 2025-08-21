import { School } from "../constants/schools";

export interface GenericSpell {
  name: string;
  type: "Standard" | "Multiplier" | "Percent Buff" | "Flat Buff";
  multiTarget: boolean;
  school: School;
}

export interface StandardSpell extends GenericSpell {
  type: "Standard";
  cost: number;
  minDam: number;
  maxDam: number;
}

export interface MultiplierSpell extends GenericSpell {
  type: "Multiplier";
  multiplier: number; // damage per pip
}

export interface PercentBuff extends GenericSpell {
  type: "Percent Buff";
  cost: number;
  percent: number; // 1..100
}

export type AnySpell = StandardSpell | MultiplierSpell | PercentBuff;

export interface ComboBuff {
  multiplier: number;   // product of (1+percent/100)
  cost: number;         // sum of buff costs
  names: string[];      // ordered names of buffs
  multiTarget: boolean; // true only if all buffs are multiTarget
}
